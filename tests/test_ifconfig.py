import os
import json
import unittest
import jc.parsers.ifconfig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ifconfig.out'), 'r') as f:
            self.centos_7_7_ifconfig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ifconfig.out'), 'r') as f:
            self.ubuntu_18_4_ifconfig = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ifconfig.json'), 'r') as f:
            self.centos_7_7_ifconfig_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ifconfig.json'), 'r') as f:
            self.ubuntu_18_4_ifconfig_json = json.loads(f.read())

    def test_ifconfig_centos_7_7(self):
        """
        Test 'ifconfig' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.centos_7_7_ifconfig, quiet=True), self.centos_7_7_ifconfig_json)

    def test_ifconfig_ubuntu_18_4(self):
        """
        Test 'ifconfig' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.ubuntu_18_4_ifconfig, quiet=True), self.ubuntu_18_4_ifconfig_json)


if __name__ == '__main__':
    unittest.main()
