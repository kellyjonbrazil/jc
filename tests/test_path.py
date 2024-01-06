import os
import json
import unittest
from typing import Dict
from jc.parsers.path import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

FIXTURES_DIR = 'fixtures/generic/'


def open_file(name, ext):
    return open(get_path(name, ext), 'r', encoding='utf-8')


def get_path(name, ext):
    return os.path.join(THIS_DIR, name + '.' + ext)


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    fixtures = {
        'path--one': 'fixtures/generic/path--one',
        'path--windows': 'fixtures/generic/path--windows',
        'path--with-spaces': 'fixtures/generic/path--with-spaces',
    }

    @classmethod
    def setUpClass(cls):

        for file, filepath in cls.fixtures.items():
            with open_file(filepath, 'out') as in_file, \
                    open_file(filepath, 'json') as json_file:
                cls.f_in[file] = in_file.read()
                cls.f_json[file] = json.loads(json_file.read())

    def test_path_nodata(self):
        """
        Test 'path' with no data
        """
        self.assertEqual(parse('', quiet=True), {})

    def test_path(self):
        """
        Test 'path' with various logs
        """
        for file in self.fixtures:
            self.assertEqual(
                parse(self.f_in[file], quiet=True),
                self.f_json[file],
                "Should be equal for test files: {0}.*".format(file)
            )


if __name__ == '__main__':
    unittest.main()
