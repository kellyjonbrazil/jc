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

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-whitespace-lines.out'
    ), 'r', encoding='utf-8') as f:
        whitespace_lines = f.read()

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-whitespace-only.out'
    ), 'r', encoding='utf-8') as f:
        whitespace_only = f.read()

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-whitespace-comments.out'
    ), 'r', encoding='utf-8') as f:
        whitespace_comments = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab.json'), 'r', encoding='utf-8') as f:
        centos_7_7_crontab_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-no-normal-entries.json'), 'r', encoding='utf-8') as f:
        generic_crontab_no_normal_entries_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-var-fix.json'), 'r', encoding='utf-8') as f:
        generic_crontab_var_fix_json = json.loads(f.read())

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-whitespace-lines.json'
    ), 'r', encoding='utf-8') as f:
        whitespace_lines_json = json.loads(f.read())

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-whitespace-lines-raw.json'
    ), 'r', encoding='utf-8') as f:
        whitespace_lines_raw_json = json.loads(f.read())

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-whitespace-only.json'
    ), 'r', encoding='utf-8') as f:
        whitespace_only_json = json.loads(f.read())

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-whitespace-comments.json'
    ), 'r', encoding='utf-8') as f:
        whitespace_comments_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-job-with-equals.out'), 'r', encoding='utf-8') as f:
        generic_crontab_job_with_equals = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-job-with-equals.json'), 'r', encoding='utf-8') as f:
        generic_crontab_job_with_equals_json = json.loads(f.read())

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

    def test_crontab_nodata_raw(self):
        """
        Test 'crontab' with no data in raw mode
        """
        self.assertEqual(
            jc.parsers.crontab.parse('', raw=True, quiet=True), {}
        )

    def test_crontab_whitespace_lines(self):
        """
        Test 'crontab' with whitespace-only lines
        """
        self.assertEqual(
            jc.parsers.crontab.parse(self.whitespace_lines, quiet=True),
            self.whitespace_lines_json
        )

    def test_crontab_whitespace_lines_raw(self):
        """
        Test 'crontab' with whitespace-only lines in raw mode
        """
        self.assertEqual(
            jc.parsers.crontab.parse(
                self.whitespace_lines, raw=True, quiet=True
            ),
            self.whitespace_lines_raw_json
        )

    def test_crontab_whitespace_only(self):
        """
        Test 'crontab' with whitespace-only input
        """
        self.assertEqual(
            jc.parsers.crontab.parse(self.whitespace_only, quiet=True),
            self.whitespace_only_json
        )

    def test_crontab_whitespace_only_raw(self):
        """
        Test 'crontab' with whitespace-only input in raw mode
        """
        self.assertEqual(
            jc.parsers.crontab.parse(
                self.whitespace_only, raw=True, quiet=True
            ),
            self.whitespace_only_json
        )

    def test_crontab_whitespace_comments(self):
        """
        Test 'crontab' with whitespace-only lines and comments
        """
        self.assertEqual(
            jc.parsers.crontab.parse(self.whitespace_comments, quiet=True),
            self.whitespace_comments_json
        )

    def test_crontab_whitespace_comments_raw(self):
        """
        Test 'crontab' with whitespace-only lines and comments in raw mode
        """
        self.assertEqual(
            jc.parsers.crontab.parse(
                self.whitespace_comments, raw=True, quiet=True
            ),
            self.whitespace_comments_json
        )


    def test_crontab_line_separator(self):
        """
        Test 'crontab' with a line-break character other than LF inside a field
        """
        data = '0 3 * * * /usr/bin/backup;\x0c#$(/usr/bin/other)\n'
        result = jc.parsers.crontab.parse(data, quiet=True)
        self.assertEqual(len(result['schedule']), 1)
        self.assertEqual(result['schedule'][0]['command'], '/usr/bin/backup;\x0c#$(/usr/bin/other)')

    def test_crontab_mixed_lines_order(self):
        """
        Test 'crontab' with comments, variables, shortcuts and entries interleaved
        """
        data = '# c1\nA=1\n* * * * * cmd1\n@daily x\nB=2\n# c2\n@reboot y z\n0 1 * * * cmd2\n'
        result = jc.parsers.crontab.parse(data, raw=True, quiet=True)
        self.assertEqual(result['variables'], [{'name': 'B', 'value': '2'}, {'name': 'A', 'value': '1'}])
        self.assertEqual([x['command'] for x in result['schedule']], ['cmd1', 'cmd2', 'y z', 'x'])

    def test_crontab_job_with_equals(self):
        """
        Test 'crontab' with job lines that contain '=' and do not start with a digit
        """
        self.assertEqual(jc.parsers.crontab.parse(self.generic_crontab_job_with_equals, quiet=True), self.generic_crontab_job_with_equals_json)

    def test_crontab_quoted_variable_values(self):
        """
        Test 'crontab' with quoted variable values
        """
        data = ('PATH="/usr/local/bin:/usr/bin"\n'
                "SHELL = '/bin/bash'\n"
                'MAILTO=""\n'
                'A="b\'\n'
                'B=c "d"\n'
                'C="\n'
                'D=""e""\n'
                '"NAME"=value\n'
                '0 3 * * * backup\n')
        expected = [
            {'name': '"NAME"', 'value': 'value'},
            {'name': 'D', 'value': '"e"'},
            {'name': 'C', 'value': '"'},
            {'name': 'B', 'value': 'c "d"'},
            {'name': 'A', 'value': '"b\''},
            {'name': 'MAILTO', 'value': ''},
            {'name': 'SHELL', 'value': '/bin/bash'},
            {'name': 'PATH', 'value': '/usr/local/bin:/usr/bin'}
        ]
        result = jc.parsers.crontab.parse(data, quiet=True)
        self.assertEqual(result['variables'], expected)
        self.assertEqual(result['schedule'][0]['command'], 'backup')

    def test_crontab_quoted_variable_values_raw(self):
        """
        Test 'crontab' with quoted variable values and raw output
        """
        data = 'PATH="/usr/local/bin:/usr/bin"\nSHELL=\'/bin/bash\'\n0 3 * * * backup\n'
        expected = [
            {'name': 'SHELL', 'value': "'/bin/bash'"},
            {'name': 'PATH', 'value': '"/usr/local/bin:/usr/bin"'}
        ]
        result = jc.parsers.crontab.parse(data, raw=True, quiet=True)
        self.assertEqual(result['variables'], expected)


if __name__ == '__main__':
    unittest.main()
