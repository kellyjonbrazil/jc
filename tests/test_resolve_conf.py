import os
import unittest
import json
from typing import Dict
from jc.parsers.resolve_conf import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'resolve_conf_1': (
                'fixtures/generic/resolve.conf-1',
                'fixtures/generic/resolve.conf-1.json'),
            'resolve_conf_2': (
                'fixtures/generic/resolve.conf-2',
                'fixtures/generic/resolve.conf-2.json'),
            'resolve_conf_3': (
                'fixtures/generic/resolve.conf-3',
                'fixtures/generic/resolve.conf-3.json'),
            'resolve_conf_4': (
                'fixtures/generic/resolve.conf-4',
                'fixtures/generic/resolve.conf-4.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_resolve_conf_nodata(self):
        """
        Test 'resolve_conf' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_resolve_conf_1(self):
        """
        Test 'resolve_conf' file 1
        """
        self.assertEqual(
            parse(self.f_in['resolve_conf_1'], quiet=True),
            self.f_json['resolve_conf_1']
        )

    def test_resolve_conf_2(self):
        """
        Test 'resolve_conf' file 2
        """
        self.assertEqual(
            parse(self.f_in['resolve_conf_2'], quiet=True),
            self.f_json['resolve_conf_2']
        )

    def test_resolve_conf_3(self):
        """
        Test 'resolve_conf' file 3
        """
        self.assertEqual(
            parse(self.f_in['resolve_conf_3'], quiet=True),
            self.f_json['resolve_conf_3']
        )

    def test_resolve_conf_4(self):
        """
        Test 'resolve_conf' file 4
        """
        self.assertEqual(
            parse(self.f_in['resolve_conf_4'], quiet=True),
            self.f_json['resolve_conf_4']
        )


if __name__ == '__main__':
    unittest.main()
