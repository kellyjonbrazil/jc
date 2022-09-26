import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_net_ipv6_route

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_net_ipv6_route': (
                'fixtures/linux-proc/net_ipv6_route',
                'fixtures/linux-proc/net_ipv6_route.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_net_ipv6_route_nodata(self):
        """
        Test 'proc_net_ipv6_route' with no data
        """
        self.assertEqual(jc.parsers.proc_net_ipv6_route.parse('', quiet=True), [])

    def test_proc_net_ipv6_route(self):
        """
        Test '/proc/net/ipv6_route'
        """
        self.assertEqual(jc.parsers.proc_net_ipv6_route.parse(self.f_in['proc_net_ipv6_route'], quiet=True),
                                                              self.f_json['proc_net_ipv6_route'])


if __name__ == '__main__':
    unittest.main()
