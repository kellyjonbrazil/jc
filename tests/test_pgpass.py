import os
import unittest
import json
from typing import Dict
from jc.parsers.pgpass import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'pgpass': (
                'fixtures/generic/pgpass.txt',
                'fixtures/generic/pgpass.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_pgpass_nodata(self):
        """
        Test 'pgpass' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_pgpass(self):
        """
        Test postgreSQL password file
        """
        self.assertEqual(
            parse(self.f_in['pgpass'], quiet=True),
            self.f_json['pgpass']
        )


if __name__ == '__main__':
    unittest.main()
