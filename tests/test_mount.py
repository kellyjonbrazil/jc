import os
import json
import unittest
import jc.parsers.mount

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mount.out'), 'r') as f:
            self.centos_7_7_mount = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/mount.out'), 'r') as f:
            self.ubuntu_18_4_mount = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mount.json'), 'r') as f:
            self.centos_7_7_mount_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/mount.json'), 'r') as f:
            self.ubuntu_18_4_mount_json = json.loads(f.read())

    def test_mount_centos_7_7(self):
        """
        Test 'mount' on Centos 7.7
        """
        self.assertEqual(jc.parsers.mount.parse(self.centos_7_7_mount, quiet=True), self.centos_7_7_mount_json)

    def test_mount_ubuntu_18_4(self):
        """
        Test 'mount' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.mount.parse(self.ubuntu_18_4_mount, quiet=True), self.ubuntu_18_4_mount_json)


if __name__ == '__main__':
    unittest.main()
