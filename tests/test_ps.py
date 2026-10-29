import os
import json
import unittest
import jc.parsers.ps

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ps-ef.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ps_ef = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ps-ef.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ps_ef = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ps-ef.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ps_ef = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ps-ef.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ps_ef = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ps-axu.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ps_axu = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ps-axu.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ps_axu = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ps-axu.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ps_axu = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ps-axu.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ps_axu = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ps-ef.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ps_ef_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ps-ef.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ps_ef_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ps-ef.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ps_ef_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ps-ef.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ps_ef_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ps-axu.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ps_axu_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ps-axu.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ps_axu_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ps-axu.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ps_axu_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ps-axu.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ps_axu_json = json.loads(f.read())


    def test_ps_line_separators(self):
        """
        Test 'ps' with line-break characters other than LF in a command line
        """
        data = 'UID         PID   PPID  C STIME TTY          TIME CMD\nroot          1      0  0 Oct25 ?        00:00:03 echo a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\nroot          2      0  0 Oct25 ?        00:00:00 [kthreadd]\n'
        result = jc.parsers.ps.parse(data, quiet=True)
        self.assertEqual(result[0]['cmd'], 'echo a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[1]['pid'], 2)

    def test_ps_nodata(self):
        """
        Test 'ps' with no data
        """
        self.assertEqual(jc.parsers.ps.parse('', quiet=True), [])

    def test_ps_ef_centos_7_7(self):
        """
        Test 'ps -ef' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ps.parse(self.centos_7_7_ps_ef, quiet=True), self.centos_7_7_ps_ef_json)

    def test_ps_ef_ubuntu_18_4(self):
        """
        Test 'ps -ef' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ps.parse(self.ubuntu_18_4_ps_ef, quiet=True), self.ubuntu_18_4_ps_ef_json)

    def test_ps_ef_osx_10_11_6(self):
        """
        Test 'ps -ef' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.ps.parse(self.osx_10_11_6_ps_ef, quiet=True), self.osx_10_11_6_ps_ef_json)

    def test_ps_ef_osx_10_14_6(self):
        """
        Test 'ps -ef' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ps.parse(self.osx_10_14_6_ps_ef, quiet=True), self.osx_10_14_6_ps_ef_json)

    def test_ps_axu_centos_7_7(self):
        """
        Test 'ps axu' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ps.parse(self.centos_7_7_ps_axu, quiet=True), self.centos_7_7_ps_axu_json)

    def test_ps_axu_ubuntu_18_4(self):
        """
        Test 'ps axu' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ps.parse(self.ubuntu_18_4_ps_axu, quiet=True), self.ubuntu_18_4_ps_axu_json)

    def test_ps_axu_osx_10_11_6(self):
        """
        Test 'ps axu' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.ps.parse(self.osx_10_11_6_ps_axu, quiet=True), self.osx_10_11_6_ps_axu_json)

    def test_ps_axu_osx_10_14_6(self):
        """
        Test 'ps axu' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ps.parse(self.osx_10_14_6_ps_axu, quiet=True), self.osx_10_14_6_ps_axu_json)


if __name__ == '__main__':
    unittest.main()
