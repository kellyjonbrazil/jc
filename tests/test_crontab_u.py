import os
import json
import unittest
import jc.parsers.crontab_u

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/crontab-u.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_crontab_u = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab-u.out'), 'r', encoding='utf-8') as f:
        centos_7_7_crontab_u = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/crontab-u.out'), 'r', encoding='utf-8') as f:
        debian10_crontab_u = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-u-no-normal-entries.out'), 'r', encoding='utf-8') as f:
        generic_crontab_u_no_normal_entries = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-u-var-fix.out'), 'r', encoding='utf-8') as f:
        generic_crontab_u_var_fix = f.read()

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-u-whitespace-lines.out'
    ), 'r', encoding='utf-8') as f:
        whitespace_lines = f.read()

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-u-whitespace-only.out'
    ), 'r', encoding='utf-8') as f:
        whitespace_only = f.read()

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-u-whitespace-comments.out'
    ), 'r', encoding='utf-8') as f:
        whitespace_comments = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/crontab-u.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_crontab_u_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab-u.json'), 'r', encoding='utf-8') as f:
        centos_7_7_crontab_u_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/crontab-u.json'), 'r', encoding='utf-8') as f:
        debian10_crontab_u_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-u-no-normal-entries.json'), 'r', encoding='utf-8') as f:
        generic_crontab_u_no_normal_entries_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-u-var-fix.json'), 'r', encoding='utf-8') as f:
        generic_crontab_u_var_fix_json = json.loads(f.read())

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-u-whitespace-lines.json'
    ), 'r', encoding='utf-8') as f:
        whitespace_lines_json = json.loads(f.read())

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-u-whitespace-lines-raw.json'
    ), 'r', encoding='utf-8') as f:
        whitespace_lines_raw_json = json.loads(f.read())

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-u-whitespace-only.json'
    ), 'r', encoding='utf-8') as f:
        whitespace_only_json = json.loads(f.read())

    with open(os.path.join(
        THIS_DIR, os.pardir,
        'tests/fixtures/generic/crontab-u-whitespace-comments.json'
    ), 'r', encoding='utf-8') as f:
        whitespace_comments_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-u-job-with-equals.out'), 'r', encoding='utf-8') as f:
        generic_crontab_u_job_with_equals = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/crontab-u-job-with-equals.json'), 'r', encoding='utf-8') as f:
        generic_crontab_u_job_with_equals_json = json.loads(f.read())

    def test_crontab_u_nodata(self):
        """
        Test 'crontab' with no data (has a user field)
        """
        self.assertEqual(jc.parsers.crontab_u.parse('', quiet=True), {})

    def test_crontab_u_ubuntu_18_4(self):
        """
        Test 'crontab' on Ubuntu 18.4 (has a user field)
        """
        self.assertEqual(jc.parsers.crontab_u.parse(self.ubuntu_18_4_crontab_u, quiet=True), self.ubuntu_18_4_crontab_u_json)

    def test_crontab_u_centos_7_7(self):
        """
        Test 'crontab' on Centos 7.7 (has a user field)
        """
        self.assertEqual(jc.parsers.crontab_u.parse(self.centos_7_7_crontab_u, quiet=True), self.centos_7_7_crontab_u_json)

    def test_crontab_u_debian10(self):
        """
        Test 'crontab' on Debian10 (has a user field)
        """
        self.assertEqual(jc.parsers.crontab_u.parse(self.debian10_crontab_u, quiet=True), self.debian10_crontab_u_json)

    def test_crontab_u_no_normal_entries(self):
        """
        Test 'crontab' with no normal entries - only shortcut entries (has a user field)
        """
        self.assertEqual(jc.parsers.crontab_u.parse(self.generic_crontab_u_no_normal_entries, quiet=True), self.generic_crontab_u_no_normal_entries_json)

    def test_crontab_u_var_fix(self):
        """
        Test 'crontab' with wildcard schedule should not generate variables from command line section
        """
        self.assertEqual(jc.parsers.crontab_u.parse(self.generic_crontab_u_var_fix, quiet=True), self.generic_crontab_u_var_fix_json)

    def test_crontab_u_nodata_raw(self):
        """
        Test 'crontab-u' with no data in raw mode
        """
        self.assertEqual(
            jc.parsers.crontab_u.parse('', raw=True, quiet=True), {}
        )

    def test_crontab_u_whitespace_lines(self):
        """
        Test 'crontab-u' with whitespace-only lines
        """
        self.assertEqual(
            jc.parsers.crontab_u.parse(self.whitespace_lines, quiet=True),
            self.whitespace_lines_json
        )

    def test_crontab_u_whitespace_lines_raw(self):
        """
        Test 'crontab-u' with whitespace-only lines in raw mode
        """
        self.assertEqual(
            jc.parsers.crontab_u.parse(
                self.whitespace_lines, raw=True, quiet=True
            ),
            self.whitespace_lines_raw_json
        )

    def test_crontab_u_whitespace_only(self):
        """
        Test 'crontab-u' with whitespace-only input
        """
        self.assertEqual(
            jc.parsers.crontab_u.parse(self.whitespace_only, quiet=True),
            self.whitespace_only_json
        )

    def test_crontab_u_whitespace_only_raw(self):
        """
        Test 'crontab-u' with whitespace-only input in raw mode
        """
        self.assertEqual(
            jc.parsers.crontab_u.parse(
                self.whitespace_only, raw=True, quiet=True
            ),
            self.whitespace_only_json
        )

    def test_crontab_u_whitespace_comments(self):
        """
        Test 'crontab-u' with whitespace-only lines and comments
        """
        self.assertEqual(
            jc.parsers.crontab_u.parse(self.whitespace_comments, quiet=True),
            self.whitespace_comments_json
        )

    def test_crontab_u_whitespace_comments_raw(self):
        """
        Test 'crontab-u' with whitespace-only lines and comments in raw mode
        """
        self.assertEqual(
            jc.parsers.crontab_u.parse(
                self.whitespace_comments, raw=True, quiet=True
            ),
            self.whitespace_comments_json
        )


    def test_crontab_u_line_separator(self):
        """
        Test 'crontab_u' with a line-break character other than LF inside a field
        """
        data = '0 3 * * * root /usr/bin/backup;\x0c#$(/usr/bin/other)\n'
        result = jc.parsers.crontab_u.parse(data, quiet=True)
        self.assertEqual(len(result['schedule']), 1)
        self.assertEqual(result['schedule'][0]['user'], 'root')
        self.assertEqual(result['schedule'][0]['command'], '/usr/bin/backup;\x0c#$(/usr/bin/other)')

    def test_crontab_u_mixed_lines_order(self):
        """
        Test 'crontab_u' with comments, variables, shortcuts and entries interleaved
        """
        data = '# c1\nA=1\n* * * * * root cmd1\n@daily root x\nB=2\n# c2\n@reboot root y z\n0 1 * * * u cmd2\n'
        result = jc.parsers.crontab_u.parse(data, raw=True, quiet=True)
        self.assertEqual(result['variables'], [{'name': 'B', 'value': '2'}, {'name': 'A', 'value': '1'}])
        self.assertEqual([x['command'] for x in result['schedule']], ['cmd1', 'cmd2', 'y z', 'x'])
        self.assertEqual([x['user'] for x in result['schedule']], ['root', 'u', 'root', 'root'])

    def test_crontab_u_job_with_equals(self):
        """
        Test 'crontab' with user, with job lines that contain '=' and do not start with a digit
        """
        self.assertEqual(jc.parsers.crontab_u.parse(self.generic_crontab_u_job_with_equals, quiet=True), self.generic_crontab_u_job_with_equals_json)

    def test_crontab_u_quoted_variable_values(self):
        """
        Test 'crontab' with user, with quoted variable values
        """
        data = ('PATH="/usr/local/bin:/usr/bin"\n'
                "SHELL = '/bin/bash'\n"
                'MAILTO=""\n'
                'A="b\'\n'
                'B=c "d"\n'
                'C="\n'
                'D=""e""\n'
                '"NAME"=value\n'
                '0 3 * * * root backup\n')
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
        result = jc.parsers.crontab_u.parse(data, quiet=True)
        self.assertEqual(result['variables'], expected)
        self.assertEqual(result['schedule'][0]['command'], 'backup')

    def test_crontab_u_quoted_variable_values_raw(self):
        """
        Test 'crontab' with user, with quoted variable values and raw output
        """
        data = 'PATH="/usr/local/bin:/usr/bin"\nSHELL=\'/bin/bash\'\n0 3 * * * root backup\n'
        expected = [
            {'name': 'SHELL', 'value': "'/bin/bash'"},
            {'name': 'PATH', 'value': '"/usr/local/bin:/usr/bin"'}
        ]
        result = jc.parsers.crontab_u.parse(data, raw=True, quiet=True)
        self.assertEqual(result['variables'], expected)


if __name__ == '__main__':
    unittest.main()
