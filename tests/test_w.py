import os
import json
import unittest
import jc.parsers.w

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/w.out'), 'r') as f:
            self.centos_7_7_w = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/w.out'), 'r') as f:
            self.ubuntu_18_4_w = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/w.out'), 'r') as f:
            self.osx_10_11_6_w = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/w.out'), 'r') as f:
            self.osx_10_14_6_w = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/w.json'), 'r') as f:
            self.centos_7_7_w_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/w.json'), 'r') as f:
            self.ubuntu_18_4_w_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/w.json'), 'r') as f:
            self.osx_10_11_6_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/w.json'), 'r') as f:
            self.osx_10_14_6_json = json.loads(f.read())

    def test_w_centos_7_7(self):
        """
        Test 'w' on Centos 7.7
        """
        self.assertEqual(jc.parsers.w.parse(self.centos_7_7_w, quiet=True), self.centos_7_7_w_json)

    def test_w_ubuntu_18_4(self):
        """
        Test 'w' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.w.parse(self.ubuntu_18_4_w, quiet=True), self.ubuntu_18_4_w_json)

    def test_w_osx_10_11_6(self):
        """
        Test 'w' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.w.parse(self.osx_10_11_6_w, quiet=True), self.osx_10_11_6_json)

    def test_w_osx_10_14_6(self):
        """
        Test 'w' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.w.parse(self.osx_10_14_6_w, quiet=True), self.osx_10_14_6_json)


if __name__ == '__main__':
    unittest.main()
