import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_stat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_stat': (
                'fixtures/linux-proc/stat',
                'fixtures/linux-proc/stat.json'),
            'proc_stat2': (
                'fixtures/linux-proc/stat2',
                'fixtures/linux-proc/stat2.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_stat_nodata(self):
        """
        Test 'proc_stat' with no data
        """
        self.assertEqual(jc.parsers.proc_stat.parse('', quiet=True), {})

    def test_proc_stat(self):
        """
        Test '/proc/stat'
        """
        self.assertEqual(jc.parsers.proc_stat.parse(self.f_in['proc_stat'], quiet=True),
                                                    self.f_json['proc_stat'])

    def test_proc_stat2(self):
        """
        Test '/proc/stat' #2
        """
        self.assertEqual(jc.parsers.proc_stat.parse(self.f_in['proc_stat2'], quiet=True),
                                                    self.f_json['proc_stat2'])


if __name__ == '__main__':
    unittest.main()
