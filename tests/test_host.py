import os
import unittest
import json
from typing import Dict
from jc.parsers.host import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'google': (
                'fixtures/generic/host-google.out',
                'fixtures/generic/host-google.json'),
            'sunet': (
                'fixtures/generic/host-sunet.out',
                'fixtures/generic/host-sunet.json'),
            'soa': (
                'fixtures/generic/host-soa.out',
                'fixtures/generic/host-soa.json'),
            'txt': (
                'fixtures/generic/host-txt.out',
                'fixtures/generic/host-txt.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())

    # host cannot run without input (will only display help)
    def test_host_nodata(self):
       """
       Test 'host' with no data
       """
       self.assertEqual(parse('', quiet=True), [])


    def test_host_google(self):
        """
        Test 'host google'
        """
        self.assertEqual(
            parse(self.f_in['google'], quiet=True),
            self.f_json['google']
        )

    def test_host_sunet(self):
        """
        Test 'host sunet'
        """
        self.assertEqual(
            parse(self.f_in['sunet'], quiet=True),
            self.f_json['sunet']
        )

    def test_host_soa(self):
        """
        Test 'host -t soa' (a single SOA line is a single record)
        """
        self.assertEqual(
            parse(self.f_in['soa'], quiet=True),
            self.f_json['soa']
        )

    def test_host_txt_record_words(self):
        """
        Test 'host' with TXT text that contains other record type words
        """
        self.assertEqual(
            parse(self.f_in['txt'], quiet=True),
            self.f_json['txt']
        )

    def test_host_soa_c_mode(self):
        """
        Test 'host -C' with multiple nameservers (one record per SOA line)
        """
        data = (
            'Nameserver 192.0.2.1:\n'
            'example.com has SOA record ns1.example.com. admin.example.com. 1 7200 3600 1209600 3600\n'
            'Nameserver 192.0.2.2:\n'
            'example.com has SOA record ns1.example.com. admin.example.com. 2 7200 3600 1209600 3600\n'
        )
        result = parse(data, quiet=True)
        self.assertEqual([x['nameserver'] for x in result], ['192.0.2.1', '192.0.2.2'])
        self.assertEqual([x['serial'] for x in result], [1, 2])

    def test_host_soa_two_lines(self):
        """
        Test 'host -t soa' with two SOA lines (one record per SOA line)
        """
        data = (
            'example.com has SOA record ns1.example.com. admin.example.com. 1 7200 3600 1209600 3600\n'
            'example.com has SOA record ns2.example.com. admin.example.com. 2 7200 3600 1209600 3600\n'
        )
        result = parse(data, quiet=True)
        self.assertEqual([x['mname'] for x in result], ['ns1.example.com.', 'ns2.example.com.'])
        self.assertEqual([x['serial'] for x in result], [1, 2])

    def test_host_C_ipv6_trailing_colons(self):
        """
        Test 'host -C' with nameserver IPv6 addresses that end with '::'
        """
        data = (
            'Nameserver 2001:db8:53::1:\n'
            '\texample.net has SOA record ns1.example.net. hostmaster.example.net. 2024010101 7200 3600 1209600 300\n'
            'Nameserver 2001:db8:53:::\n'
            '\texample.net has SOA record ns1.example.net. hostmaster.example.net. 2024010101 7200 3600 1209600 300\n'
            'Nameserver :::\n'
            '\texample.net has SOA record ns1.example.net. hostmaster.example.net. 2024010101 7200 3600 1209600 300\n'
        )
        result = parse(data, quiet=True)
        self.assertEqual([x['nameserver'] for x in result], ['2001:db8:53::1', '2001:db8:53::', '::'])
        self.assertEqual(result[1]['zone'], 'example.net')
        self.assertEqual(result[1]['serial'], 2024010101)


if __name__ == '__main__':
    unittest.main()
