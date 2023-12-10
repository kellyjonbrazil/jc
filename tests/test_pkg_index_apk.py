import os
import unittest
import json
from typing import Dict
from jc.parsers.pkg_index_apk import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class Apkindex(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'normal': (
                'fixtures/generic/pkg-index-apk.out',
                'fixtures/generic/pkg-index-apk.json'),
            'raw': (
                'fixtures/generic/pkg-index-apk.out',
                'fixtures/generic/pkg-index-apk-raw.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_pkg_index_apk_nodata(self):
        """
        Test 'pkg-index-apk' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_pkg_index_apk(self):
        """
        Test 'pkg-index-apk' normal output
        """
        self.assertEqual(
            parse(self.f_in['normal'], quiet=True),
            self.f_json['normal']
        )


    def test_pkg_index_apk_raw(self):
        """
        Test 'pkg-index-apk' raw output
        """
        self.assertEqual(
            parse(self.f_in['raw'], quiet=True, raw=True),
            self.f_json['raw']
        )


if __name__ == "__main__":
    unittest.main()
