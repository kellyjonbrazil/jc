import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_buddyinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_buddyinfo': (
                'fixtures/linux-proc/buddyinfo',
                'fixtures/linux-proc/buddyinfo.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as f:
                cls.f_in[file] = f.read()

            with open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as f:
                cls.f_json[file] = json.loads(f.read())


    def test_proc_buddyinfo_nodata(self):
        """
        Test 'proc_buddyinfo' with no data
        """
        self.assertEqual(jc.parsers.proc_buddyinfo.parse('', quiet=True), [])

    def test_proc_buddyinfo(self):
        """
        Test '/proc/buddyinfo'
        """
        self.assertEqual(jc.parsers.proc_buddyinfo.parse(self.f_in['proc_buddyinfo'], quiet=True),
                                                         self.f_json['proc_buddyinfo'])


if __name__ == '__main__':
    unittest.main()
