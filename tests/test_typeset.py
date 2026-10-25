import unittest
import os
import sys
import json
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc.parsers.typeset


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Execute these steps for standard tests:
# - Save this file as `test_{parser_name}.py` since the helper methods extract parser names from the filename.
# - Organize fixtures in `tests/fixtures` for optimal structure.
# - Format fixtures as follows (using double dashes):
#     - `{parser_name}--{some_test_description}.out` for command output.
#     - `{parser_name}--{some_test_description}.json` for expected JSON after parsing.


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/typeset--long-array-like-value.out'), 'r', encoding='utf-8') as f:
        generic_long_array_like_value = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/typeset--long-array-like-value.json'), 'r', encoding='utf-8') as f:
        generic_long_array_like_value_json = json.loads(f.read())

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

    def test_typeset_long_array_like_value(self):
        """
        Test 'declare -p' output with a long scalar value that looks like array definitions
        """
        self.assertEqual(jc.parsers.typeset.parse(self.generic_long_array_like_value, quiet=True), self.generic_long_array_like_value_json)

    def test_typeset_values_with_equals_and_quotes(self):
        """
        Test 'typeset' scalar values containing '=', quotes, parentheses, and spaces
        """
        data = 'declare -- q="a=b c=\\"d\\" (e) \\$f"\nq=\'a=b c="d" (e) $f\'\ndeclare -- t=$\'x=1\\ty\'\ndeclare -- w="declare -x a b"\ndeclare -x FOO'
        result = jc.parsers.typeset.parse(data, quiet=True)
        self.assertEqual([x['name'] for x in result], ['q', 'q', 't', 'w', 'FOO'])
        self.assertEqual([x['value'] for x in result], ['a=b c=\\"d\\" (e) \\$f', 'a=b c="d" (e) $f', 'x=1\ty', 'declare -x a b', None])
        self.assertEqual([x['type'] for x in result], ['variable'] * 5)

    def test_typeset_array_values_like_array_definitions(self):
        """
        Test 'typeset' arrays with element values that look like array definitions
        """
        data = 'declare -A colors=([red]="#f00" [mix]="r=([1]=g)" )\ntypeset -a arr=( \'k=([x]=y)\' plain )\ntypeset -A opts=( [mode]=\'a=(b)\' [x]=y )'
        result = jc.parsers.typeset.parse(data, quiet=True)
        self.assertEqual([x['name'] for x in result], ['colors', 'arr', 'opts'])
        self.assertEqual([x['type'] for x in result], ['associative', 'array', 'associative'])
        self.assertEqual([x['value'] for x in result], [{'red': '#f00', 'mix': 'r=([1]=g)'}, ['k=([x]=y)', 'plain'], {'mode': 'a=(b)', 'x': 'y'}])


if __name__ == '__main__':
    unittest.main()
