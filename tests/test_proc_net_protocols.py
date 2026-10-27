import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_net_protocols

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_net_protocols': (
                'fixtures/linux-proc/net_protocols',
                'fixtures/linux-proc/net_protocols.json'),
            'proc_net_protocols2': (
                'fixtures/linux-proc/net_protocols2',
                'fixtures/linux-proc/net_protocols2.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_net_protocols_nodata(self):
        """
        Test 'proc_net_protocols' with no data
        """
        self.assertEqual(jc.parsers.proc_net_protocols.parse('', quiet=True), [])

    def test_proc_net_protocols(self):
        """
        Test '/proc/net/protocols'
        """
        self.assertEqual(jc.parsers.proc_net_protocols.parse(self.f_in['proc_net_protocols'], quiet=True),
                                                             self.f_json['proc_net_protocols'])

    def test_proc_net_protocols2(self):
        """
        Test '/proc/net/protocols' from kernel 6.5 or later (no "sp" column)
        """
        self.assertEqual(jc.parsers.proc_net_protocols.parse(self.f_in['proc_net_protocols2'], quiet=True),
                                                             self.f_json['proc_net_protocols2'])


if __name__ == '__main__':
    unittest.main()
