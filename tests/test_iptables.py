import os
import json
import unittest
import jc.parsers.iptables

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_filter = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_filter = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-line-numbers.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_filter_line_numbers = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-line-numbers.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_filter_line_numbers = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-nv.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_filter_nv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-nv.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_filter_nv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-mangle.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_mangle = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-mangle.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_mangle = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-nat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_nat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-nat.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_nat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-raw.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_raw = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-raw.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_raw = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-no-jump.out'), 'r', encoding='utf-8') as f:
        generic_iptables_no_jump = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_filter_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_filter_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-line-numbers.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_filter_line_numbers_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-line-numbers.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_filter_line_numbers_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-nv.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_filter_nv_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-nv.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_filter_nv_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-mangle.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_mangle_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-mangle.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_mangle_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-nat.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_nat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-nat.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_nat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-raw.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iptables_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-raw.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iptables_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-no-jump.json'), 'r', encoding='utf-8') as f:
        generic_iptables_no_jump_json = json.loads(f.read())


    def test_iptables_nodata(self):
        """
        Test 'sudo iptables' with no data
        """
        self.assertEqual(jc.parsers.iptables.parse('', quiet=True), [])

    def test_iptables_filter_centos_7_7(self):
        """
        Test 'sudo iptables -L -t filter' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_filter, quiet=True), self.centos_7_7_iptables_filter_json)

    def test_iptables_filter_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t filter' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_filter, quiet=True), self.ubuntu_18_4_iptables_filter_json)

    def test_iptables_filter_line_numbers_centos_7_7(self):
        """
        Test 'sudo iptables --line-numbers -L -t filter' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_filter_line_numbers, quiet=True), self.centos_7_7_iptables_filter_line_numbers_json)

    def test_iptables_filter_line_numbers_ubuntu_18_4(self):
        """
        Test 'sudo iptables --line-numbers -L -t filter' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_filter_line_numbers, quiet=True), self.ubuntu_18_4_iptables_filter_line_numbers_json)

    def test_iptables_filter_nv_centos_7_7(self):
        """
        Test 'sudo iptables -nvL -t filter' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_filter_nv, quiet=True), self.centos_7_7_iptables_filter_nv_json)

    def test_iptables_filter_nv_ubuntu_18_4(self):
        """
        Test 'sudo iptables -nvL -t filter' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_filter_nv, quiet=True), self.ubuntu_18_4_iptables_filter_nv_json)

    def test_iptables_mangle_centos_7_7(self):
        """
        Test 'sudo iptables -L -t mangle' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_mangle, quiet=True), self.centos_7_7_iptables_mangle_json)

    def test_iptables_mangle_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t mangle' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_mangle, quiet=True), self.ubuntu_18_4_iptables_mangle_json)

    def test_iptables_nat_centos_7_7(self):
        """
        Test 'sudo iptables -L -t nat' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_nat, quiet=True), self.centos_7_7_iptables_nat_json)

    def test_iptables_nat_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t nat' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_nat, quiet=True), self.ubuntu_18_4_iptables_nat_json)

    def test_iptables_raw_centos_7_7(self):
        """
        Test 'sudo iptables -L -t raw' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_raw, quiet=True), self.centos_7_7_iptables_raw_json)

    def test_iptables_raw_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t raw' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_raw, quiet=True), self.ubuntu_18_4_iptables_raw_json)

    def test_iptables_no_jump_generic(self):
        """
        Test 'sudo iptables' with no jump target
        """
        self.assertEqual(jc.parsers.iptables.parse(self.generic_iptables_no_jump, quiet=True), self.generic_iptables_no_jump_json)

    def test_iptables_x_option_format(self):
        """
        Test iptables -x
        """
        data = '''Chain DOCKER-ISOLATION-STAGE-2 (4 references)
  pkts              bytes target     prot opt in     out     source               destination
       0        0 DROP       all  --  any    docker0  anywhere             anywhere
       0        0 DROP       all  --  any    br-b01fa3a90d3b  anywhere             anywhere
       0        0 DROP       all  --  any    br-642643a59593  anywhere             anywhere
       0        0 DROP       all  --  any    br-3e698d2f6bc4  anywhere             anywhere
44758639 38517421321 RETURN     all  --  any    any     anywhere             anywhere'''
        expected = [{"chain":"DOCKER-ISOLATION-STAGE-2","rules":[{"pkts":0,"bytes":0,"target":"DROP","prot":"all","opt":None,"in":"any","out":"docker0","source":"anywhere","destination":"anywhere"},{"pkts":0,"bytes":0,"target":"DROP","prot":"all","opt":None,"in":"any","out":"br-b01fa3a90d3b","source":"anywhere","destination":"anywhere"},{"pkts":0,"bytes":0,"target":"DROP","prot":"all","opt":None,"in":"any","out":"br-642643a59593","source":"anywhere","destination":"anywhere"},{"pkts":0,"bytes":0,"target":"DROP","prot":"all","opt":None,"in":"any","out":"br-3e698d2f6bc4","source":"anywhere","destination":"anywhere"},{"pkts":44758639,"bytes":38517421321,"target":"RETURN","prot":"all","opt":None,"in":"any","out":"any","source":"anywhere","destination":"anywhere"}]}]
        self.assertEqual(jc.parsers.iptables.parse(data, quiet=True), expected)

    def test_iptables_x_option_format2(self):
        """
        Test iptables -x
        """
        data = '''Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
    pkts      bytes target     prot opt in     out     source               destination
11291792498 217331852907122 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
  555958 33533576 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0
128628404869 172804745659762 INPUT_direct  all  --  *      *       0.0.0.0/0            0.0.0.0/0
128627559128 172804718596050 INPUT_ZONES_SOURCE  all  --  *      *       0.0.0.0/0            0.0.0.0/0
128627559125 172804718595966 INPUT_ZONES  all  --  *      *       0.0.0.0/0            0.0.0.0/0
   26599  1082920 DROP       all  --  *      *       0.0.0.0/0            0.0.0.0/0            ctstate INVALID
    1761    79571 REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            reject-with icmp-host-prohibited'''
        expected = [{'chain': 'INPUT', 'default_policy': 'ACCEPT', 'default_packets': 0, 'default_bytes': 0, 'rules': [{'pkts': 11291792498, 'bytes': 217331852907122, 'target': 'ACCEPT', 'prot': 'all', 'opt': None, 'in': '*', 'out': '*', 'source': '0.0.0.0/0', 'destination': '0.0.0.0/0', 'options': 'ctstate RELATED,ESTABLISHED'}, {'pkts': 555958, 'bytes': 33533576, 'target': 'ACCEPT', 'prot': 'all', 'opt': None, 'in': 'lo', 'out': '*', 'source': '0.0.0.0/0', 'destination': '0.0.0.0/0'}, {'pkts': 128628404869, 'bytes': 172804745659762, 'target': 'INPUT_direct', 'prot': 'all', 'opt': None, 'in': '*', 'out': '*', 'source': '0.0.0.0/0', 'destination': '0.0.0.0/0'}, {'pkts': 128627559128, 'bytes': 172804718596050, 'target': 'INPUT_ZONES_SOURCE', 'prot': 'all', 'opt': None, 'in': '*', 'out': '*', 'source': '0.0.0.0/0', 'destination': '0.0.0.0/0'}, {'pkts': 128627559125, 'bytes': 172804718595966, 'target': 'INPUT_ZONES', 'prot': 'all', 'opt': None, 'in': '*', 'out': '*', 'source': '0.0.0.0/0', 'destination': '0.0.0.0/0'}, {'pkts': 26599, 'bytes': 1082920, 'target': 'DROP', 'prot': 'all', 'opt': None, 'in': '*', 'out': '*', 'source': '0.0.0.0/0', 'destination': '0.0.0.0/0', 'options': 'ctstate INVALID'}, {'pkts': 1761, 'bytes': 79571, 'target': 'REJECT', 'prot': 'all', 'opt': None, 'in': '*', 'out': '*', 'source': '0.0.0.0/0', 'destination': '0.0.0.0/0', 'options': 'reject-with icmp-host-prohibited'}]}]
        self.assertEqual(jc.parsers.iptables.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
