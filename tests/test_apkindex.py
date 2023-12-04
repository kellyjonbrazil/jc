import os
import unittest
import json
from typing import Dict
from jc.parsers.apkindex import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class Apkindex(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'normal': (
                'fixtures/generic/apkindex',
                'fixtures/generic/apkindex.json'),
            'raw': (
                'fixtures/generic/apkindex',
                'fixtures/generic/apkindex.raw.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_apkindex_nodata(self):
        """
        Test 'apkindex' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_apkindex(self):
        """
        Test 'apkindex' normal output
        """
        self.assertEqual(
            parse(self.f_in['normal'], quiet=True),
            self.f_json['normal']
        )


    def test_apkindex_raw(self):
        """
        Test 'apkindex' raw output
        """
        self.assertEqual(
            parse(self.f_in['raw'], quiet=True, raw=True),
            self.f_json['raw']
        )


if __name__ == "__main__":
    unittest.main()
