import os
import json
import unittest
import jc.parsers.lsblk

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsblk.out'), 'r') as f:
            self.centos_7_7_lsblk = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsblk.out'), 'r') as f:
            self.ubuntu_18_4_lsblk = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsblk.json'), 'r') as f:
            self.centos_7_7_lsblk_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsblk.json'), 'r') as f:
            self.ubuntu_18_4_lsblk_json = json.loads(f.read())

    def test_lsblk_centos_7_7(self):
        """
        Test 'lsblk' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsblk.parse(self.centos_7_7_lsblk, quiet=True), self.centos_7_7_lsblk_json)

    def test_lsblk_ubuntu_18_4(self):
        """
        Test 'lsblk' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsblk.parse(self.ubuntu_18_4_lsblk, quiet=True), self.ubuntu_18_4_lsblk_json)


if __name__ == '__main__':
    unittest.main()
