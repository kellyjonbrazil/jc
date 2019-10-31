import os
import unittest
import jc.parsers.lsblk

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsblk.out'), 'r') as f:
            self.centos_7_7_lsblk = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsblk.out'), 'r') as f:
            self.ubuntu_18_4_lsblk = f.read()

    def test_lsblk_centos_7_7(self):
        """
        Test 'lsblk' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsblk.parse(self.centos_7_7_lsblk)[4], {'name': 'centos-swap',
                                                                            'maj_min': '253:1',
                                                                            'rm': '0',
                                                                            'size': '2G',
                                                                            'ro': '0',
                                                                            'type': 'lvm',
                                                                            'mountpoint': '[SWAP]'})

    def test_lsblk_ubuntu_18_4(self):
        """
        Test 'lsblk' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsblk.parse(self.ubuntu_18_4_lsblk)[8], {'name': 'loop8',
                                                                             'maj_min': '7:8',
                                                                             'rm': '0',
                                                                             'size': '3.1M',
                                                                             'ro': '1',
                                                                             'type': 'loop',
                                                                             'mountpoint': '/snap/stress-ng/847'})


if __name__ == '__main__':
    unittest.main()
