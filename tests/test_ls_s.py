import os
import json
import unittest
from jc.exceptions import ParseError
import jc.parsers.ls_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat ls-al.out | jc --ls-s | jello -c > ls-al-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls = f.read()

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alR.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_alR = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alR.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_alR = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alR.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_alR = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-lR-empty-folder.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_lR_empty_folder = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-l-iso.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_l_iso = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-l-devices.out'), 'r', encoding='utf-8') as f:
        ls_l_devices = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-l-long-iso.out'), 'r', encoding='utf-8') as f:
        ls_l_long_iso = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-l-entry-like-dirnames.out'), 'r', encoding='utf-8') as f:
        ls_l_entry_like_dirnames = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-l-newline-structure-like-names.out'), 'r', encoding='utf-8') as f:
        ls_l_newline_structure_like_names = f.read()

    # output

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-al-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_al_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-al-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_al_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-al-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_al_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alh-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_alh_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alh-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_alh_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alh-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_alh_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alR-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ls_alR_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alR-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_alR_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alR-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_alR_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-lR-empty-folder-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ls_lR_empty_folder_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-l-iso-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ls_l_iso_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-l-devices-streaming.json'), 'r', encoding='utf-8') as f:
        ls_l_devices_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-l-long-iso-streaming.json'), 'r', encoding='utf-8') as f:
        ls_l_long_iso_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ls-l-entry-like-dirnames-streaming.json'), 'r', encoding='utf-8') as f:
        ls_l_entry_like_dirnames_streaming_json = json.loads(f.read())


    def test_ls_s_empty_dir(self):
        """
        Test plain 'ls' on an empty directory
        """
        self.assertEqual(list(jc.parsers.ls_s.parse([], quiet=True)), [])

    def test_ls_s_centos_7_7_raise_exception(self):
        """
        Test plain 'ls /' on Centos 7.7 (raises ParseError)
        """
        g = jc.parsers.ls_s.parse(self.centos_7_7_ls.splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_ls_s_al_centos_7_7(self):
        """
        Test 'ls -al /' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.centos_7_7_ls_al.splitlines(), quiet=True)), self.centos_7_7_ls_al_streaming_json)

    def test_ls_s_al_ubuntu_18_4(self):
        """
        Test 'ls -al /' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.ubuntu_18_4_ls_al.splitlines(), quiet=True)), self.ubuntu_18_4_ls_al_streaming_json)

    def test_ls_s_al_osx_10_14_6(self):
        """
        Test 'ls -al /' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.osx_10_14_6_ls_al.splitlines(), quiet=True)), self.osx_10_14_6_ls_al_streaming_json)

    def test_ls_s_alh_centos_7_7(self):
        """
        Test 'ls -alh /' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.centos_7_7_ls_alh.splitlines(), quiet=True)), self.centos_7_7_ls_alh_streaming_json)

    def test_ls_s_alh_ubuntu_18_4(self):
        """
        Test 'ls -alh /' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.ubuntu_18_4_ls_alh.splitlines(), quiet=True)), self.ubuntu_18_4_ls_alh_streaming_json)

    def test_ls_s_alh_osx_10_14_6(self):
        """
        Test 'ls -alh /' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.osx_10_14_6_ls_alh.splitlines(), quiet=True)), self.osx_10_14_6_ls_alh_streaming_json)

    def test_ls_s_alR_centos_7_7(self):
        """
        Test 'ls -alR /usr' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.centos_7_7_ls_alR.splitlines(), quiet=True)), self.centos_7_7_ls_alR_streaming_json)

    def test_ls_s_alR_ubuntu_18_4(self):
        """
        Test 'ls -alR /usr' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.ubuntu_18_4_ls_alR.splitlines(), quiet=True)), self.ubuntu_18_4_ls_alR_streaming_json)

    def test_ls_s_alR_osx_10_14_6(self):
        """
        Test 'ls -alR /usr' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.osx_10_14_6_ls_alR.splitlines(), quiet=True)), self.osx_10_14_6_ls_alR_streaming_json)

    def test_ls_s_lR_empty_folder_osx_10_14_6(self):
        """
        Test 'ls -lR' for empty directories on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.osx_10_14_6_ls_lR_empty_folder.splitlines(), quiet=True)), self.osx_10_14_6_ls_lR_empty_folder_streaming_json)

    def test_ls_s_l_iso_ubuntu_18_4(self):
        """
        Test 'ls -l --time-style=full-iso' for files with convertible dates on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.ubuntu_18_4_ls_l_iso.splitlines(), quiet=True)), self.ubuntu_18_4_ls_l_iso_streaming_json)

    def test_ls_s_l_devices(self):
        """
        Test 'ls -l' on block and character device entries (e.g. /dev),
        which report major/minor numbers instead of a size.
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.ls_l_devices.splitlines(), quiet=True)), self.ls_l_devices_streaming_json)

    def test_ls_s_l_long_iso(self):
        """
        Test 'ls -l --time-style=long-iso', whose date field is 2 tokens
        wide instead of the default/full-iso 3.
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.ls_l_long_iso.splitlines(), quiet=True)), self.ls_l_long_iso_streaming_json)

    def test_ls_s_l_entry_like_dirnames(self):
        """
        Test 'ls -l -- *' where some directory names look like 'ls -l'
        entry lines or a 'total' line, and a filename ends in ':'. The
        'name:' headers are only recognized by position (first line or
        after a blank line, and followed by a 'total' line).
        """
        self.assertEqual(list(jc.parsers.ls_s.parse(self.ls_l_entry_like_dirnames.splitlines(), quiet=True)), self.ls_l_entry_like_dirnames_streaming_json)

    def test_ls_s_l_newline_structure_like_names(self):
        """
        Test 'ls -l' (without -b) with filenames containing a newline
        followed by text that looks like a 'total' line or a 'name:'
        header. The continuation lines are reported as parsing errors
        and do not set a parent.
        """
        result = list(jc.parsers.ls_s.parse(self.ls_l_newline_structure_like_names.splitlines(), quiet=True, ignore_exceptions=True))
        self.assertEqual([x['_jc_meta']['success'] for x in result], [True, True, False, True, False, True])
        self.assertEqual(result[2]['_jc_meta']['line'], 'total 1')
        self.assertEqual(result[4]['_jc_meta']['line'], 'alpha:')
        self.assertFalse(any('parent' in x for x in result))

    def test_ls_s_l_newline_structure_like_names_raise_exception(self):
        """
        Test 'ls -l' (without -b) with filenames containing a newline
        followed by text that looks like a 'total' line (raises ParseError)
        """
        g = jc.parsers.ls_s.parse(self.ls_l_newline_structure_like_names.splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_ls_s_lazy(self):
        """
        Test that records are yielded while input is still being read
        (at most one line of lookahead)
        """
        lines = self.ls_l_entry_like_dirnames.splitlines()
        consumed = []

        def line_gen():
            for i, line in enumerate(lines):
                consumed.append(i)
                yield line

        g = jc.parsers.ls_s.parse(line_gen(), quiet=True)
        first = next(g)
        self.assertEqual(first['filename'], 'notes:')
        self.assertEqual(consumed[-1], 1)
        second = next(g)
        self.assertEqual(second['filename'], 'run.sh')
        self.assertEqual(consumed[-1], 5)


if __name__ == '__main__':
    unittest.main()
