import os
import unittest
import json
from typing import Dict
from jc.parsers.deb_packages_index import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'deb_packages_index': (
                'fixtures/generic/deb-packages-index.out',
                'fixtures/generic/deb-packages-index.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_deb_packages_index_nodata(self):
        """
        Test 'deb_packages_index' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_deb_packages_index(self):
        """
        Test 'deb_packages_index'
        """
        self.assertEqual(
            parse(self.f_in['deb_packages_index'], quiet=True),
            self.f_json['deb_packages_index']
        )


if __name__ == '__main__':
    unittest.main()
