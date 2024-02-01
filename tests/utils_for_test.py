"""jc - JSON test utils"""
import os
import jc
import json
import inspect
from pathlib import Path


def open_file(file_path, ext):
    return open(Path(file_path).with_suffix(ext), 'r', encoding='utf-8')


def get_base_dir(file_path):
    THIS_DIR = os.path.dirname(os.path.abspath(file_path))
    return THIS_DIR


def get_parser_name():
    # Get the calling file name from the stack
    stack = inspect.stack()
    calling_frame = stack[1]
    calling_file_path = calling_frame[1]

    return get_parser_name_from_path(calling_file_path)


def get_parser_name_from_path(parser_path):
    return Path(parser_path).stem[len('test_'):]


def get_fixtures(base_dir, parser_name):
    fixtures = {x.stem: str(x.with_suffix('')) for x in
                (list(Path(base_dir).glob('**/{0}--*.*'.format(parser_name))))}
    return fixtures


def run_no_data(self, test_parser_path, expected):
    parser_name = get_parser_name_from_path(test_parser_path)

    # expected = jc.get_parser(parser_name).info.default_no_data

    with self.subTest("no data test for: " + parser_name):
        self.assertEqual(jc.parse(parser_name, '', quiet=True), expected)

def run_all_fixtures(self, test_parser_path):
    parser_name = get_parser_name_from_path(test_parser_path)
    base_dir = get_base_dir(test_parser_path)

    print()
    print("run all fixtures for " + parser_name + ":")
    for file, file_path in get_fixtures(base_dir, parser_name).items():

        print(f'- test "{parser_name}" parser with fixture: "{file}"')
        with self.subTest("fixture: " + file):

            with open_file(file_path, '.out') as in_file, \
                    open_file(file_path, '.json') as json_file:
                f_in = in_file.read()
                f_json = json.loads(json_file.read())

                self.assertEqual(
                    jc.parse(parser_name, f_in, quiet=True),
                    f_json,
                    "Should be equal for test files: {0}.*".format(file)
                )
    return "All tests passed from: run_all_fixtures"