import os
import unittest
import json
from typing import Dict
import jc.parsers.udevadm

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'udevadm': (
                'fixtures/generic/udevadm.out',
                'fixtures/generic/udevadm.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_udevadm_nodata(self):
        """
        Test 'udevadm' with no data
        """
        self.assertEqual(jc.parsers.udevadm.parse('', quiet=True), {})

    def test_udevadm(self):
        """
        Test 'udevadm'
        """
        self.assertEqual(jc.parsers.udevadm.parse(self.f_in['udevadm'], quiet=True),
                                                  self.f_json['udevadm'])


if __name__ == '__main__':
    unittest.main()
