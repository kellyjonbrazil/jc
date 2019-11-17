import os
import json
import unittest
import jc.parsers.systemctl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/systemctl.out'), 'r') as f:
            self.centos_7_7_systemctl = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/systemctl.out'), 'r') as f:
            self.ubuntu_18_4_systemctl = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/systemctl.json'), 'r') as f:
            self.centos_7_7_systemctl_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/systemctl.json'), 'r') as f:
            self.ubuntu_18_4_systemctl_json = json.loads(f.read())

    def test_systemctl_centos_7_7(self):
        """
        Test 'systemctl -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.systemctl.parse(self.centos_7_7_systemctl, quiet=True), self.centos_7_7_systemctl_json)

    def test_systemctl_ubuntu_18_4(self):
        """
        Test 'systemctl -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.systemctl.parse(self.ubuntu_18_4_systemctl, quiet=True), self.ubuntu_18_4_systemctl_json)


if __name__ == '__main__':
    unittest.main()
