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


if __name__ == '__main__':
    unittest.main()
