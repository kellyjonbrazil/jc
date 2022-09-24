import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_version

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_version': (
                'fixtures/linux-proc/version',
                'fixtures/linux-proc/version.json'),
            'proc_version2': (
                'fixtures/linux-proc/version2',
                'fixtures/linux-proc/version2.json'),
            'proc_version3': (
                'fixtures/linux-proc/version3',
                'fixtures/linux-proc/version3.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_version_nodata(self):
        """
        Test 'proc_version' with no data
        """
        self.assertEqual(jc.parsers.proc_version.parse('', quiet=True), {})

    def test_proc_version(self):
        """
        Test '/proc/version'
        """
        self.assertEqual(jc.parsers.proc_version.parse(self.f_in['proc_version'], quiet=True),
                                                       self.f_json['proc_version'])

    def test_proc_version2(self):
        """
        Test '/proc/version' #2
        """
        self.assertEqual(jc.parsers.proc_version.parse(self.f_in['proc_version2'], quiet=True),
                                                       self.f_json['proc_version2'])

    def test_proc_version3(self):
        """
        Test '/proc/version' #3
        """
        self.assertEqual(jc.parsers.proc_version.parse(self.f_in['proc_version3'], quiet=True),
                                                       self.f_json['proc_version3'])


if __name__ == '__main__':
    unittest.main()
