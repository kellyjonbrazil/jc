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


    def test_toml_existing_iso_key(self):
        """
        Test 'toml' with a key that has the same name as a generated _iso key
        """
        data = 'built = 1979-05-27T07:32:00Z\nbuilt_iso = "my own value"\n[nested]\nwhen = 2020-01-01T00:00:00Z\nwhen_iso = 5\n[[arr]]\nd = 2021-01-01T00:00:00Z\nd_iso = "x"\n'
        expected = {
            'built': 296638320,
            'built_iso': 'my own value',
            'nested': {'when': 1577836800, 'when_iso': 5},
            'arr': [{'d': 1609459200, 'd_iso': 'x'}]
        }
        self.assertEqual(parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
