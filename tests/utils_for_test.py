"""jc - JSON test utils"""
import json
import os
import sys
from pathlib import Path
import jc

VERBOSE = False
if '-v' in sys.argv or '--verbose' in sys.argv:
    VERBOSE = True

def _test_print(data: str) -> None:
    if VERBOSE:
        print(data)

def _open_file(file_path, ext):
    return open(Path(file_path).with_suffix(ext), 'r', encoding='utf-8')


def _get_base_dir(file_path):
    return os.path.dirname(os.path.abspath(file_path))


def _get_parser_name_from_path(parser_path):
    return Path(parser_path).stem[len('test_'):]


def _get_fixtures(base_dir, parser_name):
    fixtures = {x.stem: str(x.with_suffix('')) for x in
                (list(Path(base_dir).glob(f"**/{parser_name}--*.*")))}
    return fixtures


def run_no_data(self, test_parser_path, expected):
    """Call this function to run a test for no input data for a parser"""
    parser_name = _get_parser_name_from_path(test_parser_path)

    with self.subTest(f"'no data test' for parser '{parser_name}': "):
        self.assertEqual(jc.parse(parser_name, '', quiet=True), expected)


def run_all_fixtures(self, test_parser_path):
    """Call this function to run tests for all fixtures for a parser"""
    parser_name = _get_parser_name_from_path(test_parser_path)
    base_dir = _get_base_dir(test_parser_path)
    fixtures = _get_fixtures(base_dir, parser_name).items()

    if not fixtures:
        raise ValueError(f"No fixtures found for '{parser_name}' tests!")

    _test_print(f"\n  Run all fixtures for parser '{parser_name}':")

    for file, file_path in fixtures:
        _test_print(f"  - test '{parser_name}' parser with fixture: '{file}'")

        with self.subTest(f"fixture: '{file}'"):
            with _open_file(file_path, '.out') as in_file, \
                    _open_file(file_path, '.json') as json_file:
                f_in = in_file.read()
                f_json = json.loads(json_file.read())

                self.assertEqual(
                    jc.parse(parser_name, f_in, quiet=True),
                    f_json,
                    f"Should be equal for test files: '{file_path}.*'"
                )
