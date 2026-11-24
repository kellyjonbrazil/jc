import contextlib
import io
import os
import sys
import unittest
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc


class MyTests(unittest.TestCase):

    def test_conntrack_nodata(self):
        """
        Test 'conntrack' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_conntrack_all_fixtures(self):
        """
        Test 'conntrack' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_conntrack_unparsable_line_warns(self):
        """
        Test 'conntrack' warns with the offending line when a line can't be
        parsed
        """
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('conntrack', 'this is not conntrack output\n')

        self.assertEqual(result, [])
        self.assertIn(
            'Unparsable line found: this is not conntrack output',
            stderr.getvalue()
        )

    def test_conntrack_malformed_fixture_warns(self):
        """
        Test 'conntrack' warns once for each unparsable line in the malformed
        fixture, and not for its summary line
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'fixtures/generic/conntrack--malformed.out'),
                  encoding='utf-8') as f:
            data = f.read()

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('conntrack', data)

        self.assertEqual(len(result), 2)
        self.assertEqual(stderr.getvalue().count('Unparsable line found'), 4)

    def test_conntrack_summary_line_does_not_warn(self):
        """
        Test 'conntrack' skips the `flow entries/events have been shown`
        summary line silently
        """
        summaries = (
            'conntrack v1.4.9 (conntrack-tools): 2 flow entries have been shown.\n',
            'conntrack v1.4.9 (conntrack-tools): 3 flow events have been shown.\n'
        )

        for summary in summaries:
            with self.subTest(summary):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    result = jc.parse('conntrack', summary)

                self.assertEqual(result, [])
                self.assertNotIn('Unparsable line found', stderr.getvalue())

    def test_conntrack_valid_fixture_does_not_warn(self):
        """
        Test 'conntrack' doesn't warn on valid output that carries the summary
        line
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'fixtures/generic/conntrack--list.out'),
                  encoding='utf-8') as f:
            data = f.read()

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('conntrack', data)

        self.assertEqual(len(result), 6)
        self.assertNotIn('Unparsable line found', stderr.getvalue())

    def test_conntrack_quiet_suppresses_warning(self):
        """
        Test 'conntrack' suppresses the unparsable line warning when quiet is
        set
        """
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('conntrack', 'this is not conntrack output\n', quiet=True)

        self.assertEqual(result, [])
        self.assertEqual(stderr.getvalue(), '')

    def test_conntrack_progname_spaces(self):
        """
        Test 'conntrack -E -o userspace' with process names that contain
        spaces and text that looks like fields
        """
        line = ('[DESTROY] tcp      6 LAST_ACK src=192.168.136.128 dst=185.125.188.55 '
                'sport=57236 dport=443 src=185.125.188.55 dst=192.168.136.128 '
                'sport=443 dport=57236 [ASSURED] [USERSPACE] portid=4242 progname=%s\n')
        data = ''.join(line % name for name in (
            'tmux: server', 'x orig_dport=22', 'init portid=1', 'x event=NEW', 'a [OFFLOAD] b'))
        result = jc.parse('conntrack', data, quiet=True)

        self.assertEqual([r['progname'] for r in result], [
            'tmux: server', 'x orig_dport=22', 'init portid=1', 'x event=NEW', 'a [OFFLOAD] b'])

        for r in result:
            self.assertEqual(r['event'], 'DESTROY')
            self.assertEqual(r['orig_dport'], 443)
            self.assertEqual(r['reply_dport'], 57236)
            self.assertEqual(r['portid'], 4242)
            self.assertEqual(r['status'], ['ASSURED', 'USERSPACE'])

    def test_conntrack_trailing_field_does_not_overwrite(self):
        """
        Test 'conntrack' with a trailing field that repeats an earlier key
        """
        data = ('tcp      6 100 ESTABLISHED src=10.0.0.1 dst=10.0.0.2 sport=1 dport=2 '
                'src=10.0.0.2 dst=10.0.0.1 sport=2 dport=1 mark=5 mark=9 src=1.1.1.1\n')
        result = jc.parse('conntrack', data, quiet=True)
        self.assertEqual(result[0]['mark'], 5)
        self.assertEqual(result[0]['orig_src'], '10.0.0.1')
        self.assertEqual(result[0]['reply_src'], '10.0.0.2')


if __name__ == '__main__':
    unittest.main()
