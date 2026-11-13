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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-no-jump2.out'), 'r', encoding='utf-8') as f:
        generic_iptables_no_jump2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-chain-header-long.out'), 'r', encoding='utf-8') as f:
        generic_iptables_chain_header_long = f.read()

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-no-jump2.json'), 'r', encoding='utf-8') as f:
        generic_iptables_no_jump2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-chain-header-long.json'), 'r', encoding='utf-8') as f:
        generic_iptables_chain_header_long_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-target-looks-like-header.out'), 'r', encoding='utf-8') as f:
        generic_iptables_target_looks_like_header = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-target-looks-like-header.json'), 'r', encoding='utf-8') as f:
        generic_iptables_target_looks_like_header_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-target-looks-like-header-line-numbers.out'), 'r', encoding='utf-8') as f:
        generic_iptables_target_looks_like_header_line_numbers = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iptables-target-looks-like-header-line-numbers.json'), 'r', encoding='utf-8') as f:
        generic_iptables_target_looks_like_header_line_numbers_json = json.loads(f.read())

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

    def test_iptables_no_jump2_generic(self):
        """
        Test 'sudo iptables' with no jump target and verbose output
        """
        self.assertEqual(jc.parsers.iptables.parse(self.generic_iptables_no_jump2, quiet=True), self.generic_iptables_no_jump2_json)

    def test_iptables_chain_header_long_generic(self):
        """
        Test 'sudo iptables -nvL' with a long chain header line that repeats
        the policy text without closing the counters
        """
        self.assertEqual(jc.parsers.iptables.parse(self.generic_iptables_chain_header_long, quiet=True), self.generic_iptables_chain_header_long_json)

    def test_iptables_chain_header_policy_counters(self):
        """
        Test 'sudo iptables -nvL' chain header policy and counters, including
        a byte counter with a size suffix and headers without counters
        """
        data = '''Chain INPUT (policy DROP 1234 packets, 3456M bytes)
Chain OUTPUT (policy ACCEPT)
Chain DOCKER (2 references)'''
        expected = [
            {'chain': 'INPUT', 'default_policy': 'DROP', 'default_packets': 1234, 'default_bytes': 3456000000, 'rules': []},
            {'chain': 'OUTPUT', 'rules': []},
            {'chain': 'DOCKER', 'rules': []}
        ]
        self.assertEqual(jc.parsers.iptables.parse(data, quiet=True), expected)

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


    def test_iptables_line_separator(self):
        """
        Test 'iptables' with a line-break character other than LF inside a field
        """
        data = 'Chain INPUT (policy DROP)\ntarget     prot opt source               destination\nDROP       all  --  203.0.113.7          anywhere             /* note */\u2028ACCEPT     all  --  anywhere             anywhere             /* ticket 4711 */\n'
        result = jc.parsers.iptables.parse(data, quiet=True)
        self.assertEqual(len(result[0]['rules']), 1)
        self.assertEqual(result[0]['rules'][0]['target'], 'DROP')
        self.assertEqual(result[0]['rules'][0]['source'], '203.0.113.7')
        self.assertEqual(result[0]['rules'][0]['options'], '/* note */\u2028ACCEPT     all  --  anywhere             anywhere             /* ticket 4711 */')

    def test_iptables_target_looks_like_header(self):
        """
        Test 'iptables' with rule targets that look like a header or chain heading
        """
        self.assertEqual(jc.parsers.iptables.parse(self.generic_iptables_target_looks_like_header, quiet=True), self.generic_iptables_target_looks_like_header_json)

    def test_iptables_target_looks_like_header_line_numbers(self):
        """
        Test 'iptables --line-numbers' with rule targets that look like a header or chain heading
        """
        self.assertEqual(jc.parsers.iptables.parse(self.generic_iptables_target_looks_like_header_line_numbers, quiet=True), self.generic_iptables_target_looks_like_header_line_numbers_json)

    def test_iptables_packet_suffixes(self):
        """
        Test 'iptables' with K, M and G suffixes on packet counts and policy packets
        """
        data = (
            'Chain INPUT (policy ACCEPT 1250K packets, 3M bytes)\n'
            ' pkts bytes target     prot opt in     out     source               destination\n'
            ' 1250K  900M ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0\n'
            '   12M   3G DROP       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0\n'
            '   42    10 DROP       udp  --  *      *       0.0.0.0/0            0.0.0.0/0\n'
        )
        result = jc.parsers.iptables.parse(data, quiet=True)
        self.assertEqual(result[0]['default_packets'], 1250000)
        self.assertEqual(result[0]['default_bytes'], 3000000)
        self.assertEqual([r['pkts'] for r in result[0]['rules']], [1250000, 12000000, 42])
        self.assertEqual([r['bytes'] for r in result[0]['rules']], [900000000, 3000000000, 10])

    def test_iptables_blank_target_line_numbers(self):
        """
        Test 'iptables' with a blank target and --line-numbers, with and without -v
        """
        data = (
            'Chain FORWARD (policy ACCEPT)\n'
            'num  target     prot opt source               destination\n'
            '1               all  --  10.0.0.0/8           0.0.0.0/0\n'
            '2    ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:22\n'
        )
        result = jc.parsers.iptables.parse(data, quiet=True)
        rules = result[0]['rules']
        self.assertEqual(rules[0]['num'], 1)
        self.assertIsNone(rules[0]['target'])
        self.assertEqual(rules[0]['prot'], 'all')
        self.assertIsNone(rules[0]['opt'])
        self.assertEqual(rules[0]['source'], '10.0.0.0/8')
        self.assertEqual(rules[0]['destination'], '0.0.0.0/0')
        self.assertEqual(rules[1]['target'], 'ACCEPT')
        self.assertEqual(rules[1]['options'], 'tcp dpt:22')

        data = (
            'Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)\n'
            'num   pkts bytes target     prot opt in     out     source               destination\n'
            '1       10   840            all  --  *      *       10.0.0.0/8           0.0.0.0/0\n'
            '2        5   300 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:22\n'
        )
        result = jc.parsers.iptables.parse(data, quiet=True)
        rules = result[0]['rules']
        self.assertEqual(rules[0]['num'], 1)
        self.assertEqual(rules[0]['pkts'], 10)
        self.assertEqual(rules[0]['bytes'], 840)
        self.assertIsNone(rules[0]['target'])
        self.assertEqual(rules[0]['prot'], 'all')
        self.assertEqual(rules[0]['in'], '*')
        self.assertEqual(rules[0]['source'], '10.0.0.0/8')
        self.assertEqual(rules[1]['target'], 'ACCEPT')
        self.assertEqual(rules[1]['options'], 'tcp dpt:22')

    def test_iptables_target_is_invisible_separator(self):
        """
        Test 'iptables' with a real target that is the invisible separator character
        """
        data = (
            'Chain INPUT (policy ACCEPT)\n'
            'target     prot opt source               destination\n'
            '\u2063          all  --  0.0.0.0/0            0.0.0.0/0\n'
            '           all  --  10.0.0.0/8           0.0.0.0/0\n'
        )
        rules = jc.parsers.iptables.parse(data, quiet=True)[0]['rules']
        self.assertEqual(rules[0]['target'], '\u2063')
        self.assertEqual(rules[0]['source'], '0.0.0.0/0')
        self.assertIsNone(rules[1]['target'])
        self.assertEqual(rules[1]['source'], '10.0.0.0/8')

        data = (
            'Chain INPUT (policy ACCEPT 0 packets, 0 bytes)\n'
            ' pkts bytes target     prot opt in     out     source               destination\n'
            '    1    60 \u2063          all  --  *      *       0.0.0.0/0            0.0.0.0/0\n'
        )
        rules = jc.parsers.iptables.parse(data, quiet=True)[0]['rules']
        self.assertEqual(rules[0]['target'], '\u2063')
        self.assertEqual(rules[0]['source'], '0.0.0.0/0')


if __name__ == '__main__':
    unittest.main()
