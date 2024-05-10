import os
import unittest
import json
from typing import Dict
from jc.parsers.zpool_status import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'zpool_status': (
                'fixtures/generic/zpool-status-v.out',
                'fixtures/generic/zpool-status-v.json'),
            'zpool_status2': (
                'fixtures/generic/zpool-status-v2.out',
                'fixtures/generic/zpool-status-v2.json'),
            'zpool_status3': (
                'fixtures/generic/zpool-status-v3.out',
                'fixtures/generic/zpool-status-v3.json'),
            'zpool_status4': (
                'fixtures/generic/zpool-status-v4.out',
                'fixtures/generic/zpool-status-v4.json'),
            'zpool_status_spares': (
                'fixtures/generic/zpool-status-spares.out',
                'fixtures/generic/zpool-status-spares.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_zpool_status_nodata(self):
        """
        Test 'zpool_status' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_zpool_status_v(self):
        """
        Test 'zpool status -v'
        """
        self.assertEqual(
            parse(self.f_in['zpool_status'], quiet=True),
            self.f_json['zpool_status']
        )

    def test_zpool_status_v_2(self):
        """
        Test 'zpool status -v' #2
        """
        self.assertEqual(
            parse(self.f_in['zpool_status2'], quiet=True),
            self.f_json['zpool_status2']
        )

    def test_zpool_status_v_3(self):
        """
        Test 'zpool status -v' #3
        """
        self.assertEqual(
            parse(self.f_in['zpool_status3'], quiet=True),
            self.f_json['zpool_status3']
        )

    def test_zpool_status_v_with_tabs(self):
        """
        Test 'zpool status -v' with tabs instead of spaces
        """
        self.assertEqual(
            parse(self.f_in['zpool_status4'], quiet=True),
            self.f_json['zpool_status4']
        )

    def test_zpool_status_spares(self):
        """
        Test 'zpool status' with spares section
        """
        self.assertEqual(
            parse(self.f_in['zpool_status_spares'], quiet=True),
            self.f_json['zpool_status_spares']
        )


if __name__ == '__main__':
    unittest.main()
