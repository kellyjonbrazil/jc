import os
import unittest
import json
from typing import Dict
from jc.parsers.findmnt import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'centos_7_7_findmnt': (
                'fixtures/centos-7.7/findmnt.out',
                'fixtures/centos-7.7/findmnt.json'),
            'centos_7_7_findmnt_a': (
                'fixtures/centos-7.7/findmnt-a.out',
                'fixtures/centos-7.7/findmnt-a.json'),
            'centos_7_7_findmnt_l': (
                'fixtures/centos-7.7/findmnt-l.out',
                'fixtures/centos-7.7/findmnt-l.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_findmnt_nodata(self):
        """
        Test 'findmnt' with no data
        """
        self.assertEqual(parse('', quiet=True), [])

    def test_findmnt_centos_7_7(self):
        """
        Test 'findmnt' on Centos 7.7
        """
        self.assertEqual(
            parse(self.f_in['centos_7_7_findmnt'], quiet=True),
            self.f_json['centos_7_7_findmnt']
        )

    def test_findmnt_a_centos_7_7(self):
        """
        Test 'findmnt -a' on Centos 7.7
        """
        self.assertEqual(
            parse(self.f_in['centos_7_7_findmnt_a'], quiet=True),
            self.f_json['centos_7_7_findmnt_a']
        )

    def test_findmnt_l_centos_7_7(self):
        """
        Test 'findmnt -l' on Centos 7.7
        """
        self.assertEqual(
            parse(self.f_in['centos_7_7_findmnt_l'], quiet=True),
            self.f_json['centos_7_7_findmnt_l']
        )


if __name__ == '__main__':
    unittest.main()
