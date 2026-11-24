import json
import os
import unittest
from jc.exceptions import ParseError
import jc.parsers.cbt

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt-single.out'), 'r', encoding='utf-8') as f:
        single = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt-multiple-columns.out'), 'r', encoding='utf-8') as f:
        multiple_columns = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt-multiple-rows.out'), 'r', encoding='utf-8') as f:
        multiple_rows = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt-single.json'), 'r', encoding='utf-8') as f:
        single_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt-multiple-columns.json'), 'r', encoding='utf-8') as f:
        multiple_columns_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt-multiple-rows.json'), 'r', encoding='utf-8') as f:
        multiple_rows_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt-multiple-rows-raw.json'), 'r', encoding='utf-8') as f:
        multiple_rows_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt--dashes-in-values.out'), 'r', encoding='utf-8') as f:
        dashes_in_values = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cbt--dashes-in-values.json'), 'r', encoding='utf-8') as f:
        dashes_in_values_json = json.loads(f.read())

    def test_cbt_nodata(self):
        """
        Test 'cbt' with no data
        """
        self.assertEqual(jc.parsers.cbt.parse('', quiet=True), [])

    def test_cbt_single_row(self):
        """
        Test 'cbt' with a single row
        """
        self.assertEqual(jc.parsers.cbt.parse(self.single, quiet=True), self.single_json)

    def test_cbt_multiple_column_families(self):
        """
        Test 'cbt' with multiple columns from multiple column families
        """
        self.assertEqual(jc.parsers.cbt.parse(self.multiple_columns, quiet=True), self.multiple_columns_json)

    def test_cbt_multiple_rows(self):
        """
        Test 'cbt' with multiple rows
        """
        self.assertEqual(jc.parsers.cbt.parse(self.multiple_rows, quiet=True), self.multiple_rows_json)

    def test_cbt_multiple_rows_raw(self):
        """
        Test 'cbt' with multiple rows raw
        """
        self.assertEqual(jc.parsers.cbt.parse(self.multiple_rows, quiet=True, raw=True), self.multiple_rows_raw_json)


    def test_cbt_line_separator(self):
        """
        Test 'cbt' with a line-break character other than LF inside a field
        """
        data = '----------------------------------------\nsandbox\u2028payroll\n  acl:user                                 @ 2024/03/01-09:00:00.000000\n    "owner"\n'
        result = jc.parsers.cbt.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['key'], 'sandbox\u2028payroll')

    def test_cbt_dashes_in_values(self):
        """
        Test 'cbt' with a row key and a cell value that contain 40 dashes
        """
        self.assertEqual(jc.parsers.cbt.parse(self.dashes_in_values, quiet=True), self.dashes_in_values_json)

    def test_cbt_value_quotes_and_spaces(self):
        """
        Test 'cbt' with values that have their own leading and trailing
        spaces and quotes
        """
        sep = '-' * 40
        cell = '  f:%s                                 @ 2024/03/01-09:00:00.000000\n    %s\n'
        data = sep + '\nrow\n' + cell % ('a', '"  padded  "') + cell % ('b', '"\\"quoted\\""') + cell % ('c', '""')
        result = jc.parsers.cbt.parse(data, quiet=True)
        self.assertEqual(result[0]['cells']['f'], {'a': '  padded  ', 'b': '\\"quoted\\"', 'c': ''})


if __name__ == '__main__':
    unittest.main()
