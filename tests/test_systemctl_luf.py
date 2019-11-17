import os
import json
import unittest
import jc.parsers.systemctl_luf

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/systemctl-luf.out'), 'r') as f:
            self.centos_7_7_systemctl_luf = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/systemctl-luf.out'), 'r') as f:
            self.ubuntu_18_4_systemctl_luf = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/systemctl-luf.json'), 'r') as f:
            self.centos_7_7_systemctl_luf_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/systemctl-luf.json'), 'r') as f:
            self.ubuntu_18_4_systemctl_luf_json = json.loads(f.read())

    def test_systemctl_luf_centos_7_7(self):
        """
        Test 'systemctl -a list-sockets' on Centos 7.7
        """
        self.assertEqual(jc.parsers.systemctl_luf.parse(self.centos_7_7_systemctl_luf, quiet=True), self.centos_7_7_systemctl_luf_json)

    def test_systemctl_luf_ubuntu_18_4(self):
        """
        Test 'systemctl -a list-sockets' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.systemctl_luf.parse(self.ubuntu_18_4_systemctl_luf, quiet=True), self.ubuntu_18_4_systemctl_luf_json)


if __name__ == '__main__':
    unittest.main()
