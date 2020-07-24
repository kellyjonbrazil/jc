import os
import unittest
import json
import jc.parsers.traceroute

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/traceroute.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_traceroute = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-no-header.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_noheader = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-asn.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_asn = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-mult-addresses.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_mult_addresses = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-q.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_q = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6-mult-addresses.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute6_mult_addresses = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute6 = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/traceroute.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_traceroute_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-asn.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_asn_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-mult-addresses.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_mult_addresses_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-q.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_q_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6-mult-addresses.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute6_mult_addresses_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute6.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute6_json = json.loads(f.read())

    def test_traceroute_nodata(self):
        """
        Test 'traceroute' with no data
        """
        self.assertEqual(jc.parsers.traceroute.parse('', quiet=True), {})

    def test_traceroute_noheader(self):
        """
        Test 'traceroute' with missing header row. Should generate a ParseError exception
        """
        self.assertRaises(jc.parsers.traceroute.ParseError, jc.parsers.traceroute.parse, self.osx_10_14_6_traceroute_noheader)

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


if __name__ == '__main__':
    unittest.main()
