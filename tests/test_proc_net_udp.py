import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_net_udp

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_net_udp': (
                'fixtures/linux-proc/net_udp',
                'fixtures/linux-proc/net_udp.json'),
            'proc_net_udp6': (
                'fixtures/linux-proc/net_udp6',
                'fixtures/linux-proc/net_udp6.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_net_udp_nodata(self):
        """
        Test 'proc_net_udp' with no data
        """
        self.assertEqual(jc.parsers.proc_net_udp.parse('', quiet=True), [])

    def test_proc_net_udp(self):
        """
        Test '/proc/net/udp'
        """
        self.assertEqual(jc.parsers.proc_net_udp.parse(self.f_in['proc_net_udp'], quiet=True),
                                                       self.f_json['proc_net_udp'])

    def test_proc_net_udp_header_only(self):
        """
        Test '/proc/net/udp' with only the header line
        """
        data = self.f_in['proc_net_udp'].split('\n', 1)[0] + '\n'
        self.assertEqual(jc.parsers.proc_net_udp.parse(data, quiet=True), [])

    def test_proc_net_udp6(self):
        """
        Test '/proc/net/udp6'
        """
        self.assertEqual(jc.parsers.proc_net_udp.parse(self.f_in['proc_net_udp6'], quiet=True),
                                                       self.f_json['proc_net_udp6'])


if __name__ == '__main__':
    unittest.main()
