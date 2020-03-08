import os
import unittest
import json
import jc.parsers.blkid

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-sda2.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_sda2 = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-sda2.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_sda2 = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-udev.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_ip_udev = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-udev.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_ip_udev = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-multi.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_ip_multi = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-multi.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_ip_multi = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-udev-multi.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_ip_udev_multi = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-udev-multi.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_ip_udev_multi = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-sda2.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_sda2_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-sda2.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_sda2_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-udev.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_ip_udev_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-udev.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_ip_udev_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-multi.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_ip_multi_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-multi.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_ip_multi_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-udev-multi.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_blkid_ip_udev_multi_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-udev-multi.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_blkid_ip_udev_multi_json = json.loads(f.read())

    def test_blkid_centos_7_7(self):
        """
        Test 'blkid' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid, quiet=True), self.centos_7_7_blkid_json)

    def test_blkid_ubuntu_18_4(self):
        """
        Test 'blkid' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid, quiet=True), self.ubuntu_18_4_blkid_json)

    def test_blkid_sda2_centos_7_7(self):
        """
        Test 'blkid /dev/sda2' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid_sda2, quiet=True), self.centos_7_7_blkid_sda2_json)

    def test_blkid_sda2_ubuntu_18_4(self):
        """
        Test 'blkid /dev/sda2' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid_sda2, quiet=True), self.ubuntu_18_4_blkid_sda2_json)

    def test_blkid_ip_udev_centos_7_7(self):
        """
        Test 'blkid -ip -o udev /dev/sda2' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid_ip_udev, quiet=True), self.centos_7_7_blkid_ip_udev_json)

    def test_blkid_ip_udev_ubuntu_18_4(self):
        """
        Test 'blkid -ip -o udev /dev/sda2' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid_sda2, quiet=True), self.ubuntu_18_4_blkid_sda2_json)

    def test_blkid_ip_multi_centos_7_7(self):
        """
        Test 'blkid -ip /dev/sda1 /dev/sda2' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid_ip_multi, quiet=True), self.centos_7_7_blkid_ip_multi_json)

    def test_blkid_ip_multi_ubuntu_18_4(self):
        """
        Test 'blkid -ip /dev/sda1 /dev/sda2' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid_ip_multi, quiet=True), self.ubuntu_18_4_blkid_ip_multi_json)

    def test_blkid_ip_udev_multi_centos_7_7(self):
        """
        Test 'blkid -ip -o udev /dev/sda1 /dev/sda2' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid_ip_udev_multi, quiet=True), self.centos_7_7_blkid_ip_udev_multi_json)

    def test_blkid_ip_udev_multi_ubuntu_18_4(self):
        """
        Test 'blkid -ip -o udev /dev/sda1 /dev/sda2' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid_ip_udev_multi, quiet=True), self.ubuntu_18_4_blkid_ip_udev_multi_json)


if __name__ == '__main__':
    unittest.main()
