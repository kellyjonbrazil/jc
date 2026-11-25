import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_swaps

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_swaps': (
                'fixtures/linux-proc/swaps',
                'fixtures/linux-proc/swaps.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_swaps_nodata(self):
        """
        Test 'proc_swaps' with no data
        """
        self.assertEqual(jc.parsers.proc_swaps.parse('', quiet=True), [])

    def test_proc_swaps(self):
        """
        Test '/proc/swaps'
        """
        self.assertEqual(jc.parsers.proc_swaps.parse(self.f_in['proc_swaps'], quiet=True),
                                                     self.f_json['proc_swaps'])

    def test_proc_swaps_octal_escapes(self):
        """
        Test '/proc/swaps' with octal escapes in the file name
        """
        data = (
            'Filename\t\t\t\tType\t\tSize\t\tUsed\t\tPriority\n'
            '/my\\040swap\\011file\\134x\t\t\t\tfile\t\t1048572\t\t0\t\t-2\n'
            '/dev/dm-1                               partition\t8388604\t\t512\t\t-3\n'
        )
        result = jc.parsers.proc_swaps.parse(data, quiet=True)
        self.assertEqual(result, [
            {'filename': '/my swap\tfile\\x', 'type': 'file', 'size': 1048572, 'used': 0, 'priority': -2},
            {'filename': '/dev/dm-1', 'type': 'partition', 'size': 8388604, 'used': 512, 'priority': -3}
        ])


if __name__ == '__main__':
    unittest.main()
