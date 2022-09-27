import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_uptime

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_uptime': (
                'fixtures/linux-proc/uptime',
                'fixtures/linux-proc/uptime.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_uptime_nodata(self):
        """
        Test 'proc_uptime' with no data
        """
        self.assertEqual(jc.parsers.proc_uptime.parse('', quiet=True), {})

    def test_proc_uptime(self):
        """
        Test '/proc/uptime'
        """
        self.assertEqual(jc.parsers.proc_uptime.parse(self.f_in['proc_uptime'], quiet=True),
                                                      self.f_json['proc_uptime'])


if __name__ == '__main__':
    unittest.main()
