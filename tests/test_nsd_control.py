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
                'fixtures/generic/nsd_control-zonestatus.json'),
            'print_cookie_secrets': (
                'fixtures/generic/nsd_control-cookie_secrets.out',
                'fixtures/generic/nsd_control-cookie_secrets.json'),
            'print_tsig': (
                'fixtures/generic/nsd_control-tsig.out',
                'fixtures/generic/nsd_control-tsig.json'),
            'stats': (
                'fixtures/generic/nsd_control-stats.out',
                'fixtures/generic/nsd_control-stats.json')
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


    def test_nsd_control_status(self):
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

    def test_nsd_control_cookie_secrets(self):
        """
        Test 'nsd-control print_cookie_secrets'
        """
        self.assertEqual(
            parse(self.f_in['print_cookie_secrets'], quiet=True),
            self.f_json['print_cookie_secrets']
        )

    def test_nsd_control_tsig(self):
        """
        Test 'nsd-control print_tsig'
        """
        self.assertEqual(
            parse(self.f_in['print_tsig'], quiet=True),
            self.f_json['print_tsig']
        )

    def test_nsd_control_stats(self):
        """
        Test 'nsd-control stats'
        """
        self.assertEqual(
            parse(self.f_in['stats'], quiet=True),
            self.f_json['stats']
        )

if __name__ == '__main__':
    unittest.main()
