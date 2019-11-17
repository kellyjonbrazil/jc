import os
import json
import unittest
import jc.parsers.hosts

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/hosts.out'), 'r') as f:
            self.centos_7_7_hosts = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/hosts.out'), 'r') as f:
            self.ubuntu_18_4_hosts = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/hosts.json'), 'r') as f:
            self.centos_7_7_hosts_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/hosts.json'), 'r') as f:
            self.ubuntu_18_4_hosts_json = json.loads(f.read())

    def test_hosts_centos_7_7(self):
        """
        Test 'cat /etc/hosts' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hosts.parse(self.centos_7_7_hosts, quiet=True), self.centos_7_7_hosts_json)

    def test_hosts_ubuntu_18_4(self):
        """
        Test 'cat /etc/hosts' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.hosts.parse(self.ubuntu_18_4_hosts, quiet=True), self.ubuntu_18_4_hosts_json)


if __name__ == '__main__':
    unittest.main()
