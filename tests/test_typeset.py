import unittest
import os
import sys
import json
import shlex
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
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/typeset--numeric-first-key.out'), 'r', encoding='utf-8') as f:
        generic_numeric_first_key = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/typeset--numeric-first-key.json'), 'r', encoding='utf-8') as f:
        generic_numeric_first_key_json = json.loads(f.read())

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


    def test_typeset_ansi_c_quote_in_array_values(self):
        """
        Test 'declare -p' arrays with $'...' values that contain quotes and
        text in the form of other elements
        """
        data = "declare -A roles=([dave]=$'guest\\n\\' [carol]=\\'admin' [alice]=\"admin\" )\ndeclare -a notes=([0]=\"a\" [1]=$'b\\n\\' [9]=\\'c' [2]=\"z\")"
        result = jc.parsers.typeset.parse(data, quiet=True)
        self.assertEqual(result[0]['value'], {'dave': "guest\n' [carol]='admin", 'alice': 'admin'})
        self.assertEqual(result[1]['value'], ['a', "b\n' [9]='c", 'z'])

    def test_typeset_ansi_c_in_double_quoted_array_value(self):
        """
        Test 'declare -p' array where a double-quoted value contains $'
        """
        data = 'declare -A roles=([dave]="\\$\'\\" [carol]=\\"admin\\" [x]=\\"\'" [alice]="admin" )'
        result = jc.parsers.typeset.parse(data, quiet=True)
        self.assertEqual(sorted(result[0]['value']), ['alice', 'dave'])
        self.assertEqual(result[0]['value']['alice'], 'admin')

    def test_typeset_ansi_c_array_raw(self):
        """
        Test 'declare -p' array with $'...' values containing quotes in raw mode
        """
        data = "declare -a notes=([0]=\"a\" [1]=$'it\\'s\\n')"
        result = jc.parsers.typeset.parse(data, raw=True, quiet=True)
        self.assertEqual(result[0]['value'], ['a', "it\\'s\\n"])

    def test_typeset_ansi_c_bare_array(self):
        """
        Test zsh/ksh bare-value array with $'...' values containing quotes
        """
        data = "typeset -a arr=( a 'b c' $'d\\n\\' e=\\'f' )"
        result = jc.parsers.typeset.parse(data, quiet=True)
        self.assertEqual(result[0]['value'], ['a', 'b c', "d\n' e='f"])

    def test_typeset_numeric_first_key_associative(self):
        """
        Test 'declare -p' associative arrays declared with -A whose first key is a number
        """
        self.assertEqual(jc.parsers.typeset.parse(self.generic_numeric_first_key, quiet=True), self.generic_numeric_first_key_json)

    def test_typeset_shell_split_like_shlex(self):
        """
        Test 'typeset' array word splitting against shlex.split()
        """
        samples = [
            '', '  ', 'a b', '[0]="a b" [1]=c', "[0]='a \\ b' [1]=\"x\\\"y\"",
            'a"b c"d', "a'b c'd", '"\\$x" "\\\\" "\\n"', 'a\\ b\\\\ c', "'' \"\"",
            '\ta\r\nb\xa0c', '[k]="v" [a=b]="c"', '"a\\"', '"a', "'a", 'a\\', '"a\\',
            '[0]="' + 'x' * 1000 + '"'
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                try:
                    expected = shlex.split(sample)
                except ValueError as e:
                    expected = str(e)
                try:
                    result = jc.parsers.typeset._shell_split(sample)
                except ValueError as e:
                    result = str(e)
                self.assertEqual(result, expected)

    def test_typeset_associative_keys_with_equals(self):
        """
        Test 'declare -p' associative arrays with keys that contain '=' or ']='
        """
        data = 'declare -A x=(["s]=p"]="3" ["q\\"x"]="2" [a=b]="c" [k]="v=w" [$\'t\\tu\']="4" ["s]p"]="1" )\n'
        result = jc.parsers.typeset.parse(data, quiet=True)
        self.assertEqual(result[0]['value'], {'s]=p': '3', 'q"x': '2', 'a=b': 'c', 'k': 'v=w', 't\tu': '4', 's]p': '1'})
        self.assertEqual(result[0]['type'], 'associative')


if __name__ == '__main__':
    unittest.main()
