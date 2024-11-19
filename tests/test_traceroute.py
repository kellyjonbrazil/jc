import os
import unittest
import json
import jc.parsers.traceroute

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/traceroute.out'), 'r', encoding='utf-8') as f:
        centos_7_7_traceroute = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-no-header.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_noheader = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-asn.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_asn = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-mult-addresses.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_mult_addresses = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-q.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_q = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6-mult-addresses.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute6_mult_addresses = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute6 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/traceroute.out'), 'r', encoding='utf-8') as f:
        freebsd12_traceroute = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/traceroute6.out'), 'r', encoding='utf-8') as f:
        freebsd12_traceroute6 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute1.out'), 'r', encoding='utf-8') as f:
        generic_traceroute1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute2.out'), 'r', encoding='utf-8') as f:
        generic_traceroute2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute3.out'), 'r', encoding='utf-8') as f:
        generic_traceroute3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute4.out'), 'r', encoding='utf-8') as f:
        generic_traceroute4 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute5.out'), 'r', encoding='utf-8') as f:
        generic_traceroute5 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute6.out'), 'r', encoding='utf-8') as f:
        generic_traceroute6 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute7.out'), 'r', encoding='utf-8') as f:
        generic_traceroute7 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute8.out'), 'r', encoding='utf-8') as f:
        generic_traceroute8 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-ipv4.out'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_ipv4 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-q1-ipv4.out'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_q1_ipv4 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-ipv6.out'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_ipv6 = f.read()


    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-no-header.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_no_header_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/traceroute.json'), 'r', encoding='utf-8') as f:
        centos_7_7_traceroute_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-asn.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_asn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-mult-addresses.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_mult_addresses_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-q.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_q_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6-mult-addresses.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute6_mult_addresses_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute6_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/traceroute.json'), 'r', encoding='utf-8') as f:
        freebsd12_traceroute_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/traceroute6.json'), 'r', encoding='utf-8') as f:
        freebsd12_traceroute6_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute1.json'), 'r', encoding='utf-8') as f:
        generic_traceroute1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute2.json'), 'r', encoding='utf-8') as f:
        generic_traceroute2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute3.json'), 'r', encoding='utf-8') as f:
        generic_traceroute3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute4.json'), 'r', encoding='utf-8') as f:
        generic_traceroute4_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute5.json'), 'r', encoding='utf-8') as f:
        generic_traceroute5_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute6.json'), 'r', encoding='utf-8') as f:
        generic_traceroute6_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute7.json'), 'r', encoding='utf-8') as f:
        generic_traceroute7_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute8.json'), 'r', encoding='utf-8') as f:
        generic_traceroute8_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-ipv4.json'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_ipv4_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-q1-ipv4.json'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_q1_ipv4_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-ipv6.json'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_ipv6_json = json.loads(f.read())


    def test_traceroute_nodata(self):
        """
        Test 'traceroute' with no data
        """
        self.assertEqual(jc.parsers.traceroute.parse('', quiet=True), {})

    def test_traceroute_noheader(self):
        """
        Test 'traceroute' with missing header row
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.osx_10_14_6_traceroute_noheader, quiet=True), self.osx_10_14_6_traceroute_no_header_json)

    def test_traceroute_centos_7_7(self):
        """
        Test 'traceroute' on Centos 7.7
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.centos_7_7_traceroute, quiet=True), self.centos_7_7_traceroute_json)

    def test_traceroute_a_osx_10_14_6(self):
        """
        Test 'traceroute -a' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.osx_10_14_6_traceroute_asn, quiet=True), self.osx_10_14_6_traceroute_asn_json)

    def test_traceroute_mult_addresses_osx_10_14_6(self):
        """
        Test 'traceroute' with multiple addresses returned via dns on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.osx_10_14_6_traceroute_mult_addresses, quiet=True), self.osx_10_14_6_traceroute_mult_addresses_json)

    def test_traceroute_q_osx_10_14_6(self):
        """
        Test 'traceroute -q' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.osx_10_14_6_traceroute_q, quiet=True), self.osx_10_14_6_traceroute_q_json)

    def test_traceroute_osx_10_14_6(self):
        """
        Test 'traceroute' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.osx_10_14_6_traceroute, quiet=True), self.osx_10_14_6_traceroute_json)

    def test_traceroute6_mult_addresses_osx_10_14_6(self):
        """
        Test 'traceroute6' with multiple addresses returned via dns on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.osx_10_14_6_traceroute6_mult_addresses, quiet=True), self.osx_10_14_6_traceroute6_mult_addresses_json)

    def test_traceroute6_osx_10_14_6(self):
        """
        Test 'traceroute6' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.osx_10_14_6_traceroute6, quiet=True), self.osx_10_14_6_traceroute6_json)

    def test_traceroute_freebsd12(self):
        """
        Test 'traceroute' on freebsd12
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.freebsd12_traceroute, quiet=True), self.freebsd12_traceroute_json)

    def test_traceroute6_freebsd12(self):
        """
        Test 'traceroute6' on freebsd12
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.freebsd12_traceroute6, quiet=True), self.freebsd12_traceroute6_json)

    def test_traceroute1_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute1, quiet=True), self.generic_traceroute1_json)

    def test_traceroute2_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute2, quiet=True), self.generic_traceroute2_json)

    def test_traceroute3_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute3, quiet=True), self.generic_traceroute3_json)

    def test_traceroute4_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute4, quiet=True), self.generic_traceroute4_json)

    def test_traceroute5_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute5, quiet=True), self.generic_traceroute5_json)

    def test_traceroute6_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute6, quiet=True), self.generic_traceroute6_json)

    def test_traceroute7_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute7, quiet=True), self.generic_traceroute7_json)

    def test_traceroute8_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute8, quiet=True), self.generic_traceroute8_json)

    def test_traceroute_n_ipv4(self):
        """
        Test 'traceroute -n x.x.x.x'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute_n_ipv4, quiet=True), self.generic_traceroute_n_ipv4_json)

    def test_traceroute_n_q1_ipv4(self):
        """
        Test 'traceroute -q1 -n x.x.x.x'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute_n_q1_ipv4, quiet=True), self.generic_traceroute_n_q1_ipv4_json)

    def test_traceroute_n_ipv6(self):
        """
        Test 'traceroute6 -n x::x'
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.generic_traceroute_n_ipv6, quiet=True), self.generic_traceroute_n_ipv6_json)

    def test_traceroute_long_ipv6(self):
        """
        Test 'traceroute6' with a long ipv6 response
        """
        data = '''traceroute6 to turner-tls.map.fastly.net (2a04:4e42:200::323) from 2600:1700:bab0:d40:985:f00a:98bd:f142, 5 hops max, 12 byte packets
 1  * * *
 2  :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::  27.635 ms  20.383 ms  23.438 ms
 3  * * *
 4  2001:1890:ff:ff08:12:242:117:16  20.118 ms  20.327 ms  21.213 ms
 5  * * *'''
        expected = json.loads('''{"destination_ip":"2a04:4e42:200::323","destination_name":"turner-tls.map.fastly.net","hops":[{"hop":1,"probes":[]},{"hop":2,"probes":[{"annotation":null,"asn":null,"ip":null,"name":null,"rtt":27.635},{"annotation":null,"asn":null,"ip":null,"name":null,"rtt":20.383},{"annotation":null,"asn":null,"ip":null,"name":null,"rtt":23.438}]},{"hop":3,"probes":[]},{"hop":4,"probes":[{"annotation":null,"asn":null,"ip":"2001:1890:ff:ff08:12:242:117:16","name":null,"rtt":20.118},{"annotation":null,"asn":null,"ip":"2001:1890:ff:ff08:12:242:117:16","name":null,"rtt":20.327},{"annotation":null,"asn":null,"ip":"2001:1890:ff:ff08:12:242:117:16","name":null,"rtt":21.213}]},{"hop":5,"probes":[]}]}''')
        self.assertEqual(jc.parsers.traceroute.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
