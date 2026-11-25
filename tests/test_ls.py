import os
import json
import unittest
import jc.parsers.ls

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ls = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-al.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_al = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-al.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_al = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls-al.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ls_al = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-al.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_al = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alh.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_alh = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alh.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_alh = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls-alh.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ls_alh = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alh.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_alh = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-R.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_R = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-R.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_R = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-R.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_R = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alR.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_alR = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alR.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_alR = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alR.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_alR = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-glob.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_glob = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-glob.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_glob = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-glob.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_glob = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-R-newlines.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_R_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-R-newlines.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_R_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-R-newlines.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_R_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-l-newlines.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_l_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-l-newlines.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_l_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-l-newlines.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_l_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-lR-newlines.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_lR_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-lR-newlines.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_lR_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-lR-newlines.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_lR_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-newlines.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-newlines.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-newlines.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_newlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-lR-empty-folder.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_lR_empty_folder = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-l-iso.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_l_iso = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-devices.out'), 'r', encoding='utf-8') as f:
        ls_l_devices = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-long-iso.out'), 'r', encoding='utf-8') as f:
        ls_l_long_iso = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-entry-like-dirnames.out'), 'r', encoding='utf-8') as f:
        ls_l_entry_like_dirnames = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-newline-structure-like-names.out'), 'r', encoding='utf-8') as f:
        ls_l_newline_structure_like_names = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-entry-like-names.out'), 'r', encoding='utf-8') as f:
        ls_entry_like_names = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-no-total.out'), 'r', encoding='utf-8') as f:
        ls_l_no_total = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ls_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-al.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_al_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-al.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_al_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls-al.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ls_al_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-al.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_al_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alh.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_alh_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alh.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_alh_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls-alh.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ls_alh_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alh.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_alh_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-R.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_R_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-R.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_R_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-R.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_R_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alR.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_alR_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alR.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_alR_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alR.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_alR_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-glob.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_glob_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-glob.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_glob_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-glob.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_glob_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-R-newlines.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_R_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-R-newlines.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_R_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-R-newlines.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_R_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-l-newlines.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_l_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-l-newlines.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_l_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-l-newlines.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_l_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-lR-newlines.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_lR_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-lR-newlines.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_lR_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-lR-newlines.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_lR_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-newlines.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-newlines.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-newlines.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_newlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-lR-empty-folder.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_lR_empty_folder_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-l-iso.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_l_iso_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-devices.json'), 'r', encoding='utf-8') as f:
        ls_l_devices_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-long-iso.json'), 'r', encoding='utf-8') as f:
        ls_l_long_iso_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-entry-like-dirnames.json'), 'r', encoding='utf-8') as f:
        ls_l_entry_like_dirnames_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-newline-structure-like-names.json'), 'r', encoding='utf-8') as f:
        ls_l_newline_structure_like_names_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-entry-like-names.json'), 'r', encoding='utf-8') as f:
        ls_entry_like_names_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-no-total.json'), 'r', encoding='utf-8') as f:
        ls_l_no_total_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-lR-spaces.out'), 'r', encoding='utf-8') as f:
        ls_lR_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-spaces-long-iso.out'), 'r', encoding='utf-8') as f:
        ls_l_spaces_long_iso = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-lR-spaces.json'), 'r', encoding='utf-8') as f:
        ls_lR_spaces_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-spaces-long-iso.json'), 'r', encoding='utf-8') as f:
        ls_l_spaces_long_iso_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-lR-no-stat.out'), 'r', encoding='utf-8') as f:
        ls_lR_no_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-no-stat-long-iso.out'), 'r', encoding='utf-8') as f:
        ls_l_no_stat_long_iso = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-lR-no-stat.json'), 'r', encoding='utf-8') as f:
        ls_lR_no_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-no-stat-long-iso.json'), 'r', encoding='utf-8') as f:
        ls_l_no_stat_long_iso_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-arrows.out'), 'r', encoding='utf-8') as f:
        ls_l_arrows = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-linux-l-arrows.json'), 'r', encoding='utf-8') as f:
        ls_l_arrows_json = json.loads(f.read())

    def test_ls_line_separators(self):
        """
        Test 'ls' with line-break characters other than LF in a file name
        """
        data = 'total 20\n-rw-r--r--.   1 root root    7 Aug 15 10:53 a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\nlrwxrwxrwx.   1 root root    7 Aug 15 10:53 bin -> usr/bin\n'
        result = jc.parsers.ls.parse(data, quiet=True)
        self.assertEqual(result[0]['filename'], 'a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[1]['link_to'], 'usr/bin')

    def test_ls_empty_dir(self):
        """
        Test plain 'ls' on an empty directory
        """
        self.assertEqual(jc.parsers.ls.parse('', quiet=True), [])

    def test_ls_centos_7_7(self):
        """
        Test plain 'ls /' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls, quiet=True), self.centos_7_7_ls_json)

    def test_ls_ubuntu_18_4(self):
        """
        Test plain 'ls /' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls, quiet=True), self.ubuntu_18_4_ls_json)

    def test_ls_osx_10_11_6(self):
        """
        Test plain 'ls /' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_11_6_ls, quiet=True), self.osx_10_11_6_ls_json)

    def test_ls_osx_10_14_6(self):
        """
        Test plain 'ls /' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls, quiet=True), self.osx_10_14_6_ls_json)

    def test_ls_al_centos_7_7(self):
        """
        Test 'ls -al /' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_al, quiet=True), self.centos_7_7_ls_al_json)

    def test_ls_al_ubuntu_18_4(self):
        """
        Test 'ls -al /' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_al, quiet=True), self.ubuntu_18_4_ls_al_json)

    def test_ls_al_osx_10_11_6(self):
        """
        Test 'ls -al /' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_11_6_ls_al, quiet=True), self.osx_10_11_6_ls_al_json)

    def test_ls_al_osx_10_14_6(self):
        """
        Test 'ls -al /' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_al, quiet=True), self.osx_10_14_6_ls_al_json)

    def test_ls_alh_centos_7_7(self):
        """
        Test 'ls -alh /' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_alh, quiet=True), self.centos_7_7_ls_alh_json)

    def test_ls_alh_ubuntu_18_4(self):
        """
        Test 'ls -alh /' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_alh, quiet=True), self.ubuntu_18_4_ls_alh_json)

    def test_ls_alh_osx_10_11_6(self):
        """
        Test 'ls -alh /' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_11_6_ls_alh, quiet=True), self.osx_10_11_6_ls_alh_json)

    def test_ls_alh_osx_10_14_6(self):
        """
        Test 'ls -alh /' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_alh, quiet=True), self.osx_10_14_6_ls_alh_json)

    def test_ls_R_centos_7_7(self):
        """
        Test 'ls -R /usr' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_R, quiet=True), self.centos_7_7_ls_R_json)

    def test_ls_R_ubuntu_18_4(self):
        """
        Test 'ls -R /usr' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_R, quiet=True), self.ubuntu_18_4_ls_R_json)

    def test_ls_R_osx_10_14_6(self):
        """
        Test 'ls -R /usr' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_R, quiet=True), self.osx_10_14_6_ls_R_json)

    def test_ls_alR_centos_7_7(self):
        """
        Test 'ls -alR /usr' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_alR, quiet=True), self.centos_7_7_ls_alR_json)

    def test_ls_alR_ubuntu_18_4(self):
        """
        Test 'ls -alR /usr' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_alR, quiet=True), self.ubuntu_18_4_ls_alR_json)

    def test_ls_alR_osx_10_14_6(self):
        """
        Test 'ls -alR /usr' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_alR, quiet=True), self.osx_10_14_6_ls_alR_json)

    def test_ls_glob_centos_7_7(self):
        """
        Test 'ls /usr/*' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_glob, quiet=True), self.centos_7_7_ls_glob_json)

    def test_ls_glob_ubuntu_18_4(self):
        """
        Test 'ls /usr/*' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_glob, quiet=True), self.ubuntu_18_4_ls_glob_json)

    def test_ls_glob_osx_10_14_6(self):
        """
        Test 'ls /usr/*' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_glob, quiet=True), self.osx_10_14_6_ls_glob_json)

    def test_ls_R_newlines_centos_7_7(self):
        """
        Test 'ls -R' for filenames with newline characters on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_R_newlines, quiet=True), self.centos_7_7_ls_R_newlines_json)

    def test_ls_R_newlines_ubuntu_18_4(self):
        """
        Test 'ls -R' for filenames with newline characters on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_R_newlines, quiet=True), self.ubuntu_18_4_ls_R_newlines_json)

    def test_ls_R_newlines_osx_10_14_6(self):
        """
        Test 'ls -R' for filenames with newline characters on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_R_newlines, quiet=True), self.osx_10_14_6_ls_R_newlines_json)

    def test_ls_l_newlines_centos_7_7(self):
        """
        Test 'ls -l' for filenames with newline characters on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_l_newlines, quiet=True), self.centos_7_7_ls_l_newlines_json)

    def test_ls_l_newlines_ubuntu_18_4(self):
        """
        Test 'ls -l' for filenames with newline characters on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_l_newlines, quiet=True), self.ubuntu_18_4_ls_l_newlines_json)

    def test_ls_l_newlines_osx_10_14_6(self):
        """
        Test 'ls -l' for filenames with newline characters on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_l_newlines, quiet=True), self.osx_10_14_6_ls_l_newlines_json)

    def test_ls_lR_newlines_centos_7_7(self):
        """
        Test 'ls -lR' for filenames with newline characters on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_lR_newlines, quiet=True), self.centos_7_7_ls_lR_newlines_json)

    def test_ls_lR_newlines_ubuntu_18_4(self):
        """
        Test 'ls -lR' for filenames with newline characters on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_lR_newlines, quiet=True), self.ubuntu_18_4_ls_lR_newlines_json)

    def test_ls_lR_newlines_osx_10_14_6(self):
        """
        Test 'ls -lR' for filenames with newline characters on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_lR_newlines, quiet=True), self.osx_10_14_6_ls_lR_newlines_json)

    def test_ls_newlines_centos_7_7(self):
        """
        Test 'ls' for filenames with newline characters on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_newlines, quiet=True), self.centos_7_7_ls_newlines_json)

    def test_ls_newlines_ubuntu_18_4(self):
        """
        Test 'ls' for filenames with newline characters on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_newlines, quiet=True), self.ubuntu_18_4_ls_newlines_json)

    def test_ls_newlines_osx_10_14_6(self):
        """
        Test 'ls' for filenames with newline characters on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_newlines, quiet=True), self.osx_10_14_6_ls_newlines_json)

    def test_ls_lR_empty_folder_osx_10_14_6(self):
        """
        Test 'ls -lR' for empty directories on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ls.parse(self.osx_10_14_6_ls_lR_empty_folder, quiet=True), self.osx_10_14_6_ls_lR_empty_folder_json)

    def test_ls_l_iso_ubuntu_18_4(self):
        """
        Test 'ls -l --time-style=full-iso' for files with convertible dates on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_l_iso, quiet=True), self.ubuntu_18_4_ls_l_iso_json)

    def test_ls_l_devices(self):
        """
        Test 'ls -l' on block and character device entries (e.g. /dev),
        which report major/minor numbers instead of a size. Also
        includes a regular file to confirm the two forms coexist in one
        listing.
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_l_devices, quiet=True), self.ls_l_devices_json)

    def test_ls_l_long_iso(self):
        """
        Test 'ls -l --time-style=long-iso', whose date field is 2 tokens
        wide instead of the default/full-iso 3. Includes a symlink to
        confirm link_to parsing still works with the narrower date width.
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_l_long_iso, quiet=True), self.ls_l_long_iso_json)

    def test_ls_l_entry_like_dirnames(self):
        """
        Test 'ls -l -- *' where some directory names look like 'ls -l'
        entry lines or a 'total' line, and a filename ends in ':'. The
        'name:' headers are only recognized by position (first line or
        after a blank line, and followed by a 'total' line).
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_l_entry_like_dirnames, quiet=True), self.ls_l_entry_like_dirnames_json)

    def test_ls_l_newline_structure_like_names(self):
        """
        Test 'ls -l' with filenames containing a newline followed by text
        that looks like a 'total' line or a 'name:' header. These are
        part of the filename, not structure lines.
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_l_newline_structure_like_names, quiet=True), self.ls_l_newline_structure_like_names_json)

    def test_ls_l_total_only(self):
        """
        Test 'ls -l' on an empty directory (only a 'total 0' line)
        """
        self.assertEqual(jc.parsers.ls.parse('total 0\n', quiet=True), [])

    def test_ls_entry_like_names(self):
        """
        Test plain 'ls' where the first filenames look like 'ls -l' entry
        lines. The output has no 'total' line and not every line looks
        like an 'ls -l' entry, so it is parsed as plain 'ls' output.
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_entry_like_names, quiet=True), self.ls_entry_like_names_json)

    def test_ls_entry_like_permission_name(self):
        """
        Test plain 'ls' where the first filename is only a permission string
        """
        self.assertEqual(jc.parsers.ls.parse('----------\nbin\netc\n', quiet=True), [{'filename': '----------'}, {'filename': 'bin'}, {'filename': 'etc'}])

    def test_ls_l_no_total(self):
        """
        Test 'ls -l file1 file2 dir' which has no leading 'total' line.
        Every entry looks like an 'ls -l' entry, so it is parsed as
        'ls -l' output. Includes a filename that looks like an entry line.
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_l_no_total, quiet=True), self.ls_l_no_total_json)

    def test_ls_l_filename_with_newlines_sections(self):
        """
        Test 'ls -l' filenames with newlines across multiple sections
        """
        data = '/dir:\ntotal 8\n-rw-r--r-- 1 u g 0 Jan  1 10:00 a\nb\nc\n-rw-r--r-- 1 u g 0 Jan  1 10:00 d\n\n/dir2:\ntotal 0\n-rw-r--r-- 1 u g 0 Jan  1 10:00 e\nf\n'
        result = jc.parsers.ls.parse(data, raw=True, quiet=True)
        self.assertEqual([r['filename'] for r in result], ['a\nb\nc', 'd', 'e\nf'])
        self.assertEqual([r['parent'] for r in result], ['/dir', '/dir', '/dir2'])

    def test_ls_lR_empty_folders_osx_layout(self):
        """
        Test macOS 'ls -lR' layout with several empty directories in a row (no 'total' lines)
        """
        data = 'total 8\ndrwxr-xr-x  2 u  staff   64 Jan  3 14:46 a\ndrwxr-xr-x  2 u  staff   64 Jan  3 14:46 b\n-rw-r--r--  1 u  staff  400 Jan  3 14:46 id_rsa.pub\n\n./a:\n\n./b:\n\n./c:\ntotal 8\n-rw-r--r--  1 u  staff  12 Jan  3 14:46 notes\nmore\n\n./d:\n'
        result = jc.parsers.ls.parse(data, raw=True, quiet=True)
        self.assertEqual([r['filename'] for r in result], ['a', 'b', 'id_rsa.pub', 'notes\nmore'])
        self.assertEqual([r.get('parent') for r in result], [None, None, None, './c'])

    def test_ls_lR_spaces(self):
        """
        Test 'ls -lR' with filenames and a directory name that start or end with whitespace
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_lR_spaces, quiet=True), self.ls_lR_spaces_json)

    def test_ls_lR_spaces_names(self):
        """
        Test that leading, trailing, repeated, and whitespace-only filenames are kept as printed
        """
        result = jc.parsers.ls.parse(self.ls_lR_spaces, raw=True, quiet=True)
        self.assertEqual([r['filename'] for r in result], ['  ', ' lead', ' sub ', 'co:lon', 'plain', 'trail ', 'two  sp', '\xa0nbsp', '\xfcn\xef', 'x '])
        self.assertEqual(result[-1]['parent'], './ sub ')
        self.assertEqual(result[0]['date'], 'Oct 1 12:00')

    def test_ls_l_spaces_long_iso(self):
        """
        Test 'ls -l --time-style=long-iso' with filenames that start or end with whitespace
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_l_spaces_long_iso, quiet=True), self.ls_l_spaces_long_iso_json)

    def test_ls_l_device_leading_space(self):
        """
        Test a device entry whose filename starts with a space
        """
        result = jc.parsers.ls.parse('crw-rw-rw- 1 root root 1, 3 Sep 16 08:00  null\n', quiet=True)
        self.assertEqual(result, [{'filename': ' null', 'flags': 'crw-rw-rw-', 'links': 1, 'owner': 'root', 'group': 'root', 'major_number': 1, 'minor_number': 3, 'date': 'Sep 16 08:00'}])

    def test_ls_lR_no_stat(self):
        """
        Test 'ls -lR' with entries in a directory that can be read but not searched
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_lR_no_stat, quiet=True), self.ls_lR_no_stat_json)

    def test_ls_lR_no_stat_names(self):
        """
        Test that entries ls cannot stat are separate entries with null fields
        """
        result = jc.parsers.ls.parse(self.ls_lR_no_stat, raw=True, quiet=True)
        self.assertEqual([(r['parent'], r['filename']) for r in result], [('.', 'locked'), ('.', 'open'), ('./locked', 'afile'), ('./locked', 'alink'), ('./locked', 'fifo'), ('./locked', 'sub'), ('./locked', 'two  sp'), ('./open', 'zfile')])
        self.assertEqual(result[3], {'filename': 'alink', 'parent': './locked', 'flags': 'l?????????', 'links': None, 'owner': None, 'group': None, 'size': None, 'date': None})

    def test_ls_l_no_stat_long_iso(self):
        """
        Test 'ls -l --time-style=long-iso' where the first entries cannot be stat'ed
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_l_no_stat_long_iso, quiet=True), self.ls_l_no_stat_long_iso_json)

    def test_ls_l_no_stat_device(self):
        """
        Test a character device entry that cannot be stat'ed
        """
        result = jc.parsers.ls.parse('c????????? ? ? ? ?            ? tty0\n', quiet=True)
        self.assertEqual(result, [{'filename': 'tty0', 'flags': 'c?????????', 'links': None, 'owner': None, 'group': None, 'size': None, 'date': None}])

    def test_ls_l_arrows(self):
        """
        Test 'ls -l' with ' -> ' in the names of files, directories, and symbolic links
        """
        self.assertEqual(jc.parsers.ls.parse(self.ls_l_arrows, quiet=True), self.ls_l_arrows_json)

    def test_ls_l_arrows_link_to(self):
        """
        Test that only symbolic links get link_to, split at the first ' -> '
        """
        result = jc.parsers.ls.parse(self.ls_l_arrows, raw=True, quiet=True)
        self.assertEqual([(r['filename'], r.get('link_to')) for r in result], [('arrowtarget', 'a -> b'), ('deploy.key', None), ('deploy.key -> old', None), ('dir -> y', None), ('lnk', 'x -> target'), ('normallnk', 'tgt')])
        self.assertEqual(result[2]['flags'], '-rw-r--r--.')


if __name__ == '__main__':
    unittest.main()
