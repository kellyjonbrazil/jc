import contextlib
import io
import os
import sys
import unittest
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc
from jc.cli import JcCli


SAMPLE_KEY_ED = 'AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl'
SAMPLE_KEY_RSA = 'AAAAB3NzaC1yc2EAAAADAQABAAABgQC7vX6' + ('A' * 300)


class MyTests(unittest.TestCase):

    def test_known_hosts_nodata(self):
        """
        Test 'known_hosts' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_known_hosts_all_fixtures(self):
        """
        Test 'known_hosts' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_known_hosts_raw_output(self):
        """
        Test 'known_hosts' with raw=True preserves unsplit hosts and omits hashed
        """
        data = (
            '# Host example.com found: line 1 \n'
            f'example.com,192.0.2.10 ssh-ed25519 {SAMPLE_KEY_ED} ops\n'
            f'|1|salt=|hash= ssh-ed25519 {SAMPLE_KEY_ED}\n'
            f'@cert-authority *.example.org ssh-rsa {SAMPLE_KEY_RSA} ca\n'
        )
        expected = [
            {
                'matched_host': 'example.com',
                'hosts': 'example.com,192.0.2.10',
                'marker': None,
                'type': 'ssh-ed25519',
                'key': SAMPLE_KEY_ED,
                'comment': 'ops'
            },
            {
                'matched_host': 'example.com',
                'hosts': '|1|salt=|hash=',
                'marker': None,
                'type': 'ssh-ed25519',
                'key': SAMPLE_KEY_ED,
                'comment': None
            },
            {
                'matched_host': 'example.com',
                'hosts': '*.example.org',
                'marker': '@cert-authority',
                'type': 'ssh-rsa',
                'key': SAMPLE_KEY_RSA,
                'comment': 'ca'
            }
        ]
        result = jc.parse('known_hosts', data, raw=True, quiet=True)
        self.assertEqual(result, expected)
        for item in result:
            self.assertNotIn('hashed', item)
            self.assertEqual(
                list(item.keys()),
                ['matched_host', 'hosts', 'marker', 'type', 'key', 'comment']
            )

    def test_known_hosts_matched_host_reset(self):
        """
        Test non-Host comments and blank lines reset matched_host to None
        """
        data = (
            '# Host alpha.example.com found: line 1 \n'
            f'alpha.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
            f'|1|a=|b= ssh-rsa {SAMPLE_KEY_RSA}\n'
            '# regular comment resets matched_host\n'
            f'beta.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
            '# Host gamma.example.com found: line 5 CA\n'
            f'@cert-authority gamma.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
            '\n'
            f'delta.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
        )
        result = jc.parse('known_hosts', data, quiet=True)
        self.assertEqual(
            [r['matched_host'] for r in result],
            ['alpha.example.com', 'alpha.example.com', None, 'gamma.example.com', None]
        )

    def test_known_hosts_line_endings(self):
        """
        Test CRLF splits records while non-LF Unicode line separators do not
        """
        crlf_data = (
            f'one.example.com ssh-ed25519 {SAMPLE_KEY_ED}\r\n'
            f'two.example.com ssh-ed25519 {SAMPLE_KEY_ED} note\r\n'
        )
        crlf_result = jc.parse('known_hosts', crlf_data, quiet=True)
        self.assertEqual(
            [(r['hosts'], r['key'], r['comment']) for r in crlf_result],
            [
                (['one.example.com'], SAMPLE_KEY_ED, None),
                (['two.example.com'], SAMPLE_KEY_ED, 'note')
            ]
        )

        for sep in ('\u2028', '\x0b', '\x0c', '\r'):
            with self.subTest(sep=repr(sep)):
                data = (
                    f'one.example.com ssh-ed25519 {SAMPLE_KEY_ED} '
                    f'before{sep}two.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
                )
                result = jc.parse('known_hosts', data, quiet=True)
                self.assertEqual(len(result), 1)
                self.assertIn(sep, result[0]['comment'])

    def test_known_hosts_ascii_whitespace(self):
        """
        Test ASCII-only splitting preserves Unicode whitespace and internal comment whitespace
        """
        data = (
            f'  \talpha.example.com\tssh-ed25519\t{SAMPLE_KEY_ED}\tfirst  second\tthird  \n'
            f'beta\u00a0host.example.com ssh-ed25519 {SAMPLE_KEY_ED} lead\u3000trail\n'
        )
        result = jc.parse('known_hosts', data, quiet=True)
        self.assertEqual(
            result,
            [
                {
                    'matched_host': None,
                    'hosts': ['alpha.example.com'],
                    'hashed': False,
                    'marker': None,
                    'type': 'ssh-ed25519',
                    'key': SAMPLE_KEY_ED,
                    'comment': 'first  second\tthird'
                },
                {
                    'matched_host': None,
                    'hosts': ['beta\u00a0host.example.com'],
                    'hashed': False,
                    'marker': None,
                    'type': 'ssh-ed25519',
                    'key': SAMPLE_KEY_ED,
                    'comment': 'lead\u3000trail'
                }
            ]
        )

    def test_known_hosts_malformed_lines_warnings(self):
        """
        Test malformed lines and unrecognized markers emit warnings unless quiet=True
        """
        data = (
            'too_few_tokens ssh-ed25519\n'
            f'@unknown example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
            '@cert-authority missing_key_field\n'
            f'valid.example.com ssh-ed25519 {SAMPLE_KEY_ED} ok\n'
        )
        expected = [
            {
                'matched_host': None,
                'hosts': ['valid.example.com'],
                'hashed': False,
                'marker': None,
                'type': 'ssh-ed25519',
                'key': SAMPLE_KEY_ED,
                'comment': 'ok'
            }
        ]

        stderr_noisy = io.StringIO()
        with contextlib.redirect_stderr(stderr_noisy):
            result_noisy = jc.parse('known_hosts', data, quiet=False)
        self.assertEqual(result_noisy, expected)
        err_text = stderr_noisy.getvalue()
        self.assertIn('Skipping malformed line', err_text)
        self.assertIn('Skipping line with unrecognized marker', err_text)

        stderr_quiet = io.StringIO()
        with contextlib.redirect_stderr(stderr_quiet):
            result_quiet = jc.parse('known_hosts', data, quiet=True)
        self.assertEqual(result_quiet, expected)
        self.assertEqual(stderr_quiet.getvalue(), '')

    def test_known_hosts_empty_whitespace_and_comments_only(self):
        """
        Test whitespace-only and comment-only inputs return []
        """
        for data in ('   \t\n\n', '# comment only\n# another comment\n'):
            with self.subTest(data=repr(data)):
                self.assertEqual(jc.parse('known_hosts', data, quiet=True), [])

    def test_known_hosts_magic_parser(self):
        """
        Test JcCli magic_parser maps ssh-keygen -F and ssh-keyscan to --known-hosts
        """
        commands = {
            'jc -p ssh-keygen -F example.com': (
                '--known-hosts',
                ['p'],
                ['ssh-keygen', '-F', 'example.com']
            ),
            'jc -p ssh-keyscan example.com': (
                '--known-hosts',
                ['p'],
                ['ssh-keyscan', 'example.com']
            )
        }
        for command, expected in commands.items():
            with self.subTest(command=command):
                cli = JcCli()
                cli.args = command.split()
                cli.magic_parser()
                self.assertEqual(
                    (cli.magic_found_parser, cli.magic_options, cli.magic_run_command),
                    expected
                )

    def test_known_hosts_marker_edge_cases_and_comma_hosts(self):
        """
        Test marker-only lines, duplicate markers, comma-only hosts, and empty host segments
        """
        invalid_cases = {
            'marker-only @cert-authority': '@cert-authority\n',
            'marker-only @revoked with spaces': '@revoked  \n',
            'duplicate marker': f'@cert-authority @revoked example.com ssh-ed25519 {SAMPLE_KEY_ED}\n',
            'comma-only hosts': f',,, ssh-ed25519 {SAMPLE_KEY_ED}\n',
        }
        for name, line in invalid_cases.items():
            with self.subTest(name):
                data = line + f'ok.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
                stderr_noisy = io.StringIO()
                with contextlib.redirect_stderr(stderr_noisy):
                    result = jc.parse('known_hosts', data, quiet=False)
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]['hosts'], ['ok.example.com'])
                self.assertIn('Skipping malformed line', stderr_noisy.getvalue())

                stderr_quiet = io.StringIO()
                with contextlib.redirect_stderr(stderr_quiet):
                    result_quiet = jc.parse('known_hosts', data, quiet=True)
                self.assertEqual(result_quiet, result)
                self.assertEqual(stderr_quiet.getvalue(), '')

        comma_data = f',a.com,,b.com, ssh-ed25519 {SAMPLE_KEY_ED} \t \n'
        comma_result = jc.parse('known_hosts', comma_data, quiet=True)
        self.assertEqual(
            comma_result,
            [
                {
                    'matched_host': None,
                    'hosts': ['a.com', 'b.com'],
                    'hashed': False,
                    'marker': None,
                    'type': 'ssh-ed25519',
                    'key': SAMPLE_KEY_ED,
                    'comment': None
                }
            ]
        )

    def test_known_hosts_legacy_header_and_skipped_line_resets_matched_host(self):
        """
        Test legacy Host header sets matched_host and skipped lines reset it to None
        """
        legacy_data = (
            '# Host example.com found: line 1 type RSA\n'
            f'example.com ssh-rsa {SAMPLE_KEY_RSA}\n'
        )
        legacy_result = jc.parse('known_hosts', legacy_data, quiet=True)
        self.assertEqual(len(legacy_result), 1)
        self.assertEqual(legacy_result[0]['matched_host'], 'example.com')

        skipped_cases = {
            'malformed intervening line': 'too_few_tokens ssh-ed25519\n',
            'unrecognized marker intervening line': f'@unknown bad.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n',
        }
        for name, bad_line in skipped_cases.items():
            with self.subTest(name):
                data = (
                    '# Host alpha.example.com found: line 1 \n'
                    f'alpha.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
                    + bad_line
                    + f'beta.example.com ssh-ed25519 {SAMPLE_KEY_ED}\n'
                )
                result = jc.parse('known_hosts', data, quiet=True)
                self.assertEqual(
                    [r['matched_host'] for r in result],
                    ['alpha.example.com', None]
                )

    def test_known_hosts_warning_escapes_control_chars(self):
        """
        Test warning messages escape control characters on malformed lines
        """
        data = 'bad\x07host\x1b[31m ssh-ed25519\n'
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('known_hosts', data, quiet=False)
        self.assertEqual(result, [])
        err_text = stderr.getvalue()
        self.assertIn('Skipping malformed line', err_text)
        self.assertIn('\\x07', err_text)
        self.assertIn('\\x1b', err_text)
        self.assertNotIn('\x07', err_text)
        self.assertNotIn('\x1b', err_text)


if __name__ == '__main__':
    unittest.main()
