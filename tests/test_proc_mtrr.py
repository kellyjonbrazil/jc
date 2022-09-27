import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_mtrr

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_mtrr': (
                'fixtures/linux-proc/mtrr',
                'fixtures/linux-proc/mtrr.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_mtrr_nodata(self):
        """
        Test 'proc_mtrr' with no data
        """
        self.assertEqual(jc.parsers.proc_mtrr.parse('', quiet=True), [])

    def test_proc_mtrr(self):
        """
        Test '/proc/mtrr'
        """
        self.assertEqual(jc.parsers.proc_mtrr.parse(self.f_in['proc_mtrr'], quiet=True),
                                                    self.f_json['proc_mtrr'])


if __name__ == '__main__':
    unittest.main()
