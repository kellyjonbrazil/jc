import os
import json
import unittest
import jc.parsers.fstab

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/fstab.out'), 'r', encoding='utf-8') as f:
        centos_7_7_fstab = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/fstab.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_fstab = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/fstab.json'), 'r', encoding='utf-8') as f:
        centos_7_7_fstab_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/fstab.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_fstab_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/fstab-optional-fields.out'), 'r', encoding='utf-8') as f:
        generic_fstab_optional_fields = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/fstab-optional-fields.json'), 'r', encoding='utf-8') as f:
        generic_fstab_optional_fields_json = json.loads(f.read())


    def test_fstab_nodata(self):
        """
        Test 'cat /etc/fstab' with no data
        """
        self.assertEqual(jc.parsers.fstab.parse('', quiet=True), [])

    def test_fstab_whitespace_only_line(self):
        """
        Test 'cat /etc/fstab' with a whitespace-only line
        """
        data = ' \t \n/dev/sda1 / ext4 defaults 0 1\n'
        expected = [{'fs_spec': '/dev/sda1', 'fs_file': '/', 'fs_vfstype': 'ext4', 'fs_mntops': 'defaults', 'fs_freq': 0, 'fs_passno': 1}]
        self.assertEqual(jc.parsers.fstab.parse(data, quiet=True), expected)

    def test_fstab_centos_7_7(self):
        """
        Test 'cat /etc/fstab' on Centos 7.7
        """
        self.assertEqual(jc.parsers.fstab.parse(self.centos_7_7_fstab, quiet=True), self.centos_7_7_fstab_json)

    def test_fstab_ubuntu_18_4(self):
        """
        Test 'cat /etc/fstab' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.fstab.parse(self.ubuntu_18_4_fstab, quiet=True), self.ubuntu_18_4_fstab_json)

    def test_fstab_optional_fields(self):
        """
        Test 'cat /etc/fstab' with the optional fs_freq and fs_passno fields omitted
        """
        self.assertEqual(jc.parsers.fstab.parse(self.generic_fstab_optional_fields, quiet=True),
                         self.generic_fstab_optional_fields_json)


if __name__ == '__main__':
    unittest.main()
