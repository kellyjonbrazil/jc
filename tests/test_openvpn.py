import os
import unittest
import json
from typing import Dict
from jc.parsers.openvpn import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'openvpn': (
                'fixtures/generic/openvpn-status.log',
                'fixtures/generic/openvpn-status.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/openvpn-status-marker-names.log'), 'r', encoding='utf-8') as f:
        f_marker_in = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/openvpn-status-marker-names.json'), 'r', encoding='utf-8') as f:
        f_marker_json = json.loads(f.read())

    def test_openvpn_nodata(self):
        """
        Test 'openvpn' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_openvpn(self):
        """
        Test 'openvpn'
        """
        self.assertEqual(
            parse(self.f_in['openvpn'], quiet=True),
            self.f_json['openvpn']
        )


    def test_openvpn_line_separator(self):
        """
        Test 'openvpn' with a line-break character other than LF inside a field
        """
        data = 'OpenVPN CLIENT LIST\nUpdated,Thu Jun 18 08:12:15 2015\nCommon Name,Real Address,Bytes Received,Bytes Sent,Connected Since\nfoo@example.com,10.0.0.5:1194,9,9,Thu Jun 18 08:00:00 2015\u2028x,203.0.113.9:40000,3512,3801,Thu Jun 18 08:11:00 2015\nROUTING TABLE\nVirtual Address,Common Name,Real Address,Last Ref\nGLOBAL STATS\nMax bcast/mcast queue length,0\nEND\n'
        result = parse(data, quiet=True)
        self.assertEqual(len(result['clients']), 1)
        self.assertEqual(result['clients'][0]['common_name'], 'foo@example.com')
        self.assertEqual(result['clients'][0]['real_address'], '10.0.0.5')
        self.assertEqual(result['clients'][0]['connected_since'], 'Thu Jun 18 08:00:00 2015\u2028x,203.0.113.9:40000,3512,3801,Thu Jun 18 08:11:00 2015')


    def test_openvpn_marker_names(self):
        """
        Test 'openvpn' with common names that start with a section name
        """
        self.assertEqual(parse(self.f_marker_in, quiet=True), self.f_marker_json)



if __name__ == '__main__':
    unittest.main()
