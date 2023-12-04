import os
import unittest
import json
from typing import Dict
from jc.parsers.debconf_show import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'debconf_show': (
                'fixtures/generic/debconf-show.out',
                'fixtures/generic/debconf-show.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_debconf_show_nodata(self):
        """
        Test 'debconf_show' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_debconf_show_centos_7_7(self):
        """
        Test 'debconf_show onlyoffice-documentserver'
        """
        self.assertEqual(
            parse(self.f_in['debconf_show'], quiet=True),
            self.f_json['debconf_show']
        )


if __name__ == '__main__':
    unittest.main()
