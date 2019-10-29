import os
import unittest
import jc.parsers.iptables

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter.out'), 'r') as f:
            self.centos_7_7_iptables_filter = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter.out'), 'r') as f:
            self.ubuntu_18_4_iptables_filter = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-nv.out'), 'r') as f:
            self.centos_7_7_iptables_filter_nv = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-nv.out'), 'r') as f:
            self.ubuntu_18_4_iptables_filter_nv = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-mangle.out'), 'r') as f:
            self.centos_7_7_iptables_mangle = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-mangle.out'), 'r') as f:
            self.ubuntu_18_4_iptables_mangle = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-nat.out'), 'r') as f:
            self.centos_7_7_iptables_nat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-nat.out'), 'r') as f:
            self.ubuntu_18_4_iptables_nat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-raw.out'), 'r') as f:
            self.centos_7_7_iptables_raw = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-raw.out'), 'r') as f:
            self.ubuntu_18_4_iptables_raw = f.read()

    def test_iptables_filter_centos_7_7(self):
        """
        Test 'sudo iptables -L -t filter' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_filter)[2], {'chain': 'OUTPUT',
                                                                                         'rules': [{'target': 'ACCEPT',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere'},
                                                                                                   {'target': 'OUTPUT_direct',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere'},
                                                                                                   {'target': 'ACCEPT',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere'},
                                                                                                   {'target': 'ACCEPT',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere',
                                                                                                    'options': 'ctstate ESTABLISHED'},
                                                                                                   {'target': 'ACCEPT',
                                                                                                    'prot': 'tcp',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere',
                                                                                                    'options': 'tcp spt:ssh ctstate ESTABLISHED'},
                                                                                                   {'target': 'ACCEPT',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere'},
                                                                                                   {'target': 'ACCEPT',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere',
                                                                                                    'options': 'ctstate ESTABLISHED'},
                                                                                                   {'target': 'ACCEPT',
                                                                                                    'prot': 'tcp',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere',
                                                                                                    'options': 'tcp spt:ssh ctstate ESTABLISHED'}]})

    def test_iptables_filter_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t filter' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_filter)[0], {'chain': 'INPUT',
                                                                                          'rules': [{'target': 'ACCEPT',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere'},
                                                                                                    {'target': 'ACCEPT',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'ctstate RELATED,ESTABLISHED'},
                                                                                                    {'target': 'DROP',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'ctstate INVALID'},
                                                                                                    {'target': 'ACCEPT',
                                                                                                     'prot': 'tcp',
                                                                                                     'opt': '--',
                                                                                                     'source': '15.15.15.0/24',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'tcp dpt:ssh ctstate NEW,ESTABLISHED'},
                                                                                                    {'target': 'ACCEPT',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere'},
                                                                                                    {'target': 'ACCEPT',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'ctstate RELATED,ESTABLISHED'},
                                                                                                    {'target': 'DROP',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'ctstate INVALID'},
                                                                                                    {'target': 'ACCEPT',
                                                                                                     'prot': 'tcp',
                                                                                                     'opt': '--',
                                                                                                     'source': '15.15.15.0/24',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'tcp dpt:ssh ctstate NEW,ESTABLISHED'},
                                                                                                    {'target': 'ACCEPT',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere'},
                                                                                                    {'target': 'ACCEPT',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'ctstate RELATED,ESTABLISHED'},
                                                                                                    {'target': 'DROP',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': 'anywhere',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'ctstate INVALID'},
                                                                                                    {'target': 'DROP',
                                                                                                     'prot': 'all',
                                                                                                     'opt': '--',
                                                                                                     'source': '15.15.15.51',
                                                                                                     'destination': 'anywhere'},
                                                                                                    {'target': 'ACCEPT',
                                                                                                     'prot': 'tcp',
                                                                                                     'opt': '--',
                                                                                                     'source': '15.15.15.0/24',
                                                                                                     'destination': 'anywhere',
                                                                                                     'options': 'tcp dpt:ssh ctstate NEW,ESTABLISHED'}]})

    def test_iptables_filter_nv_centos_7_7(self):
        """
        Test 'sudo iptables -nvL -t filter' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_filter_nv)[4], {'chain': 'DOCKER-ISOLATION',
                                                                                            'rules': [{'pkts': '0',
                                                                                                       'bytes': '0',
                                                                                                       'target': 'RETURN',
                                                                                                       'prot': 'all',
                                                                                                       'opt': '--',
                                                                                                       'in': '*',
                                                                                                       'out': '*',
                                                                                                       'source': '0.0.0.0/0',
                                                                                                       'destination': '0.0.0.0/0'}]})

    def test_iptables_filter_nv_ubuntu_18_4(self):
        """
        Test 'sudo iptables -nvL -t filter' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_filter_nv)[0]['rules'][3], {'pkts': '0',
                                                                                                         'bytes': '0',
                                                                                                         'target': 'ACCEPT',
                                                                                                         'prot': 'tcp',
                                                                                                         'opt': '--',
                                                                                                         'in': '*',
                                                                                                         'out': '*',
                                                                                                         'source': '15.15.15.0/24',
                                                                                                         'destination': '0.0.0.0/0',
                                                                                                         'options': 'tcp dpt:22 ctstate NEW,ESTABLISHED'})

    def test_iptables_mangle_centos_7_7(self):
        """
        Test 'sudo iptables -L -t mangle' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_mangle)[0], {'chain': 'PREROUTING',
                                                                                         'rules': [{'target': 'PREROUTING_direct',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere'},
                                                                                                   {'target': 'PREROUTING_ZONES_SOURCE',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere'},
                                                                                                   {'target': 'PREROUTING_ZONES',
                                                                                                    'prot': 'all',
                                                                                                    'opt': '--',
                                                                                                    'source': 'anywhere',
                                                                                                    'destination': 'anywhere'}]})

    def test_iptables_mangle_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t mangle' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_mangle), [{'chain': 'PREROUTING',
                                                                                        'rules': []},
                                                                                       {'chain': 'INPUT',
                                                                                        'rules': []},
                                                                                       {'chain': 'FORWARD',
                                                                                        'rules': []},
                                                                                       {'chain': 'OUTPUT',
                                                                                        'rules': []}])

    def test_iptables_nat_centos_7_7(self):
        """
        Test 'sudo iptables -L -t nat' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_nat)[3], {'chain': 'POSTROUTING',
                                                                                      'rules': [{'target': 'MASQUERADE',
                                                                                                 'prot': 'all',
                                                                                                 'opt': '--',
                                                                                                 'source': '172.17.0.0/16',
                                                                                                 'destination': 'anywhere'},
                                                                                                {'target': 'POSTROUTING_direct',
                                                                                                 'prot': 'all',
                                                                                                 'opt': '--',
                                                                                                 'source': 'anywhere',
                                                                                                 'destination': 'anywhere'},
                                                                                                {'target': 'POSTROUTING_ZONES_SOURCE',
                                                                                                 'prot': 'all',
                                                                                                 'opt': '--',
                                                                                                 'source': 'anywhere',
                                                                                                 'destination': 'anywhere'},
                                                                                                {'target': 'POSTROUTING_ZONES',
                                                                                                 'prot': 'all',
                                                                                                 'opt': '--',
                                                                                                 'source': 'anywhere',
                                                                                                 'destination': 'anywhere'}]})

    def test_iptables_nat_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t nat' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_nat), [{'chain': 'PREROUTING',
                                                                                     'rules': []},
                                                                                    {'chain': 'INPUT',
                                                                                     'rules': []},
                                                                                    {'chain': 'OUTPUT',
                                                                                     'rules': []}])

    def test_iptables_raw_centos_7_7(self):
        """
        Test 'sudo iptables -L -t raw' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_raw)[3], {'chain': 'PREROUTING_ZONES',
                                                                                      'rules': [{'target': 'PRE_public',
                                                                                                 'prot': 'all',
                                                                                                 'opt': '--',
                                                                                                 'source': 'anywhere',
                                                                                                 'destination': 'anywhere',
                                                                                                 'options': '[goto] '},
                                                                                                {'target': 'PRE_public',
                                                                                                 'prot': 'all',
                                                                                                 'opt': '--',
                                                                                                 'source': 'anywhere',
                                                                                                 'destination': 'anywhere',
                                                                                                 'options': '[goto] '}]})

    def test_iptables_raw_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t raw' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_raw), [{'chain': 'PREROUTING',
                                                                                     'rules': []}])


if __name__ == '__main__':
    unittest.main()
