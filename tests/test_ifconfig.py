import os
import unittest
import jc.parsers.ifconfig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ifconfig.out'), 'r') as f:
            self.centos_7_7_ifconfig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ifconfig.out'), 'r') as f:
            self.ubuntu_18_4_ifconfig = f.read()

    def test_ifconfig_centos_7_7(self):
        """
        Test 'ifconfig' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.centos_7_7_ifconfig)[0], {'name': 'docker0',
                                                                                  'flags': '4099',
                                                                                  'state': 'UP,BROADCAST,MULTICAST',
                                                                                  'mtu': '1500',
                                                                                  'ipv4_addr': '172.17.0.1',
                                                                                  'ipv4_mask': '255.255.0.0',
                                                                                  'ipv4_bcast': '0.0.0.0',
                                                                                  'mac_addr': '02:42:b1:9a:ea:02',
                                                                                  'type': 'Ethernet',
                                                                                  'rx_packets': '0',
                                                                                  'rx_errors': '0',
                                                                                  'rx_dropped': '0',
                                                                                  'rx_overruns': '0',
                                                                                  'rx_frame': '0',
                                                                                  'tx_packets': '0',
                                                                                  'tx_errors': '0',
                                                                                  'tx_dropped': '0',
                                                                                  'tx_overruns': '0',
                                                                                  'tx_carrier': '0',
                                                                                  'tx_collisions': '0',
                                                                                  'ipv6_addr': None,
                                                                                  'ipv6_mask': None,
                                                                                  'ipv6_scope': None,
                                                                                  'metric': None})

    def test_ifconfig_ubuntu_18_4(self):
        """
        Test 'ifconfig' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.ubuntu_18_4_ifconfig)[1], {'name': 'lo',
                                                                                   'flags': '73',
                                                                                   'state': 'UP,LOOPBACK,RUNNING',
                                                                                   'mtu': '65536',
                                                                                   'ipv4_addr': '127.0.0.1',
                                                                                   'ipv4_mask': '255.0.0.0',
                                                                                   'ipv4_bcast': None,
                                                                                   'ipv6_addr': '::1',
                                                                                   'ipv6_mask': '128',
                                                                                   'ipv6_scope': 'host',
                                                                                   'mac_addr': None,
                                                                                   'type': 'Local Loopback',
                                                                                   'rx_packets': '825',
                                                                                   'rx_errors': '0',
                                                                                   'rx_dropped': '0',
                                                                                   'rx_overruns': '0',
                                                                                   'rx_frame': '0',
                                                                                   'tx_packets': '825',
                                                                                   'tx_errors': '0',
                                                                                   'tx_dropped': '0',
                                                                                   'tx_overruns': '0',
                                                                                   'tx_carrier': '0',
                                                                                   'tx_collisions': '0',
                                                                                   'metric': None})


if __name__ == '__main__':
    unittest.main()
