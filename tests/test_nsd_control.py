import os
import unittest
import json
from typing import Dict
from jc.parsers.nsd_control import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'default': (
                'fixtures/generic/nsd_control.out',
                'fixtures/generic/nsd_control.json'),
            'status': (
                'fixtures/generic/nsd_control-status.out',
                'fixtures/generic/nsd_control-status.json'),
            'zonestatus': (
                'fixtures/generic/nsd_control-zonestatus.out',
                'fixtures/generic/nsd_control-zonestatus.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_nsd_control_default(self):
        """
        Test 'nsd-control <command>' with default output
        """
        self.assertEqual(
            parse(self.f_in['default'], quiet=True),
            self.f_json['default']
        )


    def test_host_google(self):
        """
        Test 'nsd-control status'
        """
        self.assertEqual(
            parse(self.f_in['status'], quiet=True),
            self.f_json['status']
        )

    def test_nsd_control_zonestatus(self):
        """
        Test 'nsd-control zonestatus'
        """
        self.assertEqual(
            parse(self.f_in['zonestatus'], quiet=True),
            self.f_json['zonestatus']
        )

if __name__ == '__main__':
    unittest.main()
