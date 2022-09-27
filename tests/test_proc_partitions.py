import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_partitions

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_partitions': (
                'fixtures/linux-proc/partitions',
                'fixtures/linux-proc/partitions.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_partitions_nodata(self):
        """
        Test 'proc_partitions' with no data
        """
        self.assertEqual(jc.parsers.proc_partitions.parse('', quiet=True), [])

    def test_proc_partitions(self):
        """
        Test '/proc/partitions'
        """
        self.assertEqual(jc.parsers.proc_partitions.parse(self.f_in['proc_partitions'], quiet=True),
                                                          self.f_json['proc_partitions'])


if __name__ == '__main__':
    unittest.main()
