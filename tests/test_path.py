import os
import json
import unittest
from pathlib import Path
from typing import Dict
from jc.parsers.path import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def open_file(name, ext):
    return open(Path(name).with_suffix(ext), 'r', encoding='utf-8')


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    parser_name = Path(__file__).stem[len('test_'):]

    fixtures = {x.stem: str(x.with_suffix('')) for x in
                (list(Path(THIS_DIR).glob('**/{0}--*.*'.format(parser_name))))}


    @classmethod
    def setUpClass(cls):

        for file, filepath in cls.fixtures.items():
            with open_file(filepath, '.out') as in_file, \
                    open_file(filepath, '.json') as json_file:
                cls.f_in[file] = in_file.read()
                cls.f_json[file] = json.loads(json_file.read())

    def test_path_nodata(self):
        """
        Test 'path' with no data
        """
        self.assertEqual(parse('', quiet=True), {})

    def test_all_fixtures(self):
        """
        Test 'path' with various logs
        """
        print()
        for file in self.fixtures:
            print(f'test "{self.parser_name}" parser with fixture: "{file}"')
            with self.subTest("fixture: " + file):
                self.assertEqual(
                    parse(self.f_in[file], quiet=True),
                    self.f_json[file],
                    "Should be equal for test files: {0}.*".format(file)
                )


if __name__ == '__main__':
    unittest.main()
