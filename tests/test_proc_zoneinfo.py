import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_zoneinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_zoneinfo': (
                'fixtures/linux-proc/zoneinfo',
                'fixtures/linux-proc/zoneinfo.json'),
            'proc_zoneinfo2': (
                'fixtures/linux-proc/zoneinfo2',
                'fixtures/linux-proc/zoneinfo2.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_zoneinfo_nodata(self):
        """
        Test 'proc_zoneinfo' with no data
        """
        self.assertEqual(jc.parsers.proc_zoneinfo.parse('', quiet=True), [])

    def test_proc_zoneinfo(self):
        """
        Test '/proc/zoneinfo'
        """
        self.assertEqual(jc.parsers.proc_zoneinfo.parse(self.f_in['proc_zoneinfo'], quiet=True),
                                                        self.f_json['proc_zoneinfo'])

    def test_proc_zoneinfo2(self):
        """
        Test '/proc/zoneinfo' #2
        """
        self.assertEqual(jc.parsers.proc_zoneinfo.parse(self.f_in['proc_zoneinfo2'], quiet=True),
                                                        self.f_json['proc_zoneinfo2'])


if __name__ == '__main__':
    unittest.main()
