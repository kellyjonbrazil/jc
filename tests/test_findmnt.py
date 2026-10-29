import os
import unittest
import json
from typing import Dict
from jc.parsers.findmnt import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/findmnt-spaces.out'), 'r', encoding='utf-8') as f:
        generic_findmnt_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/findmnt-spaces.json'), 'r', encoding='utf-8') as f:
        generic_findmnt_spaces_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/findmnt-quoted-and-escaped-commas.out'), 'r', encoding='utf-8') as f:
        generic_findmnt_quoted_and_escaped_commas = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/findmnt-quoted-and-escaped-commas.json'), 'r', encoding='utf-8') as f:
        generic_findmnt_quoted_and_escaped_commas_json = json.loads(f.read())

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'centos_7_7_findmnt': (
                'fixtures/centos-7.7/findmnt.out',
                'fixtures/centos-7.7/findmnt.json'),
            'centos_7_7_findmnt_a': (
                'fixtures/centos-7.7/findmnt-a.out',
                'fixtures/centos-7.7/findmnt-a.json'),
            'centos_7_7_findmnt_l': (
                'fixtures/centos-7.7/findmnt-l.out',
                'fixtures/centos-7.7/findmnt-l.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_findmnt_nodata(self):
        """
        Test 'findmnt' with no data
        """
        self.assertEqual(parse('', quiet=True), [])

    def test_findmnt_centos_7_7(self):
        """
        Test 'findmnt' on Centos 7.7
        """
        self.assertEqual(
            parse(self.f_in['centos_7_7_findmnt'], quiet=True),
            self.f_json['centos_7_7_findmnt']
        )

    def test_findmnt_a_centos_7_7(self):
        """
        Test 'findmnt -a' on Centos 7.7
        """
        self.assertEqual(
            parse(self.f_in['centos_7_7_findmnt_a'], quiet=True),
            self.f_json['centos_7_7_findmnt_a']
        )

    def test_findmnt_l_centos_7_7(self):
        """
        Test 'findmnt -l' on Centos 7.7
        """
        self.assertEqual(
            parse(self.f_in['centos_7_7_findmnt_l'], quiet=True),
            self.f_json['centos_7_7_findmnt_l']
        )


    def test_findmnt_spaces(self):
        """
        Test 'findmnt' with spaces in mount point names
        """
        self.assertEqual(
            parse(self.generic_findmnt_spaces, quiet=True),
            self.generic_findmnt_spaces_json
        )

    def test_findmnt_spaces_column_text(self):
        """
        Test 'findmnt -l' with a mount point name that contains text in the
        shape of the other columns
        """
        data = (
            'TARGET                      SOURCE    FSTYPE OPTIONS\n'
            '/                           /dev/sda2 ext4   rw,relatime\n'
            '/mnt/a /dev/sdb1 ext4 ro,x= tmpfs     tmpfs  rw,relatime,inode64\n'
        )
        result = parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]['target'], '/mnt/a /dev/sdb1 ext4 ro,x=')
        self.assertEqual(result[1]['source'], 'tmpfs')
        self.assertEqual(result[1]['fstype'], 'tmpfs')
        self.assertEqual(result[1]['options'], ['rw', 'relatime', 'inode64'])
        self.assertNotIn('kv_options', result[1])

    def test_findmnt_blank_options(self):
        """
        Test 'findmnt -o' output with a blank cell in the options column
        """
        data = (
            'SOURCE    TARGET   OPTIONS     FSTYPE\n'
            '/dev/sda2 /        rw,relatime ext4\n'
            'none      /mnt/x               autofs\n'
        )
        expected = [
            {'source': '/dev/sda2', 'target': '/', 'options': ['rw', 'relatime'], 'fstype': 'ext4'},
            {'source': 'none', 'target': '/mnt/x', 'options': None, 'fstype': 'autofs'}
        ]
        self.assertEqual(parse(data, quiet=True), expected)

    def test_findmnt_r(self):
        """
        Test 'findmnt -r' output, which escapes spaces and does not align
        the columns
        """
        data = (
            'TARGET SOURCE FSTYPE OPTIONS\n'
            '/ /dev/sda2 ext4 rw,relatime\n'
            '/media/My\\x20Passport /dev/sdb1 exfat rw,nosuid,uid=1000\n'
        )
        expected = [
            {'target': '/', 'source': '/dev/sda2', 'fstype': 'ext4', 'options': ['rw', 'relatime']},
            {'target': '/media/My\\x20Passport', 'source': '/dev/sdb1', 'fstype': 'exfat', 'options': ['rw', 'nosuid'], 'kv_options': {'uid': '1000'}}
        ]
        self.assertEqual(parse(data, quiet=True), expected)

    def test_findmnt_quoted_and_escaped_commas(self):
        """
        Test 'findmnt' with quoted and backslash-escaped commas in options
        """
        self.assertEqual(
            parse(self.generic_findmnt_quoted_and_escaped_commas, quiet=True),
            self.generic_findmnt_quoted_and_escaped_commas_json
        )

    def test_findmnt_single_space_header_with_spaces_in_values(self):
        """
        Test 'findmnt' aligned output whose header columns are one space apart and a value has spaces
        """
        data = (
            'FSTYPE TARGET SOURCE\n'
            'ext4   /a b   /dev/sda1\n'
            'xfs    /      /dev/sdb1\n'
        )
        self.assertEqual(parse(data, quiet=True), [
            {'fstype': 'ext4', 'target': '/a b', 'source': '/dev/sda1'},
            {'fstype': 'xfs', 'target': '/', 'source': '/dev/sdb1'}
        ])

        # -r output escapes the spaces
        data = (
            'TARGET SOURCE FSTYPE\n'
            '/a\\x20b /dev/sda1 ext4\n'
            '/ /dev/sdb1 xfs\n'
        )
        self.assertEqual(parse(data, quiet=True), [
            {'target': '/a\\x20b', 'source': '/dev/sda1', 'fstype': 'ext4'},
            {'target': '/', 'source': '/dev/sdb1', 'fstype': 'xfs'}
        ])


if __name__ == '__main__':
    unittest.main()
