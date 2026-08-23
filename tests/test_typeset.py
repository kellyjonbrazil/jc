import unittest
import os
import json
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()

import jc

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_fixture(name):
    base = os.path.join(THIS_DIR, 'fixtures', 'generic', name)
    with open(base + '.out', encoding='utf-8') as f:
        raw = f.read()
    with open(base + '.json', encoding='utf-8') as f:
        expected = json.load(f)
    return raw, expected

# Execute these steps for standard tests:
# - Save this file as `test_{parser_name}.py` since the helper methods extract parser names from the filename.
# - Organize fixtures in `tests/fixtures` for optimal structure.
# - Format fixtures as follows (using double dashes):
#     - `{parser_name}--{some_test_description}.out` for command output.
#     - `{parser_name}--{some_test_description}.json` for expected JSON after parsing.

class MyTests(unittest.TestCase):

    def test_typeset_nodata(self):
        """
        Test 'typeset' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_typeset_all_fixtures(self):
        """
        Test 'typeset' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    # def test_typeset_ksh(self):
    #     """
    #     Test 'typeset -p' output from ksh
    #     """
    #     raw, expected = _load_fixture('typeset--ksh')
    #     self.assertEqual(jc.parse('typeset', raw, quiet=True), expected)

    # def test_typeset_zsh(self):
    #     """
    #     Test 'typeset -p' output from zsh
    #     """
    #     raw, expected = _load_fixture('typeset--zsh')
    #     self.assertEqual(jc.parse('typeset', raw, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
