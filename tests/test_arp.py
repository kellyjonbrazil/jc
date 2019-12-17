import os
import unittest
import json
import jc.parsers.arp

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/arp.out'), 'r') as f:
            self.centos_7_7_arp = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/arp.out'), 'r') as f:
            self.ubuntu_18_4_arp = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/arp-a.out'), 'r') as f:
            self.centos_7_7_arp_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/arp-a.out'), 'r') as f:
            self.ubuntu_18_4_arp_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/arp-v.out'), 'r') as f:
            self.centos_7_7_arp_v = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/arp-v.out'), 'r') as f:
            self.ubuntu_18_4_arp_v = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/arp-a.out'), 'r') as f:
            self.osx_10_11_6_arp_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/arp-a.out'), 'r') as f:
            self.osx_10_14_6_arp_a = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/arp.json'), 'r') as f:
            self.centos_7_7_arp_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/arp.json'), 'r') as f:
            self.ubuntu_18_4_arp_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/arp-a.json'), 'r') as f:
            self.centos_7_7_arp_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/arp-a.json'), 'r') as f:
            self.ubuntu_18_4_arp_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/arp-v.json'), 'r') as f:
            self.centos_7_7_arp_v_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/arp-v.json'), 'r') as f:
            self.ubuntu_18_4_arp_v_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/arp-a.json'), 'r') as f:
            self.osx_10_11_6_arp_a_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/arp-a.json'), 'r') as f:
            self.osx_10_14_6_arp_a_json = json.loads(f.read())

    def test_arp_centos_7_7(self):
        """
        Test 'arp' on Centos 7.7
        """
        self.assertEqual(jc.parsers.arp.parse(self.centos_7_7_arp, quiet=True), self.centos_7_7_arp_json)

    def test_arp_ubuntu_18_4(self):
        """
        Test 'arp' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.arp.parse(self.ubuntu_18_4_arp, quiet=True), self.ubuntu_18_4_arp_json)

    def test_arp_a_centos_7_7(self):
        """
        Test 'arp -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.arp.parse(self.centos_7_7_arp_a, quiet=True), self.centos_7_7_arp_a_json)

    def test_arp_a_ubuntu_18_4(self):
        """
        Test 'arp -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.arp.parse(self.ubuntu_18_4_arp_a, quiet=True), self.ubuntu_18_4_arp_a_json)

    def test_arp_v_centos_7_7(self):
        """
        Test 'arp -v' on Centos 7.7
        """
        self.assertEqual(jc.parsers.arp.parse(self.centos_7_7_arp_v, quiet=True), self.centos_7_7_arp_v_json)

    def test_arp_v_ubuntu_18_4(self):
        """
        Test 'arp -v' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.arp.parse(self.ubuntu_18_4_arp_v, quiet=True), self.ubuntu_18_4_arp_v_json)

    def test_arp_a_osx_10_11_6(self):
        """
        Test 'arp -a' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.arp.parse(self.osx_10_11_6_arp_a, quiet=True), self.osx_10_11_6_arp_a_json)

    def test_arp_a_osx_10_14_6(self):
        """
        Test 'arp -a' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.arp.parse(self.osx_10_14_6_arp_a, quiet=True), self.osx_10_14_6_arp_a_json)


if __name__ == '__main__':
    unittest.main()
