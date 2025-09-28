import os
import unittest
import json
import jc.parsers.traceroute_s

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-long-ipv6.out'), 'r', encoding='utf-8') as f:
        generic_traceroute_long_ipv6 = f.read()


    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-no-header-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_no_header_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/traceroute-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_traceroute_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-asn-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_asn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-mult-addresses-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_mult_addresses_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-q-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_q_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6-mult-addresses-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute6_mult_addresses_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_traceroute6_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/traceroute-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_traceroute_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/traceroute6-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_traceroute6_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute1-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute2-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute3-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute4-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute4_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute5-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute5_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute6-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute6_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute7-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute7_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute8-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute8_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-ipv4-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_ipv4_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-q1-ipv4-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_q1_ipv4_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-n-ipv6-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute_n_ipv6_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/traceroute-long-ipv6-streaming.json'), 'r', encoding='utf-8') as f:
        generic_traceroute_long_ipv6_json = json.loads(f.read())


    def test_traceroute_s_nodata(self):
        """
        Test 'traceroute' with no data
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse([], quiet=True)), [])

    def test_traceroute_s_noheader(self):
        """
        Test 'traceroute' with missing header row
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.osx_10_14_6_traceroute_noheader.splitlines(), quiet=True)), self.osx_10_14_6_traceroute_no_header_json)

    def test_traceroute_s_centos_7_7(self):
        """
        Test 'traceroute' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.centos_7_7_traceroute.splitlines(), quiet=True)), self.centos_7_7_traceroute_json)

    def test_traceroute_s_a_osx_10_14_6(self):
        """
        Test 'traceroute -a' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.osx_10_14_6_traceroute_asn.splitlines(), quiet=True)), self.osx_10_14_6_traceroute_asn_json)

    def test_traceroute_s_mult_addresses_osx_10_14_6(self):
        """
        Test 'traceroute' with multiple addresses returned via dns on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.osx_10_14_6_traceroute_mult_addresses.splitlines(), quiet=True)), self.osx_10_14_6_traceroute_mult_addresses_json)

    def test_traceroute_s_q_osx_10_14_6(self):
        """
        Test 'traceroute -q' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.osx_10_14_6_traceroute_q.splitlines(), quiet=True)), self.osx_10_14_6_traceroute_q_json)

    def test_traceroute_s_osx_10_14_6(self):
        """
        Test 'traceroute' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.osx_10_14_6_traceroute.splitlines(), quiet=True)), self.osx_10_14_6_traceroute_json)

    def test_traceroute_s6_mult_addresses_osx_10_14_6(self):
        """
        Test 'traceroute6' with multiple addresses returned via dns on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.osx_10_14_6_traceroute6_mult_addresses.splitlines(), quiet=True)), self.osx_10_14_6_traceroute6_mult_addresses_json)

    def test_traceroute_s6_osx_10_14_6(self):
        """
        Test 'traceroute6' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.osx_10_14_6_traceroute6.splitlines(), quiet=True)), self.osx_10_14_6_traceroute6_json)

    def test_traceroute_s_freebsd12(self):
        """
        Test 'traceroute' on freebsd12
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.freebsd12_traceroute.splitlines(), quiet=True)), self.freebsd12_traceroute_json)

    def test_traceroute_s6_freebsd12(self):
        """
        Test 'traceroute6' on freebsd12
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.freebsd12_traceroute6.splitlines(), quiet=True)), self.freebsd12_traceroute6_json)

    def test_traceroute_s1_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute1.splitlines(), quiet=True)), self.generic_traceroute1_json)

    def test_traceroute_s2_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute2.splitlines(), quiet=True)), self.generic_traceroute2_json)

    def test_traceroute_s3_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute3.splitlines(), quiet=True)), self.generic_traceroute3_json)

    def test_traceroute_s4_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute4.splitlines(), quiet=True)), self.generic_traceroute4_json)

    def test_traceroute_s5_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute5.splitlines(), quiet=True)), self.generic_traceroute5_json)

    def test_traceroute_s6_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute6.splitlines(), quiet=True)), self.generic_traceroute6_json)

    def test_traceroute_s7_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute7.splitlines(), quiet=True)), self.generic_traceroute7_json)

    def test_traceroute_s8_generic(self):
        """
        Test 'traceroute'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute8.splitlines(), quiet=True)), self.generic_traceroute8_json)

    def test_traceroute_s_n_ipv4(self):
        """
        Test 'traceroute -n x.x.x.x'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute_n_ipv4.splitlines(), quiet=True)), self.generic_traceroute_n_ipv4_json)

    def test_traceroute_s_n_q1_ipv4(self):
        """
        Test 'traceroute -q1 -n x.x.x.x'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute_n_q1_ipv4.splitlines(), quiet=True)), self.generic_traceroute_n_q1_ipv4_json)

    def test_traceroute_s_n_ipv6(self):
        """
        Test 'traceroute6 -n x::x'
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute_n_ipv6.splitlines(), quiet=True)), self.generic_traceroute_n_ipv6_json)

    def test_traceroute_s_long_ipv6(self):
        """
        Test 'traceroute6' with a long ipv6 response
        """
        self.assertEqual(list(jc.parsers.traceroute_s.parse(self.generic_traceroute_long_ipv6.splitlines(), quiet=True)), self.generic_traceroute_long_ipv6_json)


if __name__ == '__main__':
    unittest.main()
