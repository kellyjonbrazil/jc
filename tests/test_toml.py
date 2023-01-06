import os
import unittest
import json
from typing import Dict
from jc.parsers.toml import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'toml1': (
                'fixtures/generic/toml-example.toml',
                'fixtures/generic/toml-example.json'),
            'toml2': (
                'fixtures/generic/toml-example2.toml',
                'fixtures/generic/toml-example2.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_toml_nodata(self):
        """
        Test 'toml' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_toml_example1(self):
        """
        Test 'toml' with first example file
        """
        self.assertEqual(
            parse(self.f_in['toml1'], quiet=True),
            self.f_json['toml1']
        )

    def test_toml_example2(self):
        """
        Test 'toml' with second example file
        """
        self.assertEqual(
            parse(self.f_in['toml2'], quiet=True),
            self.f_json['toml2']
        )


if __name__ == '__main__':
    unittest.main()
