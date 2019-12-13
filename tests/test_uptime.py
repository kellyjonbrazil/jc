import os
import json
import unittest
import jc.parsers.uptime

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uptime.out'), 'r') as f:
            self.centos_7_7_uptime = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uptime.out'), 'r') as f:
            self.ubuntu_18_4_uptime = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/uptime.out'), 'r') as f:
            self.osx_10_11_6_uptime = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uptime.out'), 'r') as f:
            self.osx_10_14_6_uptime = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uptime.json'), 'r') as f:
            self.centos_7_7_uptime_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uptime.json'), 'r') as f:
            self.ubuntu_18_4_uptime_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/uptime.json'), 'r') as f:
            self.osx_10_11_6_uptime_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uptime.json'), 'r') as f:
            self.osx_10_14_6_uptime_json = json.loads(f.read())

    def test_uptime_centos_7_7(self):
        """
        Test 'uptime' on Centos 7.7
        """
        self.assertEqual(jc.parsers.uptime.parse(self.centos_7_7_uptime, quiet=True), self.centos_7_7_uptime_json)

    def test_uptime_ubuntu_18_4(self):
        """
        Test 'uptime' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.uptime.parse(self.ubuntu_18_4_uptime, quiet=True), self.ubuntu_18_4_uptime_json)

    def test_uptime_osx_10_11_6(self):
        """
        Test 'uptime' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.uptime.parse(self.osx_10_11_6_uptime, quiet=True), self.osx_10_11_6_uptime_json)

    def test_uptime_osx_10_14_6(self):
        """
        Test 'uptime' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.uptime.parse(self.osx_10_14_6_uptime, quiet=True), self.osx_10_14_6_uptime_json)


if __name__ == '__main__':
    unittest.main()
