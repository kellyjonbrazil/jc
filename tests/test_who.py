import os
import json
import unittest
import jc.parsers.who

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/who.out'), 'r') as f:
            self.centos_7_7_who = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/who.out'), 'r') as f:
            self.ubuntu_18_4_who = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/who.out'), 'r') as f:
            self.osx_10_14_6_who = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/who-a.out'), 'r') as f:
            self.centos_7_7_who_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/who-a.out'), 'r') as f:
            self.ubuntu_18_4_who_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/who-a.out'), 'r') as f:
            self.osx_10_14_6_who_a = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/who.json'), 'r') as f:
            self.centos_7_7_who_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/who.json'), 'r') as f:
            self.ubuntu_18_4_who_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/who.json'), 'r') as f:
            self.osx_10_14_6_who_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/who-a.json'), 'r') as f:
            self.centos_7_7_who_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/who-a.json'), 'r') as f:
            self.ubuntu_18_4_who_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/who-a.json'), 'r') as f:
            self.osx_10_14_6_who_a_json = json.loads(f.read())

    def test_who_centos_7_7(self):
        """
        Test 'who' on Centos 7.7
        """
        self.assertEqual(jc.parsers.who.parse(self.centos_7_7_who, quiet=True), self.centos_7_7_who_json)

    def test_who_ubuntu_18_4(self):
        """
        Test 'who' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.who.parse(self.ubuntu_18_4_who, quiet=True), self.ubuntu_18_4_who_json)

    def test_who_osx_10_14_6(self):
        """
        Test 'who' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.who.parse(self.osx_10_14_6_who, quiet=True), self.osx_10_14_6_who_json)

    def test_who_a_centos_7_7(self):
        """
        Test 'who -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.who.parse(self.centos_7_7_who_a, quiet=True), self.centos_7_7_who_a_json)

    def test_who_a_ubuntu_18_4(self):
        """
        Test 'who -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.who.parse(self.ubuntu_18_4_who_a, quiet=True), self.ubuntu_18_4_who_a_json)

    def test_who_a_osx_10_14_6(self):
        """
        Test 'who -a' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.who.parse(self.osx_10_14_6_who_a, quiet=True), self.osx_10_14_6_who_a_json)


if __name__ == '__main__':
    unittest.main()
