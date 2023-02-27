import os
import unittest
import json
from typing import Dict
from jc.parsers.ssh_conf import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'ssh_config1': (
                'fixtures/generic/ssh_config1',
                'fixtures/generic/ssh_config1.json'),
            'ssh_config2': (
                'fixtures/generic/ssh_config2',
                'fixtures/generic/ssh_config2.json'),
            'ssh_config3': (
                'fixtures/generic/ssh_config3',
                'fixtures/generic/ssh_config3.json'),
            'ssh_config4': (
                'fixtures/generic/ssh_config4',
                'fixtures/generic/ssh_config4.json'),
            'ssh_config5': (
                'fixtures/generic/ssh_config5',
                'fixtures/generic/ssh_config5.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_ssh_nodata(self):
        """
        Test 'ssh' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_ssh_config1(self):
        """
        Test 'ssh' config 1
        """
        self.assertEqual(
            parse(self.f_in['ssh_config1'], quiet=True),
            self.f_json['ssh_config1']
        )

    def test_ssh_config2(self):
        """
        Test 'ssh' config 2
        """
        self.assertEqual(
            parse(self.f_in['ssh_config2'], quiet=True),
            self.f_json['ssh_config2']
        )

    def test_ssh_config3(self):
        """
        Test 'ssh' config 3
        """
        self.assertEqual(
            parse(self.f_in['ssh_config3'], quiet=True),
            self.f_json['ssh_config3']
        )

    def test_ssh_config4(self):
        """
        Test 'ssh' config 4
        """
        self.assertEqual(
            parse(self.f_in['ssh_config4'], quiet=True),
            self.f_json['ssh_config4']
        )

    def test_ssh_config5(self):
        """
        Test 'ssh' config 5
        """
        self.assertEqual(
            parse(self.f_in['ssh_config5'], quiet=True),
            self.f_json['ssh_config5']
        )


if __name__ == '__main__':
    unittest.main()
