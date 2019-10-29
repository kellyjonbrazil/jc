import os
import unittest
import jc.parsers.uname

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uname-a.out'), 'r') as f:
            self.centos_7_7_uname_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uname-a.out'), 'r') as f:
            self.ubuntu_18_4_uname_a = f.read()

    def test_uname_centos_7_7(self):
        """
        Test 'uname -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.uname.parse(self.centos_7_7_uname_a), {'kernel_name': 'Linux',
                                                                           'node_name': 'localhost.localdomain',
                                                                           'kernel_release': '3.10.0-1062.1.2.el7.x86_64',
                                                                           'operating_system': 'GNU/Linux',
                                                                           'hardware_platform': 'x86_64',
                                                                           'processor': 'x86_64',
                                                                           'machine': 'x86_64',
                                                                           'kernel_version': '#1 SMP Mon Sep 30 14:19:46 UTC 2019'})

    def test_uname_ubuntu_18_4(self):
        """
        Test 'uname -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.uname.parse(self.ubuntu_18_4_uname_a), {'kernel_name': 'Linux',
                                                                            'node_name': 'kbrazil-ubuntu',
                                                                            'kernel_release': '4.15.0-65-generic',
                                                                            'operating_system': 'GNU/Linux',
                                                                            'hardware_platform': 'x86_64',
                                                                            'processor': 'x86_64',
                                                                            'machine': 'x86_64',
                                                                            'kernel_version': '#74-Ubuntu SMP Tue Sep 17 17:06:04 UTC 2019'})


if __name__ == '__main__':
    unittest.main()
