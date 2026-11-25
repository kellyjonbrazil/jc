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


    def test_proc_softirqs_counter_name_that_looks_like_a_number(self):
        """
        Test '/proc/softirqs' with a counter name that looks like a number
        """
        data = '                    CPU0       CPU1\n          007:          1          2\n'
        result = jc.parsers.proc_softirqs.parse(data, quiet=True)
        self.assertEqual(result, [{'counter': '007', 'CPU0': 1, 'CPU1': 2}])


if __name__ == '__main__':
    unittest.main()
