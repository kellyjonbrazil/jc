import os
import json
import unittest
import jc.parsers.lsof

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsof.out'), 'r', encoding='utf-8') as f:
        centos_7_7_lsof = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsof.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lsof = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsof-sudo.out'), 'r', encoding='utf-8') as f:
        centos_7_7_lsof_sudo = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsof-sudo.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lsof_sudo = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsof--long-name.out'), 'r', encoding='utf-8') as f:
        generic_lsof_long_name = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsof.json'), 'r', encoding='utf-8') as f:
        centos_7_7_lsof_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsof.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lsof_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsof-sudo.json'), 'r', encoding='utf-8') as f:
        centos_7_7_lsof_sudo_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsof-sudo.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lsof_sudo_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsof--long-name.json'), 'r', encoding='utf-8') as f:
        generic_lsof_long_name_json = json.loads(f.read())


    def test_lsof_line_separators(self):
        """
        Test 'lsof' with line-break characters other than LF in a file name
        """
        data = 'COMMAND    PID  TID    USER   FD      TYPE DEVICE  SIZE/OFF     NODE NAME\nsystemd      1         root  cwd       DIR  253,0       224       64 /tmp/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\nsystemd      1         root  rtd       DIR  253,0       224       64 /\n'
        result = jc.parsers.lsof.parse(data, quiet=True)
        self.assertEqual(result[0]['name'], '/tmp/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[1]['fd'], 'rtd')

    def test_lsof_nodata(self):
        """
        Test 'lsof' with no data
        """
        self.assertEqual(jc.parsers.lsof.parse('', quiet=True), [])

    def test_lsof_centos_7_7(self):
        """
        Test 'lsof' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsof.parse(self.centos_7_7_lsof, quiet=True), self.centos_7_7_lsof_json)

    def test_lsof_ubuntu_18_4(self):
        """
        Test 'lsof' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsof.parse(self.ubuntu_18_4_lsof, quiet=True), self.ubuntu_18_4_lsof_json)

    def test_lsof_sudo_centos_7_7(self):
        """
        Test 'sudo lsof' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsof.parse(self.centos_7_7_lsof_sudo, quiet=True), self.centos_7_7_lsof_sudo_json)

    def test_lsof_sudo_ubuntu_18_4(self):
        """
        Test 'sudo lsof' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsof.parse(self.ubuntu_18_4_lsof_sudo, quiet=True), self.ubuntu_18_4_lsof_sudo_json)

    def test_lsof_long_name(self):
        """
        Test 'lsof' with one very long NAME value and many ordinary rows
        """
        self.assertEqual(jc.parsers.lsof.parse(self.generic_lsof_long_name, quiet=True), self.generic_lsof_long_name_json)


if __name__ == '__main__':
    unittest.main()
