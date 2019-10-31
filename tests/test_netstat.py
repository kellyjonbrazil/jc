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

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-l.out'), 'r') as f:
            self.centos_7_7_netstat_l = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-l.out'), 'r') as f:
            self.ubuntu_18_4_netstat_l = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-p.out'), 'r') as f:
            self.centos_7_7_netstat_p = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-p.out'), 'r') as f:
            self.ubuntu_18_4_netstat_p = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-lnp.out'), 'r') as f:
            self.centos_7_7_netstat_sudo_lnp = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-lnp.out'), 'r') as f:
            self.ubuntu_18_4_netstat_sudo_lnp = f.read()

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

    def test_netstat_l_centos_7_7(self):
        """
        Test 'netstat -l' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_l)[3], {'transport_protocol': 'tcp',
                                                                                  'network_protocol': 'ipv6',
                                                                                  'local_address': '[::]',
                                                                                  'local_port': 'ssh',
                                                                                  'foreign_address': '[::]',
                                                                                  'foreign_port': '*',
                                                                                  'state': 'LISTEN',
                                                                                  'receive_q': '0',
                                                                                  'send_q': '0'})

    def test_netstat_l_ubuntu_18_4(self):
        """
        Test 'netstat -l' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_l)[4], {'transport_protocol': 'udp',
                                                                                   'network_protocol': 'ipv4',
                                                                                   'local_address': 'localhost',
                                                                                   'local_port': 'domain',
                                                                                   'foreign_address': '0.0.0.0',
                                                                                   'foreign_port': '*',
                                                                                   'receive_q': '0',
                                                                                   'send_q': '0'})

    def test_netstat_p_centos_7_7(self):
        """
        Test 'netstat -l' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_p), [{'transport_protocol': 'tcp',
                                                                                'network_protocol': 'ipv4',
                                                                                'local_address': 'localhost.localdoma',
                                                                                'local_port': 'ssh',
                                                                                'foreign_address': '192.168.71.1',
                                                                                'foreign_port': '58727',
                                                                                'state': 'ESTABLISHED',
                                                                                'receive_q': '0',
                                                                                'send_q': '0'}])

    def test_netstat_p_ubuntu_18_4(self):
        """
        Test 'netstat -l' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_p)[1], {'transport_protocol': 'tcp',
                                                                                   'network_protocol': 'ipv4',
                                                                                   'local_address': 'kbrazil-ubuntu',
                                                                                   'local_port': '55656',
                                                                                   'foreign_address': 'lb-192-30-253-113',
                                                                                   'foreign_port': 'https',
                                                                                   'state': 'ESTABLISHED',
                                                                                   'pid': '23921',
                                                                                   'program_name': 'git-remote-ht',
                                                                                   'receive_q': '0',
                                                                                   'send_q': '0'})

    def test_netstat_sudo_lnp_centos_7_7(self):
        """
        Test 'sudo netstat -lnp' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_sudo_lnp)[5], {'transport_protocol': 'udp',
                                                                                         'network_protocol': 'ipv4',
                                                                                         'local_address': '127.0.0.1',
                                                                                         'local_port': '323',
                                                                                         'foreign_address': '0.0.0.0',
                                                                                         'foreign_port': '*',
                                                                                         'pid': '795',
                                                                                         'program_name': 'chronyd',
                                                                                         'receive_q': '0',
                                                                                         'send_q': '0'})

    def test_netstat_sudo_lnp_ubuntu_18_4(self):
        """
        Test 'sudo netstat -lnp' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_sudo_lnp)[4], {'transport_protocol': 'udp',
                                                                                          'network_protocol': 'ipv4',
                                                                                          'local_address': '127.0.0.53',
                                                                                          'local_port': '53',
                                                                                          'foreign_address': '0.0.0.0',
                                                                                          'foreign_port': '*',
                                                                                          'pid': '885',
                                                                                          'program_name': 'systemd-resolve',
                                                                                          'receive_q': '0',
                                                                                          'send_q': '0'})


if __name__ == '__main__':
    unittest.main()
