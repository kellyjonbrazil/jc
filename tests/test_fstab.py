import os
import json
import unittest
import jc.parsers.fstab

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/fstab.out'), 'r') as f:
            self.centos_7_7_fstab = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/fstab.out'), 'r') as f:
            self.ubuntu_18_4_fstab = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/fstab.json'), 'r') as f:
            self.centos_7_7_fstab_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/fstab.json'), 'r') as f:
            self.ubuntu_18_4_fstab_json = json.loads(f.read())

    def test_fstab_centos_7_7(self):
        """
        Test 'cat /etc/fstab' on Centos 7.7
        """
        self.assertEqual(jc.parsers.fstab.parse(self.centos_7_7_fstab, quiet=True), self.centos_7_7_fstab_json)

    def test_fstab_ubuntu_18_4(self):
        """
        Test 'cat /etc/fstab' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.fstab.parse(self.ubuntu_18_4_fstab, quiet=True), self.ubuntu_18_4_fstab_json)


if __name__ == '__main__':
    unittest.main()
