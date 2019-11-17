import os
import json
import unittest
import jc.parsers.ss

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ss-sudo-a.out'), 'r') as f:
            self.centos_7_7_ss_sudo_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ss-sudo-a.out'), 'r') as f:
            self.ubuntu_18_4_ss_sudo_a = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ss-sudo-a.json'), 'r') as f:
            self.centos_7_7_ss_sudo_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ss-sudo-a.json'), 'r') as f:
            self.ubuntu_18_4_ss_sudo_a_json = json.loads(f.read())

    def test_ss_sudo_a_centos_7_7(self):
        """
        Test 'sudo ss -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ss.parse(self.centos_7_7_ss_sudo_a, quiet=True), self.centos_7_7_ss_sudo_a_json)

    def test_ss_sudo_a_ubuntu_18_4(self):
        """
        Test 'sudo ss -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ss.parse(self.ubuntu_18_4_ss_sudo_a, quiet=True), self.ubuntu_18_4_ss_sudo_a_json)


if __name__ == '__main__':
    unittest.main()
