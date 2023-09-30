import os
import unittest
import json
from typing import Dict
from jc.parsers.host import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'google': (
                'fixtures/generic/host-google.out',
                'fixtures/generic/host-google.json'),
            'sunet': (
                'fixtures/generic/host-sunet.out',
                'fixtures/generic/host-sunet.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())

    # host cannot run without input (will only display help)
    def test_host_nodata(self):
       """
       Test 'host' with no data
       """
       self.assertEqual(parse('', quiet=True), [])


    def test_host_google(self):
        """
        Test 'host google'
        """
        self.assertEqual(
            parse(self.f_in['google'], quiet=True),
            self.f_json['google']
        )

    def test_host_sunet(self):
        """
        Test 'host sunet'
        """
        self.assertEqual(
            parse(self.f_in['sunet'], quiet=True),
            self.f_json['sunet']
        )

if __name__ == '__main__':
    unittest.main()
