import os
import json
import unittest
from typing import Dict
from jc.parsers.foo_s import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat foo.out | jc --foo-s | jello -c > foo-streaming.json


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'centos_7_7_foo': (
                'fixtures/centos-7.7/foo.out',
                'fixtures/centos-7.7/foo-streaming.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_foo_s_nodata(self):
        """
        Test 'foo' with no data
        """
        self.assertEqual(list(parse([], quiet=True)), [])


    def test_foo_s_centos_7_7(self):
        """
        Test 'foo' on Centos 7.7
        """
        self.assertEqual(
            list(parse(self.f_in['centos_7_7_foo'].splitlines(), quiet=True)),
            self.f_json['centos_7_7_foo']
        )


if __name__ == '__main__':
    unittest.main()
