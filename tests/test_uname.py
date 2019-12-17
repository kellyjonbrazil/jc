import os
import json
import unittest
import jc.parsers.uname

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uname-a.out'), 'r') as f:
            self.centos_7_7_uname_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uname-a.out'), 'r') as f:
            self.ubuntu_18_4_uname_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/uname-a.out'), 'r') as f:
            self.osx_10_11_6_uname_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uname-a.out'), 'r') as f:
            self.osx_10_14_6_uname_a = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uname-a.json'), 'r') as f:
            self.centos_7_7_uname_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uname-a.json'), 'r') as f:
            self.ubuntu_18_4_uname_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/uname-a.json'), 'r') as f:
            self.osx_10_11_6_uname_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uname-a.json'), 'r') as f:
            self.osx_10_14_6_uname_a_json = json.loads(f.read())

    def test_uname_centos_7_7(self):
        """
        Test 'uname -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.uname.parse(self.centos_7_7_uname_a, quiet=True), self.centos_7_7_uname_a_json)

    def test_uname_ubuntu_18_4(self):
        """
        Test 'uname -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.uname.parse(self.ubuntu_18_4_uname_a, quiet=True), self.ubuntu_18_4_uname_a_json)

    def test_uname_osx_10_11_6(self):
        """
        Test 'uname -a' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.uname.parse(self.osx_10_11_6_uname_a, quiet=True), self.osx_10_11_6_uname_a_json)

    def test_uname_osx_10_14_6(self):
        """
        Test 'uname -a' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.uname.parse(self.osx_10_14_6_uname_a, quiet=True), self.osx_10_14_6_uname_a_json)


if __name__ == '__main__':
    unittest.main()
