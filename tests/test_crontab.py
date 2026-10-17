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


if __name__ == '__main__':
    unittest.main()
