import os
import json
import unittest
import jc.parsers.lsattr

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/lsattr-error.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_lsattr_error = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/lsattr-R.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_lsattr_R = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/lsattr.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_lsattr = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/lsattr-error.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_lsattr_error_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/lsattr-R.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_lsattr_R_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/lsattr.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_lsattr_json = json.loads(f.read())

    def test_lsattr_nodata(self):
        """
        Test 'lsattr' with no data
        """
        self.assertEqual(jc.parsers.lsattr.parse('', quiet=True), [])

    def test_lsattr_error(self):
        """
        Test 'lsattr' with permission error
        """
        self.assertEqual(jc.parsers.lsattr.parse(self.ubuntu_20_4_lsattr_error, quiet=True), self.ubuntu_20_4_lsattr_error_json)

    def test_lsattr_R_ubuntu_20_4(self):
        """
        Test 'sudo lsattr -R' on Ubuntu 20.4
        """
        self.assertEqual(jc.parsers.lsattr.parse(self.ubuntu_20_4_lsattr_R, quiet=True), self.ubuntu_20_4_lsattr_R_json)

    def test_lsattr_ubuntu_20_4(self):
        """
        Test 'sudo lsattr' on Ubuntu 20.4
        """
        self.assertEqual(jc.parsers.lsattr.parse(self.ubuntu_20_4_lsattr, quiet=True), self.ubuntu_20_4_lsattr_json)

if __name__ == '__main__':
    unittest.main()
