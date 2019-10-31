import os
import unittest
import jc.parsers.lsmod

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsmod.out'), 'r') as f:
            self.centos_7_7_lsmod = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsmod.out'), 'r') as f:
            self.ubuntu_18_4_lsmod = f.read()

    def test_lsmod_centos_7_7(self):
        """
        Test 'lsmod' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsmod.parse(self.centos_7_7_lsmod)[17], {'module': 'nf_nat_ipv6',
                                                                             'size': '14131',
                                                                             'used': '1',
                                                                             'by': ['ip6table_nat']})

    def test_lsmod_ubuntu_18_4(self):
        """
        Test 'lsmod' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsmod.parse(self.ubuntu_18_4_lsmod)[21], {'module': 'nf_conntrack',
                                                                              'size': '131072',
                                                                              'used': '4',
                                                                              'by': ['xt_conntrack',
                                                                                     'nf_conntrack_ipv4',
                                                                                     'nf_nat',
                                                                                     'nf_nat_ipv4']})


if __name__ == '__main__':
    unittest.main()
