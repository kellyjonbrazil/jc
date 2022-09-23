import os
import json
import unittest
import jc.parsers.dpkg_l

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dpkg-l.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dpkg_l = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dpkg-l-columns500.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dpkg_l_columns500 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dpkg-l-codes.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dpkg_l_codes = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dpkg-l.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dpkg_l_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dpkg-l-columns500.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dpkg_l_columns500_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dpkg-l-codes.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dpkg_l_codes_json = json.loads(f.read())


    def test_dpkg_l_nodata(self):
        """
        Test plain 'dpkg_l' with no data
        """
        self.assertEqual(jc.parsers.dpkg_l.parse('', quiet=True), [])

    def test_dpkg_l_ubuntu_18_4(self):
        """
        Test plain 'dpkg -l' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dpkg_l.parse(self.ubuntu_18_4_dpkg_l, quiet=True), self.ubuntu_18_4_dpkg_l_json)

    def test_dpkg_l_columns500_ubuntu_18_4(self):
        """
        Test 'dpkg -l' on Ubuntu 18.4 with COLUMNS=500 set
        """
        self.assertEqual(jc.parsers.dpkg_l.parse(self.ubuntu_18_4_dpkg_l_columns500, quiet=True), self.ubuntu_18_4_dpkg_l_columns500_json)

    def test_dpkg_l_codes_ubuntu_18_4(self):
        """
        Test 'dpkg -l' on Ubuntu 18.4 with multiple codes set
        """
        self.assertEqual(jc.parsers.dpkg_l.parse(self.ubuntu_18_4_dpkg_l_codes, quiet=True), self.ubuntu_18_4_dpkg_l_codes_json)


if __name__ == '__main__':
    unittest.main()
