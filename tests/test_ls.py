import os
import json
import unittest
import jc.parsers.ls

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls.out'), 'r') as f:
            self.centos_7_7_ls = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls.out'), 'r') as f:
            self.ubuntu_18_4_ls = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls.out'), 'r') as f:
            self.osx_10_11_6_ls = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls.out'), 'r') as f:
            self.osx_10_14_6_ls = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-al.out'), 'r') as f:
            self.centos_7_7_ls_al = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-al.out'), 'r') as f:
            self.ubuntu_18_4_ls_al = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls-al.out'), 'r') as f:
            self.osx_10_11_6_ls_al = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-al.out'), 'r') as f:
            self.osx_10_14_6_ls_al = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alh.out'), 'r') as f:
            self.centos_7_7_ls_alh = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alh.out'), 'r') as f:
            self.ubuntu_18_4_ls_alh = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls-alh.out'), 'r') as f:
            self.osx_10_11_6_ls_alh = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alh.out'), 'r') as f:
            self.osx_10_14_6_ls_alh = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls.json'), 'r') as f:
            self.centos_7_7_ls_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls.json'), 'r') as f:
            self.ubuntu_18_4_ls_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls.json'), 'r') as f:
            self.osx_10_11_6_ls_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls.json'), 'r') as f:
            self.osx_10_14_6_ls_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-al.json'), 'r') as f:
            self.centos_7_7_ls_al_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-al.json'), 'r') as f:
            self.ubuntu_18_4_ls_al_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls-al.json'), 'r') as f:
            self.osx_10_11_6_ls_al_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-al.json'), 'r') as f:
            self.osx_10_14_6_ls_al_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alh.json'), 'r') as f:
            self.centos_7_7_ls_alh_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alh.json'), 'r') as f:
            self.ubuntu_18_4_ls_alh_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ls-alh.json'), 'r') as f:
            self.osx_10_11_6_ls_alh_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ls-alh.json'), 'r') as f:
            self.osx_10_14_6_ls_alh_json = json.loads(f.read())

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


if __name__ == '__main__':
    unittest.main()
