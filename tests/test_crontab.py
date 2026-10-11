import os
import json
import unittest
import jc.parsers.crontab

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab.out'), 'r', encoding='utf-8') as f:
        centos_7_7_crontab = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-no-normal-entries.out'), 'r', encoding='utf-8') as f:
        generic_crontab_no_normal_entries = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-var-fix.out'), 'r', encoding='utf-8') as f:
        generic_crontab_var_fix = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab.json'), 'r', encoding='utf-8') as f:
        centos_7_7_crontab_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-no-normal-entries.json'), 'r', encoding='utf-8') as f:
        generic_crontab_no_normal_entries_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-var-fix.json'), 'r', encoding='utf-8') as f:
        generic_crontab_var_fix_json = json.loads(f.read())


    def test_crontab_nodata(self):
        """
        Test 'crontab' with no data
        """
        self.assertEqual(jc.parsers.crontab.parse('', quiet=True), {})

    def test_crontab_centos_7_7(self):
        """
        Test 'crontab' on Centos 7.7
        """
        self.assertEqual(jc.parsers.crontab.parse(self.centos_7_7_crontab, quiet=True), self.centos_7_7_crontab_json)

    def test_crontab_no_normal_entries(self):
        """
        Test 'crontab' with no normal entries - only shortcuts
        """
        self.assertEqual(jc.parsers.crontab.parse(self.generic_crontab_no_normal_entries, quiet=True), self.generic_crontab_no_normal_entries_json)

    def test_crontab_var_fix(self):
        """
        Test 'crontab' with wildcard schedule should not generate variables from command line section
        """
        self.assertEqual(jc.parsers.crontab.parse(self.generic_crontab_var_fix, quiet=True), self.generic_crontab_var_fix_json)

    def test_whitespace_only_lines(self):
        command = 'echo "a  b\tc"'
        entry = {
            'minute': '0,15',
            'hour': '*',
            'day_of_month': '*',
            'month': '*',
            'day_of_week': '*',
            'command': command,
        }
        shortcut = {'occurrence': 'reboot', 'command': command}
        lines = [
            ' \t# comment',
            'MAILTO = "cron@example.com"',
            '0,15 * * * * ' + command,
            '@reboot ' + command,
        ]
        for raw in (False, True):
            expected_entry = dict(entry)
            if not raw:
                fields = ('minute', 'hour', 'day_of_month',
                          'month', 'day_of_week')
                for field in fields:
                    expected_entry[field] = expected_entry[field].split(',')
            expected = {
                'variables': [
                    {'name': 'MAILTO', 'value': '"cron@example.com"'}
                ],
                'schedule': [expected_entry, shortcut],
            }
            for blank in ('', '   ', '\t', ' \t '):
                for position in range(len(lines) + 1):
                    with self.subTest(raw=raw, blank=blank, position=position):
                        data = '\n'.join(
                            lines[:position] + [blank] + lines[position:]
                        ) + '\n'
                        self.assertEqual(
                            jc.parsers.crontab.parse(
                                data, raw=raw, quiet=True
                            ),
                            expected,
                        )

    def test_blank_and_comment_input(self):
        for raw in (False, True):
            for data in ('', '\n', '   ', '\t', ' \t\n\t \n'):
                with self.subTest(raw=raw, data=data):
                    self.assertEqual(
                        jc.parsers.crontab.parse(data, raw=raw, quiet=True),
                        {},
                    )
            for data in ('# comment\n', ' \t\n \t# comment\n\t \n'):
                with self.subTest(raw=raw, data=data):
                    self.assertEqual(
                        jc.parsers.crontab.parse(data, raw=raw, quiet=True),
                        {'variables': [], 'schedule': []},
                    )


if __name__ == '__main__':
    unittest.main()
