import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_softirqs

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_softirqs': (
                'fixtures/linux-proc/softirqs',
                'fixtures/linux-proc/softirqs.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_softirqs_nodata(self):
        """
        Test 'proc_softirqs' with no data
        """
        self.assertEqual(jc.parsers.proc_softirqs.parse('', quiet=True), [])

    def test_proc_softirqs(self):
        """
        Test '/proc/softirqs'
        """
        self.assertEqual(jc.parsers.proc_softirqs.parse(self.f_in['proc_softirqs'], quiet=True),
                                                        self.f_json['proc_softirqs'])


if __name__ == '__main__':
    unittest.main()
