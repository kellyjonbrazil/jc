import os
import unittest
import json
from typing import Dict
from jc.parsers.zpool_iostat import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'zpool_iostat': (
                'fixtures/generic/zpool-iostat.out',
                'fixtures/generic/zpool-iostat.json'),
            'zpool_iostat_v': (
                'fixtures/generic/zpool-iostat-v.out',
                'fixtures/generic/zpool-iostat-v.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_zpool_iostat_nodata(self):
        """
        Test 'zpool iostat' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_zpool_iostat(self):
        """
        Test 'zpool iostat'
        """
        self.assertEqual(
            parse(self.f_in['zpool_iostat'], quiet=True),
            self.f_json['zpool_iostat']
        )

    def test_zpool_iostat_v(self):
        """
        Test 'zpool iostat -v'
        """
        self.assertEqual(
            parse(self.f_in['zpool_iostat_v'], quiet=True),
            self.f_json['zpool_iostat_v']
        )


if __name__ == '__main__':
    unittest.main()
