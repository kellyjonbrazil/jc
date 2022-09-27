import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_cpuinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_cpuinfo': (
                'fixtures/linux-proc/cpuinfo',
                'fixtures/linux-proc/cpuinfo.json'),
            'proc_cpuinfo2': (
                'fixtures/linux-proc/cpuinfo2',
                'fixtures/linux-proc/cpuinfo2.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_cpuinfo_nodata(self):
        """
        Test 'proc_cpuinfo' with no data
        """
        self.assertEqual(jc.parsers.proc_cpuinfo.parse('', quiet=True), [])

    def test_proc_cpuinfo(self):
        """
        Test '/proc/buddyinfo'
        """
        self.assertEqual(jc.parsers.proc_cpuinfo.parse(self.f_in['proc_cpuinfo'], quiet=True),
                                                       self.f_json['proc_cpuinfo'])

    def test_proc_cpuinfo2(self):
        """
        Test '/proc/buddyinfo2'
        """
        self.assertEqual(jc.parsers.proc_cpuinfo.parse(self.f_in['proc_cpuinfo2'], quiet=True),
                                                       self.f_json['proc_cpuinfo2'])


if __name__ == '__main__':
    unittest.main()
