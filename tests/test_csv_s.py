import csv
import os
import json
import unittest
import jc.parsers.csv
import jc.parsers.csv_s
import jc.parsers.csv_ih_s
import jc.parsers.tsv_s
import jc.parsers.tsv_ih_s
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# To create streaming output use:
# $ cat file.csv | jc --csv-s | jello -c > csv-file-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-biostats.csv'), 'r', encoding='utf-8') as f:
        generic_csv_biostats = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-cities.csv'), 'r', encoding='utf-8') as f:
        generic_csv_cities = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-deniro.csv'), 'r', encoding='utf-8') as f:
        generic_csv_deniro = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-example.csv'), 'r', encoding='utf-8') as f:
        generic_csv_example = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna.tsv'), 'r', encoding='utf-8') as f:
        generic_csv_flyrna = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna2.tsv'), 'r', encoding='utf-8') as f:
        generic_csv_flyrna2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-pipe.csv'), 'r', encoding='utf-8') as f:
        generic_csv_homes_pipe = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes.csv'), 'r', encoding='utf-8') as f:
        generic_csv_homes = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-10k-sales-records.csv'), 'r', encoding='utf-8') as f:
        generic_csv_10k_sales_records = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-doublequoted.csv'), 'r', encoding='utf-8') as f:
        generic_csv_doublequoted = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-apostrophes.csv'), 'r', encoding='utf-8') as f:
        generic_csv_apostrophes = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-apostrophes-pipe.csv'), 'r', encoding='utf-8') as f:
        generic_csv_apostrophes_pipe = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-utf-8-bom.csv'), 'r', encoding='utf-8') as f:
        generic_csv_utf8_bom = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv_ih-homes.csv'), 'r', encoding='utf-8') as f:
        generic_csv_ih_homes_csv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv_ih-jagged.csv'), 'r', encoding='utf-8') as f:
        generic_csv_ih_jagged_csv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv_ih-dpkg-query.tsv'), 'r', encoding='utf-8') as f:
        generic_tsv_ih_dpkg_query_tsv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv-dpkg-query.tsv'), 'r', encoding='utf-8') as f:
        generic_tsv_dpkg_query_tsv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv_ih-simple-double-quote.tsv'), 'r', encoding='utf-8') as f:
        generic_tsv_ih_simple_double_quote_tsv = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-biostats-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_biostats_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-cities-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_cities_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-deniro-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_deniro_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-example-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_example_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_flyrna_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna2-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_flyrna2_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-pipe-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_homes_pipe_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_homes_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-10k-sales-records-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_10k_sales_records_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-doublequoted-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_doublequoted_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-apostrophes-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_apostrophes_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-apostrophes-pipe-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_apostrophes_pipe_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-utf-8-bom-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_utf8_bom_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv_ih-homes-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_ih_homes_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv_ih-jagged-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_ih_jagged_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv_ih-dpkg-query-streaming.json'), 'r', encoding='utf-8') as f:
        generic_tsv_ih_dpkg_query_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv-dpkg-query-streaming.json'), 'r', encoding='utf-8') as f:
        generic_tsv_dpkg_query_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv_ih-simple-double-quote-streaming.json'), 'r', encoding='utf-8') as f:
        generic_tsv_ih_simple_double_quote_streaming_json = json.loads(f.read())


    def test_csv_s_nodata(self):
        """
        Test CSV parser with no data
        """
        self.assertEqual(list(jc.parsers.csv_s.parse([], quiet=True)), [])

    def test_csv_unparsable(self):
        """
        Test CSV streaming parser with '\r' newlines. This will raise ParseError due to a Python bug
        that does not correctly iterate on that line ending with sys.stdin. This is not a great test.
        https://bugs.python.org/issue45617
        """
        data = r'unparsable\rdata'    # raw mode simulates unrecognized line separator - not great
        g = jc.parsers.csv_s.parse(data.splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_csv_s_biostats(self):
        """
        Test 'biostats.csv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_biostats.splitlines(), quiet=True)), self.generic_csv_biostats_streaming_json)

    def test_csv_s_cities(self):
        """
        Test 'cities.csv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_cities.splitlines(), quiet=True)), self.generic_csv_cities_streaming_json)

    def test_csv_s_deniro(self):
        """
        Test 'deniro.csv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_deniro.splitlines(), quiet=True)), self.generic_csv_deniro_streaming_json)

    def test_csv_s_example(self):
        """
        Test 'example.csv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_example.splitlines(), quiet=True)), self.generic_csv_example_streaming_json)

    def test_csv_s_flyrna(self):
        """
        Test 'flyrna.tsv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_flyrna.splitlines(), quiet=True)), self.generic_csv_flyrna_streaming_json)

    def test_csv_s_flyrna2(self):
        """
        Test 'flyrna2.tsv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_flyrna2.splitlines(), quiet=True)), self.generic_csv_flyrna2_streaming_json)

    def test_csv_s_homes_pipe(self):
        """
        Test 'homes-pipe.csv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_homes_pipe.splitlines(), quiet=True)), self.generic_csv_homes_pipe_streaming_json)

    def test_csv_s_homes(self):
        """
        Test 'homes.csv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_homes.splitlines(), quiet=True)), self.generic_csv_homes_streaming_json)

    def test_csv_s_10k_records(self):
        """
        Test '10k-sales-records.csv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_10k_sales_records.splitlines(), quiet=True)), self.generic_csv_10k_sales_records_streaming_json)

    def test_csv_s_doublequoted(self):
        """
        Test 'doublequoted.csv' file
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_doublequoted.splitlines(), quiet=True)), self.generic_csv_doublequoted_streaming_json)

    def test_csv_s_apostrophes(self):
        """
        Test 'csv-apostrophes.csv' file to ensure apostrophes in field values do not change the quote character
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_apostrophes.splitlines(), quiet=True)), self.generic_csv_apostrophes_streaming_json)

    def test_csv_s_apostrophes_pipe(self):
        """
        Test 'csv-apostrophes-pipe.csv' file to ensure apostrophes and delimiters in field values do not change the dialect
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_apostrophes_pipe.splitlines(), quiet=True)), self.generic_csv_apostrophes_pipe_streaming_json)

    def test_csv_s_doublequoted_matches_csv(self):
        """
        Test 'doublequoted.csv' file gives the same records as the csv parser
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_doublequoted.splitlines(), quiet=True)), jc.parsers.csv.parse(self.generic_csv_doublequoted, quiet=True))

    def test_csv_s_utf8_bom(self):
        """
        Test 'csv-utf-8-bom.csv' file to ensure the first column is correct if UTF-8 BOM bytes are present
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_utf8_bom.splitlines(), quiet=True)), self.generic_csv_utf8_bom_streaming_json)

    def test_csv_s_ih_homes(self):
        """
        Test 'csv_ih-homes.csv' file in implicit header mode.
        """
        self.assertEqual(list(jc.parsers.csv_ih_s.parse(self.generic_csv_ih_homes_csv.splitlines(), quiet=True)), self.generic_csv_ih_homes_streaming_json)

    def test_csv_s_ih_jagged(self):
        """
        Test 'csv_ih-jagged.csv' file in implicit header mode.
        """
        self.assertEqual(list(jc.parsers.csv_ih_s.parse(self.generic_csv_ih_jagged_csv.splitlines(), quiet=True)), self.generic_csv_ih_jagged_streaming_json)

    def test_tsv_s_ih_dpkg_query(self):
        """
        Test 'tsv_ih-dpkg-query.tsv' file in implicit header mode.
        """
        self.assertEqual(list(jc.parsers.tsv_ih_s.parse(self.generic_tsv_ih_dpkg_query_tsv.splitlines(), quiet=True)), self.generic_tsv_ih_dpkg_query_streaming_json)

    def test_tsv_s_dpkg_query(self):
        """
        Test 'tsv-dpkg-query.tsv' file
        """
        self.assertEqual(list(jc.parsers.tsv_s.parse(self.generic_tsv_dpkg_query_tsv.splitlines(), quiet=True)), self.generic_tsv_dpkg_query_streaming_json)

    def test_tsv_s_ih_simple_double_quote(self):
        """
        Test 'tsv_ih-simple-double-quote.tsv' file in implicit header mode.
        """
        self.assertEqual(list(jc.parsers.tsv_ih_s.parse(self.generic_tsv_ih_simple_double_quote_tsv.splitlines(), quiet=True)), self.generic_tsv_ih_simple_double_quote_streaming_json)


    def test_csv_s_blank_only(self):
        """
        Test csv_s with blank-only input
        """
        self.assertEqual(list(jc.parsers.csv_s.parse([''], quiet=True)), [])

    def test_csv_ih_s_blank_only(self):
        """
        Test csv_ih_s with blank-only input
        """
        self.assertEqual(list(jc.parsers.csv_ih_s.parse([''], quiet=True)), [])

    def test_tsv_s_blank_only(self):
        """
        Test tsv_s with blank-only input
        """
        self.assertEqual(list(jc.parsers.tsv_s.parse([''], quiet=True)), [])

    def test_tsv_ih_s_blank_only(self):
        """
        Test tsv_ih_s with blank-only input
        """
        self.assertEqual(list(jc.parsers.tsv_ih_s.parse([''], quiet=True)), [])

    def test_tsv_csv_ih_wrappers_ignore_exceptions(self):
        """
        Test 'tsv_s', 'tsv_ih_s' and 'csv_ih_s' with ignore_exceptions=True:
        every row has the _jc_meta success object
        """
        cases = [
            (jc.parsers.tsv_s, self.generic_tsv_dpkg_query_tsv, self.generic_tsv_dpkg_query_streaming_json),
            (jc.parsers.tsv_ih_s, self.generic_tsv_ih_dpkg_query_tsv, self.generic_tsv_ih_dpkg_query_streaming_json),
            (jc.parsers.csv_ih_s, self.generic_csv_ih_homes_csv, self.generic_csv_ih_homes_streaming_json),
        ]
        for parser, data, expected in cases:
            expected = [dict(row, _jc_meta={'success': True}) for row in expected]
            self.assertEqual(list(parser.parse(data.splitlines(), quiet=True, ignore_exceptions=True)), expected)

    def test_tsv_s_jc_meta_column_ignore_exceptions(self):
        """
        Test 'tsv_s' with a column named _jc_meta and ignore_exceptions=True:
        the column is replaced by the _jc_meta success object
        """
        data = ['a\t_jc_meta', '1\tfrom the file']
        expected = [{'a': '1', '_jc_meta': {'success': True}}]
        self.assertEqual(list(jc.parsers.tsv_s.parse(data, quiet=True, ignore_exceptions=True)), expected)


    def test_csv_s_multiline_cell(self):
        """
        Test 'csv_s' with line breaks and a blank line inside quoted fields, with and without line endings in the input lines
        """
        data = 'id,name,note\n7,"ad\nmin",x\n8,"para one\n\npara two",y\n\n9,z,"last"\n'
        expected = [
            {'id': '7', 'name': 'ad\nmin', 'note': 'x'},
            {'id': '8', 'name': 'para one\n\npara two', 'note': 'y'},
            {'id': '9', 'name': 'z', 'note': 'last'}
        ]
        self.assertEqual(list(jc.parsers.csv_s.parse(data.splitlines(keepends=True), quiet=True)), expected)
        self.assertEqual(list(jc.parsers.csv_s.parse(data.split('\n'), quiet=True)), expected)

    def test_csv_s_multiline_cell_crlf(self):
        """
        Test 'csv_s' with a line break inside a quoted field in CRLF text split on LF
        """
        data = 'id,name\r\n7,"ad\r\nmin"\r\n8,b\r\n'
        expected = [
            {'id': '7', 'name': 'ad\r\nmin'},
            {'id': '8', 'name': 'b'}
        ]
        self.assertEqual(list(jc.parsers.csv_s.parse(data.split('\n'), quiet=True)), expected)

    def test_csv_s_multiline_cell_after_100_lines(self):
        """
        Test 'csv_s' with the same multi-line quoted field in the first 100 lines and after them
        """
        data = ['id,name', '7,"ad', 'min"'] + [f'{i},x' for i in range(100)] + ['8,"ad', 'min"']
        result = list(jc.parsers.csv_s.parse(data, quiet=True))
        self.assertEqual(len(result), 102)
        self.assertEqual(result[0], {'id': '7', 'name': 'ad\nmin'})
        self.assertEqual(result[1], {'id': '0', 'name': 'x'})
        self.assertEqual(result[-1], {'id': '8', 'name': 'ad\nmin'})

    def test_csv_s_multiline_cell_wrappers(self):
        """
        Test 'tsv_s', 'csv_ih_s' and 'tsv_ih_s' with a line break inside a quoted field
        """
        self.assertEqual(list(jc.parsers.tsv_s.parse(['a\tb', '1\t"x', 'y"'], quiet=True)), [{'a': '1', 'b': 'x\ny'}])
        self.assertEqual(list(jc.parsers.csv_ih_s.parse(['1,"x', 'y"', '2,z'], quiet=True)), [{'c0': '1', 'c1': 'x\ny'}, {'c0': '2', 'c1': 'z'}])
        self.assertEqual(list(jc.parsers.tsv_ih_s.parse(['1\t"x', 'y"', '2\tz'], quiet=True)), [{'c0': '1', 'c1': 'x\ny'}, {'c0': '2', 'c1': 'z'}])

    def test_tsv_s_trailing_empty_fields(self):
        """
        Test 'tsv_s' with empty fields at the end of a row in the first 100 lines
        """
        self.assertEqual(list(jc.parsers.tsv_s.parse(['a\tb\tc', '1\t\t'], quiet=True)), [{'a': '1', 'b': '', 'c': ''}])


    def test_csv_s_reader_error_ignore_exceptions(self):
        """
        Test 'csv_s' with ignore_exceptions=True and rows the csv module rejects (a field over the size limit, a CR in an unquoted field): parsing continues at the next row
        """
        long_field = 'A' * 131073
        data = ['user,comment', 'alice,first', 'bob,' + long_field, 'carol,second', 'dave,x\ry', 'erin,third']
        result = list(jc.parsers.csv_s.parse(data, quiet=True, ignore_exceptions=True))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], {'user': 'alice', 'comment': 'first', '_jc_meta': {'success': True}})
        self.assertFalse(result[1]['_jc_meta']['success'])
        self.assertEqual(result[1]['_jc_meta']['error'], 'Error: field larger than field limit (131072)')
        self.assertEqual(result[1]['_jc_meta']['line'], 'bob,' + long_field)
        self.assertEqual(result[2], {'user': 'carol', 'comment': 'second', '_jc_meta': {'success': True}})
        self.assertFalse(result[3]['_jc_meta']['success'])
        self.assertIn('new-line character seen in unquoted field', result[3]['_jc_meta']['error'])
        self.assertEqual(result[3]['_jc_meta']['line'], 'dave,x\ry')
        self.assertEqual(result[4], {'user': 'erin', 'comment': 'third', '_jc_meta': {'success': True}})

    def test_csv_s_reader_error_multiline_ignore_exceptions(self):
        """
        Test 'csv_s' with ignore_exceptions=True and a field over the size limit inside a multi-line quoted field: the rest of the quoted field is not parsed as rows
        """
        long_field = 'A' * 131073
        data = ['user,role', 'alice,user', 'bob,"x', long_field, 'root,admin', 'erin,admin"', 'carol,user']
        result = list(jc.parsers.csv_s.parse(data, quiet=True, ignore_exceptions=True))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {'user': 'alice', 'role': 'user', '_jc_meta': {'success': True}})
        self.assertFalse(result[1]['_jc_meta']['success'])
        self.assertEqual(result[1]['_jc_meta']['line'], '\n'.join(data[2:4]))
        self.assertEqual(result[2], {'user': 'carol', 'role': 'user', '_jc_meta': {'success': True}})

    def test_csv_s_reader_error(self):
        """
        Test 'csv_s' without ignore_exceptions and a field over the size limit: the error is raised
        """
        data = ['user,comment', 'alice,first', 'bob,' + 'A' * 131073, 'carol,second']
        g = jc.parsers.csv_s.parse(data, quiet=True)
        self.assertEqual(next(g), {'user': 'alice', 'comment': 'first'})
        with self.assertRaises(csv.Error):
            next(g)

    def test_csv_s_reader_error_header(self):
        """
        Test 'csv_s' with ignore_exceptions=True and a header row the csv module rejects: ParseError is raised
        """
        data = ['user,' + 'A' * 131073, '1,2', '3,4']
        with self.assertRaises(ParseError):
            list(jc.parsers.csv_s.parse(data, quiet=True, ignore_exceptions=True))

    def test_csv_s_reader_error_wrappers_ignore_exceptions(self):
        """
        Test 'tsv_s', 'csv_ih_s' and 'tsv_ih_s' with ignore_exceptions=True and a CR in an unquoted field
        """
        cases = [
            (jc.parsers.tsv_s, ['a\tb', '1\tx\ry', '2\tz'], {'a': '2', 'b': 'z', '_jc_meta': {'success': True}}),
            (jc.parsers.csv_ih_s, ['0,w', '1,x\ry', '2,z'], {'c0': '2', 'c1': 'z', '_jc_meta': {'success': True}}),
            (jc.parsers.tsv_ih_s, ['0\tw', '1\tx\ry', '2\tz'], {'c0': '2', 'c1': 'z', '_jc_meta': {'success': True}}),
        ]
        for parser, data, last in cases:
            result = list(parser.parse(data, quiet=True, ignore_exceptions=True))
            self.assertFalse(result[-2]['_jc_meta']['success'])
            self.assertEqual(result[-2]['_jc_meta']['line'], data[1])
            self.assertEqual(result[-1], last)


if __name__ == '__main__':
    unittest.main()
