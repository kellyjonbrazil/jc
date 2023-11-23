import os
import unittest
import json
from typing import Dict
from jc.parsers.tune2fs import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'tune2fs': (
                'fixtures/generic/tune2fs-l.out',
                'fixtures/generic/tune2fs-l.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_tune2fs_nodata(self):
        """
        Test 'tune2fs' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_tune2fs_l(self):
        """
        Test 'tune2fs -l'
        """
        self.assertEqual(
            parse(self.f_in['tune2fs'], quiet=True),
            self.f_json['tune2fs']
        )


if __name__ == '__main__':
    unittest.main()
