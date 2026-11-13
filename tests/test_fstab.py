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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/fstab-octal-escapes.out'), 'r', encoding='utf-8') as f:
        generic_fstab_octal_escapes = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/fstab-octal-escapes.json'), 'r', encoding='utf-8') as f:
        generic_fstab_octal_escapes_json = json.loads(f.read())


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


    def test_fstab_line_separator(self):
        """
        Test 'fstab' with a line-break character other than LF inside a field
        """
        data = '# disabled:\x0ctmpfs /tmp tmpfs rw,noexec,nosuid,nodev 0 0\n/dev/sda1 / ext4 defaults 0 1\n'
        expected = [{'fs_spec': '/dev/sda1', 'fs_file': '/', 'fs_vfstype': 'ext4', 'fs_mntops': 'defaults', 'fs_freq': 0, 'fs_passno': 1}]
        self.assertEqual(jc.parsers.fstab.parse(data, quiet=True), expected)


    def test_fstab_other_whitespace_in_field(self):
        """
        Test 'fstab' splits fields on space and tab only
        """
        data = 'tmpfs\xa0/mnt/scratch\xa0tmpfs\xa0rw,noexec,nosuid,nodev\xa00\xa00 /usr/local/bin tmpfs rw,exec,suid,dev 0 0\n'
        expected = [{'fs_spec': 'tmpfs\xa0/mnt/scratch\xa0tmpfs\xa0rw,noexec,nosuid,nodev\xa00\xa00', 'fs_file': '/usr/local/bin', 'fs_vfstype': 'tmpfs', 'fs_mntops': 'rw,exec,suid,dev', 'fs_freq': 0, 'fs_passno': 0}]
        self.assertEqual(jc.parsers.fstab.parse(data, quiet=True), expected)

    def test_fstab_other_whitespace_before_hash(self):
        """
        Test 'fstab' only skips leading space and tab before a comment character
        """
        data = '\xa0#tmpfs /usr/local/bin tmpfs rw,exec,suid,dev 0 0\n \t# comment\n'
        expected = [{'fs_spec': '\xa0#tmpfs', 'fs_file': '/usr/local/bin', 'fs_vfstype': 'tmpfs', 'fs_mntops': 'rw,exec,suid,dev', 'fs_freq': 0, 'fs_passno': 0}]
        self.assertEqual(jc.parsers.fstab.parse(data, quiet=True), expected)

    def test_fstab_octal_escapes(self):
        """
        Test 'fstab' with octal escapes in the first four fields
        """
        self.assertEqual(jc.parsers.fstab.parse(self.generic_fstab_octal_escapes, quiet=True),
                         self.generic_fstab_octal_escapes_json)

    def test_fstab_octal_escapes_raw(self):
        """
        Test 'fstab' decodes octal escapes in raw output
        """
        data = '//server/My\\040Share /mnt/my\\040disk e\\170t4 rw,\\145xec 1 2\n'
        expected = [{'fs_spec': '//server/My Share', 'fs_file': '/mnt/my disk', 'fs_vfstype': 'ext4', 'fs_mntops': 'rw,exec', 'fs_freq': '1', 'fs_passno': '2'}]
        self.assertEqual(jc.parsers.fstab.parse(data, raw=True, quiet=True), expected)

    def test_fstab_octal_escape_nul(self):
        """
        Test 'fstab' ends a field at a decoded NUL like libmount
        """
        data = '/dev/sdb1 /mnt/a\\000b ext4 defaults\\000,noexec 0 0\n'
        expected = [{'fs_spec': '/dev/sdb1', 'fs_file': '/mnt/a', 'fs_vfstype': 'ext4', 'fs_mntops': 'defaults', 'fs_freq': 0, 'fs_passno': 0}]
        self.assertEqual(jc.parsers.fstab.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
