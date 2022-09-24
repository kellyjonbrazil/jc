import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_filesystems

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_filesystems': (
                'fixtures/linux-proc/filesystems',
                'fixtures/linux-proc/filesystems.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_filesystems_nodata(self):
        """
        Test 'proc_filesystems' with no data
        """
        self.assertEqual(jc.parsers.proc_filesystems.parse('', quiet=True), [])

    def test_proc_filesystems(self):
        """
        Test '/proc/buddyinfo'
        """
        self.assertEqual(jc.parsers.proc_filesystems.parse(self.f_in['proc_filesystems'], quiet=True),
                                                           self.f_json['proc_filesystems'])


if __name__ == '__main__':
    unittest.main()
