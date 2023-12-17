import os
import unittest
import json
from typing import Dict
from jc.parsers.pkg_index_deb import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'deb_packages_index': (
                'fixtures/generic/pkg-index-deb.out',
                'fixtures/generic/pkg-index-deb.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_pkg_index_deb_nodata(self):
        """
        Test 'pkg-index-deb' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_pkg_index_deb(self):
        """
        Test 'pkg-index-deb'
        """
        self.assertEqual(
            parse(self.f_in['deb_packages_index'], quiet=True),
            self.f_json['deb_packages_index']
        )


if __name__ == '__main__':
    unittest.main()
