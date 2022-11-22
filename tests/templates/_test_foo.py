import os
import unittest
import json
from typing import Dict
from jc.parsers.foo import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'centos_7_7_foo': (
                'fixtures/centos-7.7/foo.out',
                'fixtures/centos-7.7/foo.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_foo_nodata(self):
        """
        Test 'foo' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_foo_centos_7_7(self):
        """
        Test 'foo' on Centos 7.7
        """
        self.assertEqual(
            parse(self.f_in['centos_7_7_foo'], quiet=True),
            self.f_json['centos_7_7_foo']
        )


if __name__ == '__main__':
    unittest.main()
