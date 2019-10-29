import os
import unittest
import jc.parsers.netstat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat.out'), 'r') as f:
            self.centos_7_7_netstat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat.out'), 'r') as f:
            self.ubuntu_18_4_netstat = f.read()

    def test_netstat_centos_7_7(self):
        """
        Test 'netstat' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat)[1], {'transport_protocol': 'tcp',
                                                                                'network_protocol': 'ipv4',
                                                                                'local_address': 'localhost.localdoma',
                                                                                'local_port': 'ssh',
                                                                                'foreign_address': '192.168.71.1',
                                                                                'foreign_port': '58727',
                                                                                'state': 'ESTABLISHED',
                                                                                'receive_q': '0',
                                                                                'send_q': '0'})

    def test_netstat_ubuntu_18_4(self):
        """
        Test 'netstat' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat)[1], {'transport_protocol': 'tcp',
                                                                                 'network_protocol': 'ipv4',
                                                                                 'local_address': 'kbrazil-ubuntu',
                                                                                 'local_port': '55656',
                                                                                 'foreign_address': 'lb-192-30-253-113',
                                                                                 'foreign_port': 'https',
                                                                                 'state': 'ESTABLISHED',
                                                                                 'receive_q': '0',
                                                                                 'send_q': '0'})


if __name__ == '__main__':
    unittest.main()
