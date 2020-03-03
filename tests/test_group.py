import os
import json
import unittest
import jc.parsers.group

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/group.out'), 'r') as f:
            self.centos_7_7_group = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/group.out'), 'r') as f:
            self.ubuntu_18_4_group = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/group.out'), 'r') as f:
            self.osx_10_14_6_group = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/group.json'), 'r') as f:
            self.centos_7_7_group_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/group.json'), 'r') as f:
            self.ubuntu_18_4_group_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/group.json'), 'r') as f:
            self.osx_10_14_6_group_json = json.loads(f.read())

    def test_group_centos_7_7(self):
        """
        Test 'cat /etc/group' on Centos 7.7
        """
        self.assertEqual(jc.parsers.group.parse(self.centos_7_7_group, quiet=True), self.centos_7_7_group_json)

    def test_group_ubuntu_18_4(self):
        """
        Test 'cat /etc/group' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.group.parse(self.ubuntu_18_4_group, quiet=True), self.ubuntu_18_4_group_json)

    def test_group_osx_10_14_6(self):
        """
        Test 'cat /etc/group' on OSX 10.14
        """
        self.assertEqual(jc.parsers.group.parse(self.osx_10_14_6_group, quiet=True), self.osx_10_14_6_group_json)


if __name__ == '__main__':
    unittest.main()
