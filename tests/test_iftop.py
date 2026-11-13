import os
import unittest
import json
import jc.parsers.iftop

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n1.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n3.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n1-noport.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n1_noport = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-truncated-lines.out'), 'r', encoding='utf-8') as f:
        generic_iftop_truncated_lines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-b-n1-unmatched-send.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n1_unmatched_send = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-repeated-separators.out'), 'r', encoding='utf-8') as f:
        generic_iftop_repeated_separators = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n1.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n3.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n1-noport.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n1_noport_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-truncated-lines.json'), 'r', encoding='utf-8') as f:
        generic_iftop_truncated_lines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-b-n1-unmatched-send.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n1_unmatched_send_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-repeated-separators.json'), 'r', encoding='utf-8') as f:
        generic_iftop_repeated_separators_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-port-service-name.out'), 'r', encoding='utf-8') as f:
        generic_iftop_port_service_name = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-port-service-name.json'), 'r', encoding='utf-8') as f:
        generic_iftop_port_service_name_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-linux-no-port-flows.out'), 'r', encoding='utf-8') as f:
        generic_iftop_linux_no_port_flows = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-linux-no-port-flows.json'), 'r', encoding='utf-8') as f:
        generic_iftop_linux_no_port_flows_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-linux-ipv6-no-port.out'), 'r', encoding='utf-8') as f:
        generic_iftop_linux_ipv6_no_port = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iftop-linux-ipv6-no-port.json'), 'r', encoding='utf-8') as f:
        generic_iftop_linux_ipv6_no_port_json = json.loads(f.read())

    def test_iftop_nodata(self):
        """
        Test 'iftop -b' with no data
        """
        self.assertEqual(jc.parsers.iftop.parse('', quiet=True), [])

    def test_iftop_ubuntu_20_10(self):
        """
        Test 'iftop -i <device> -t -P -s 1' with units as MiB on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iftop.parse(self.ubuntu_20_10_iftop_b_n1, quiet=True), self.ubuntu_20_10_iftop_b_n1_json)

    def test_iftop_multiple_runs_ubuntu_20_10(self):
        """
        Test 'iftop -i <device> -t -P -s 1' with units as MiB on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iftop.parse(self.ubuntu_20_10_iftop_b_n3, quiet=True), self.ubuntu_20_10_iftop_b_n3_json)

    def test_iftop_ubuntu_20_10_no_port(self):
        """
        Test 'iftop -i <device> -t -B -s 1' with units as MiB on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iftop.parse(self.ubuntu_20_10_iftop_b_n1_noport, quiet=True), self.ubuntu_20_10_iftop_b_n1_noport_json)

    def test_iftop_truncated_lines(self):
        """
        Test 'iftop -t -P' output with a flow line that is only padding before
        the arrow and a flow line with a long host field and no rate columns
        """
        self.assertEqual(jc.parsers.iftop.parse(self.generic_iftop_truncated_lines, quiet=True), self.generic_iftop_truncated_lines_json)

    def test_iftop_unmatched_send_line(self):
        """
        Test 'iftop -t -P' with a send line that cannot be parsed: its receive
        line is ignored and the previous client is not repeated
        """
        self.assertEqual(jc.parsers.iftop.parse(self.ubuntu_20_10_iftop_b_n1_unmatched_send, quiet=True), self.ubuntu_20_10_iftop_b_n1_unmatched_send_json)

    def test_iftop_unmatched_first_send_line(self):
        """
        Test 'iftop -t -P' where the very first send line cannot be parsed
        """
        lines = self.ubuntu_20_10_iftop_b_n1.splitlines()
        lines[6] = '   1 ubuntu-2004-clean-01:ssh                 =>'
        result = jc.parsers.iftop.parse('\n'.join(lines), quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['clients'], [])

    def test_iftop_repeated_separators(self):
        """
        Test 'iftop -t -P' with repeated '=' separator lines, an interface
        name containing a colon and an IPv6 address
        """
        self.assertEqual(jc.parsers.iftop.parse(self.generic_iftop_repeated_separators, quiet=True), self.generic_iftop_repeated_separators_json)
        self.assertEqual(len(jc.parsers.iftop.parse(self.generic_iftop_repeated_separators, raw=True, quiet=True)), 1)

    def test_iftop_host_port_split(self):
        """
        Test 'iftop -t -P' splits host and port at the last colon of the host
        field, including IPv6 addresses and a host field that ends in a colon
        """
        cases = [
            ('2001:db8::1:https', '[2001:db8::5]:443', ('2001:db8::1', 'https'), ('2001:db8::5', '443')),
            ('fe80::1:ssh', 'fe80::2:40876', ('fe80::1', 'ssh'), ('fe80::2', '40876')),
            ('a:b:', 'host:http', ('a', 'b:'), ('host', 'http'))
        ]

        for send_host, receive_host, send_expected, receive_expected in cases:
            with self.subTest(send_host):
                lines = self.ubuntu_20_10_iftop_b_n1.splitlines()
                lines[6] = '   1 ' + send_host + '                 =>       448b       448b       448b       112B'
                lines[7] = '     ' + receive_host + '                    <=       208b       208b       208b        52B'
                connections = jc.parsers.iftop.parse('\n'.join(lines), quiet=True)[0]['clients'][0]['connections']
                self.assertEqual((connections[0]['host_name'], connections[0]['host_port']), send_expected)
                self.assertEqual((connections[1]['host_name'], connections[1]['host_port']), receive_expected)

    def test_iftop_port_service_name(self):
        """
        Test 'iftop' with receive lines whose port is a service name containing a hyphen
        """
        self.assertEqual(jc.parsers.iftop.parse(self.generic_iftop_port_service_name, quiet=True), self.generic_iftop_port_service_name_json)

    def test_iftop_no_port_flows(self):
        """
        Test 'iftop -t -P' output where one flow is printed without ports
        between flows that have ports
        """
        self.assertEqual(jc.parsers.iftop.parse(self.generic_iftop_linux_no_port_flows, quiet=True), self.generic_iftop_linux_no_port_flows_json)

    def test_iftop_ipv6_no_port(self):
        """
        Test 'iftop -t -P' output with IPv6 addresses printed without a port
        next to bracketed IPv6 addresses that have a port
        """
        self.assertEqual(jc.parsers.iftop.parse(self.generic_iftop_linux_ipv6_no_port, quiet=True), self.generic_iftop_linux_ipv6_no_port_json)

    def test_iftop_aggregated_hosts(self):
        """
        Test 'iftop -t' with hide-source or hide-destination, which prints the hidden host as '*'
        """
        for send_host, receive_host, send_expected, receive_expected in (
                (' * :ssh                ', '10.10.15.72:40876      ', ('*', 'ssh'), ('10.10.15.72', '40876')),
                ('ubuntu-2004-clean-01:ssh', ' * :40876              ', ('ubuntu-2004-clean-01', 'ssh'), ('*', '40876')),
                (' *                     ', ' *                     ', ('*', None), ('*', None)),
                ('[ * ]:22               ', '[2001:db8::1]:40876    ', ('*', '22'), ('2001:db8::1', '40876'))):
            with self.subTest(send_host=send_host, receive_host=receive_host):
                lines = self.ubuntu_20_10_iftop_b_n1.splitlines()
                lines[6] = '   1 ' + send_host + '                 =>       448b       448b       448b       112B'
                lines[7] = '     ' + receive_host + '                    <=       208b       208b       208b        52B'
                connections = jc.parsers.iftop.parse('\n'.join(lines), quiet=True)[0]['clients'][0]['connections']
                self.assertEqual((connections[0]['host_name'], connections[0].get('host_port')), send_expected)
                self.assertEqual((connections[1]['host_name'], connections[1].get('host_port')), receive_expected)
                self.assertEqual((connections[0]['last_2s'], connections[1]['cumulative']), (448, 52))


if __name__ == '__main__':
    unittest.main()
