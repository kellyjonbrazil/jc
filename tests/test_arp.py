import os
import unittest
import jc.parsers.arp

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
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

    def test_arp_centos_7_7(self):
        """
        Test 'arp' on Centos 7.7
        """
        self.assertEqual(jc.parsers.arp.parse(self.centos_7_7_arp), [{'address': 'gateway',
                                                                      'flags_mask': 'C',
                                                                      'hwaddress': '00:50:56:f7:4a:fc',
                                                                      'hwtype': 'ether',
                                                                      'iface': 'ens33'},
                                                                     {'address': '192.168.71.254',
                                                                      'flags_mask': 'C',
                                                                      'hwaddress': '00:50:56:fe:7a:b4',
                                                                      'hwtype': 'ether',
                                                                      'iface': 'ens33'}])

    def test_arp_ubuntu_18_4(self):
        """
        Test 'arp' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.arp.parse(self.ubuntu_18_4_arp), [{'address': '192.168.71.254',
                                                                       'flags_mask': 'C',
                                                                       'hwaddress': '00:50:56:fe:7a:b4',
                                                                       'hwtype': 'ether',
                                                                       'iface': 'ens33'},
                                                                      {'address': '_gateway',
                                                                       'flags_mask': 'C',
                                                                       'hwaddress': '00:50:56:f7:4a:fc',
                                                                       'hwtype': 'ether',
                                                                       'iface': 'ens33'}])

    def test_arp_a_centos_7_7(self):
        """
        Test 'arp -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.arp.parse(self.centos_7_7_arp_a), [{'address': '192.168.71.2',
                                                                        'hwaddress': '00:50:56:f7:4a:fc',
                                                                        'hwtype': 'ether',
                                                                        'iface': 'ens33',
                                                                        'name': 'gateway'},
                                                                       {'address': '192.168.71.1',
                                                                        'hwaddress': '00:50:56:c0:00:08',
                                                                        'hwtype': 'ether',
                                                                        'iface': 'ens33',
                                                                        'name': '?'},
                                                                       {'address': '192.168.71.254',
                                                                        'hwaddress': '00:50:56:fe:7a:b4',
                                                                        'hwtype': 'ether',
                                                                        'iface': 'ens33',
                                                                        'name': '?'}])

    def test_arp_a_ubuntu_18_4(self):
        """
        Test 'arp -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.arp.parse(self.ubuntu_18_4_arp_a), [{'address': '192.168.71.1',
                                                                         'hwaddress': '00:50:56:c0:00:08',
                                                                         'hwtype': 'ether',
                                                                         'iface': 'ens33',
                                                                         'name': '?'},
                                                                        {'address': '192.168.71.254',
                                                                         'hwaddress': '00:50:56:fe:7a:b4',
                                                                         'hwtype': 'ether',
                                                                         'iface': 'ens33',
                                                                         'name': '?'},
                                                                        {'address': '192.168.71.2',
                                                                         'hwaddress': '00:50:56:f7:4a:fc',
                                                                         'hwtype': 'ether',
                                                                         'iface': 'ens33',
                                                                         'name': '_gateway'}])

    def test_arp_v_centos_7_7(self):
        """
        Test 'arp -v' on Centos 7.7
        """
        self.assertEqual(jc.parsers.arp.parse(self.centos_7_7_arp_v), [{'address': 'gateway',
                                                                        'flags_mask': 'C',
                                                                        'hwaddress': '00:50:56:f7:4a:fc',
                                                                        'hwtype': 'ether',
                                                                        'iface': 'ens33'},
                                                                       {'address': '192.168.71.254',
                                                                        'flags_mask': 'C',
                                                                        'hwaddress': '00:50:56:fe:7a:b4',
                                                                        'hwtype': 'ether',
                                                                        'iface': 'ens33'}])

    def test_arp_v_ubuntu_18_4(self):
        """
        Test 'arp -v' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.arp.parse(self.ubuntu_18_4_arp_v), [{'address': '192.168.71.254',
                                                                         'flags_mask': 'C',
                                                                         'hwaddress': '00:50:56:fe:7a:b4',
                                                                         'hwtype': 'ether',
                                                                         'iface': 'ens33'},
                                                                        {'address': '_gateway',
                                                                         'flags_mask': 'C',
                                                                         'hwaddress': '00:50:56:f7:4a:fc',
                                                                         'hwtype': 'ether',
                                                                         'iface': 'ens33'}])


if __name__ == '__main__':
    unittest.main()
