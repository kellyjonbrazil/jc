import os
import json
import unittest
import jc.parsers.du

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/du.out'), 'r') as f:
            self.centos_7_7_du = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/du.out'), 'r') as f:
            self.ubuntu_18_4_du = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/du.out'), 'r') as f:
            self.osx_10_11_6_du = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/du.out'), 'r') as f:
            self.osx_10_14_6_du = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/du.json'), 'r') as f:
            self.centos_7_7_du_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/du.json'), 'r') as f:
            self.ubuntu_18_4_du_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/du.json'), 'r') as f:
            self.osx_10_11_6_du_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/du.json'), 'r') as f:
            self.osx_10_14_6_du_json = json.loads(f.read())

    def test_du_centos_7_7(self):
        """
        Test 'du' on Centos 7.7
        """
        self.assertEqual(jc.parsers.du.parse(self.centos_7_7_du, quiet=True), self.centos_7_7_du_json)

    def test_du_ubuntu_18_4(self):
        """
        Test 'du' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.du.parse(self.ubuntu_18_4_du, quiet=True), self.ubuntu_18_4_du_json)

    def test_du_osx_10_11_6(self):
        """
        Test 'du' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.du.parse(self.osx_10_11_6_du, quiet=True), self.osx_10_11_6_du_json)

    def test_du_osx_10_14_6(self):
        """
        Test 'du' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.du.parse(self.osx_10_14_6_du, quiet=True), self.osx_10_14_6_du_json)


if __name__ == '__main__':
    unittest.main()
