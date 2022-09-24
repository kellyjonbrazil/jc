import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_modules

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_modules': (
                'fixtures/linux-proc/modules',
                'fixtures/linux-proc/modules.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_modules_nodata(self):
        """
        Test 'proc_modules' with no data
        """
        self.assertEqual(jc.parsers.proc_modules.parse('', quiet=True), [])

    def test_proc_modules(self):
        """
        Test '/proc/modules'
        """
        self.assertEqual(jc.parsers.proc_modules.parse(self.f_in['proc_modules'], quiet=True),
                                                       self.f_json['proc_modules'])


if __name__ == '__main__':
    unittest.main()
