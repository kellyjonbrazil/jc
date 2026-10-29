import os
import json
import unittest
import jc.parsers.csv
import jc.parsers.csv_ih
import jc.parsers.tsv
import jc.parsers.tsv_ih

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-insurance.csv'), 'r', encoding='utf-8') as f:
        generic_csv_insurance = f.read()

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
        generic_tsv_ih_dpkg_query_csv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv-dpkg-query.tsv'), 'r', encoding='utf-8') as f:
        generic_tsv_dpkg_query_csv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv_ih-simple-double-quote.tsv'), 'r', encoding='utf-8') as f:
        generic_tsv_simple_double_quote_csv = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-biostats.json'), 'r', encoding='utf-8') as f:
        generic_csv_biostats_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-cities.json'), 'r', encoding='utf-8') as f:
        generic_csv_cities_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-deniro.json'), 'r', encoding='utf-8') as f:
        generic_csv_deniro_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-example.json'), 'r', encoding='utf-8') as f:
        generic_csv_example_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna.json'), 'r', encoding='utf-8') as f:
        generic_csv_flyrna_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna2.json'), 'r', encoding='utf-8') as f:
        generic_csv_flyrna2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-pipe.json'), 'r', encoding='utf-8') as f:
        generic_csv_homes_pipe_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes.json'), 'r', encoding='utf-8') as f:
        generic_csv_homes_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-insurance.json'), 'r', encoding='utf-8') as f:
        generic_csv_insurance_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-doublequoted.json'), 'r', encoding='utf-8') as f:
        generic_csv_doublequoted_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-apostrophes.json'), 'r', encoding='utf-8') as f:
        generic_csv_apostrophes_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-apostrophes-pipe.json'), 'r', encoding='utf-8') as f:
        generic_csv_apostrophes_pipe_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-utf-8-bom.json'), 'r', encoding='utf-8') as f:
        generic_csv_utf8_bom_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv_ih-homes.json'), 'r', encoding='utf-8') as f:
        generic_csv_ih_homes_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv_ih-jagged.json'), 'r', encoding='utf-8') as f:
        generic_csv_ih_jagged_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv_ih-dpkg-query.json'), 'r', encoding='utf-8') as f:
        generic_tsv_ih_dpkg_query_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv-dpkg-query.json'), 'r', encoding='utf-8') as f:
        generic_tsv_dpkg_query_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tsv_ih-simple-double-quote.json'), 'r', encoding='utf-8') as f:
        generic_tsv_simple_double_quote_json = json.loads(f.read())


    def test_csv_line_separators(self):
        """
        Test 'csv' with a line-break character other than LF in the first data row
        """
        data = 'name;note\nfoo;a\u2028b,c\nbar;c\n'
        result = jc.parsers.csv.parse(data, quiet=True)
        self.assertEqual(result[0], {'name': 'foo', 'note': 'a\u2028b,c'})
        self.assertEqual(result[1], {'name': 'bar', 'note': 'c'})

    def test_csv_nodata(self):
        """
        Test with no data
        """
        self.assertEqual(jc.parsers.csv.parse('', quiet=True), [])

    def test_csv_biostats(self):
        """
        Test 'biostats.csv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_biostats, quiet=True), self.generic_csv_biostats_json)

    def test_csv_cities(self):
        """
        Test 'cities.csv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_cities, quiet=True), self.generic_csv_cities_json)

    def test_csv_deniro(self):
        """
        Test 'deniro.csv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_deniro, quiet=True), self.generic_csv_deniro_json)

    def test_csv_example(self):
        """
        Test 'example.csv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_example, quiet=True), self.generic_csv_example_json)

    def test_csv_flyrna(self):
        """
        Test 'flyrna.tsv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_flyrna, quiet=True), self.generic_csv_flyrna_json)

    def test_csv_flyrna2(self):
        """
        Test 'flyrna2.tsv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_flyrna2, quiet=True), self.generic_csv_flyrna2_json)

    def test_csv_homes_pipe(self):
        """
        Test 'homes-pipe.csv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_homes_pipe, quiet=True), self.generic_csv_homes_pipe_json)

    def test_csv_homes(self):
        """
        Test 'homes.csv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_homes, quiet=True), self.generic_csv_homes_json)

    def test_csv_insurance(self):
        """
        Test 'insurance.csv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_insurance, quiet=True), self.generic_csv_insurance_json)

    def test_csv_doublequoted(self):
        """
        Test 'csv-doublequoted.csv' file
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_doublequoted, quiet=True), self.generic_csv_doublequoted_json)

    def test_csv_utf8_bom(self):
        """
        Test 'csv-utf-8-bom.csv' file to ensure the first column is correct if UTF-8 BOM bytes are present
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_utf8_bom, quiet=True), self.generic_csv_utf8_bom_json)

    def test_csv_ih_homes(self):
        """
        Test 'csv_ih-homes.csv' file in implicit header mode.
        """
        self.assertEqual(jc.parsers.csv_ih.parse(self.generic_csv_ih_homes_csv, quiet=True), self.generic_csv_ih_homes_json)

    def test_csv_ih_jagged(self):
        """
        Test 'csv_ih-jagged.csv' file in implicit header mode.
        """
        self.assertEqual(jc.parsers.csv_ih.parse(self.generic_csv_ih_jagged_csv, quiet=True), self.generic_csv_ih_jagged_json)

    def test_tsv_dpkg_query(self):
        """
        Test 'tsv-dpkg-query.tsv' file
        """
        self.assertEqual(jc.parsers.tsv.parse(self.generic_tsv_dpkg_query_csv, quiet=True), self.generic_tsv_dpkg_query_json)

    def test_tsv_ih_dpkg_query(self):
        """
        Test 'tsv_ih-dpkg-query.tsv' file in implicit header mode.
        """
        self.assertEqual(jc.parsers.tsv_ih.parse(self.generic_tsv_ih_dpkg_query_csv, quiet=True), self.generic_tsv_ih_dpkg_query_json)

    def test_tsv_simple_double_quote(self):
        """
        Test 'tsv_ih-simple-double-quote.tsv' file in implicit header mode.
        """
        self.assertEqual(jc.parsers.tsv_ih.parse(self.generic_tsv_simple_double_quote_csv, quiet=True), self.generic_tsv_simple_double_quote_json)


    def test_csv_line_separator(self):
        """
        Test 'csv' with a line-break character other than LF inside a field
        """
        data = 'id,role,name,note\n1,admin,alice,x\n2,user,bob\x0c99,admin\n'
        result = jc.parsers.csv.parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]['name'], 'bob\x0c99')

    def test_csv_cr_line_endings(self):
        """
        Test 'csv-insurance.csv' with CR-only line endings (file read without newline translation)
        """
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-insurance.csv'), 'r', encoding='utf-8', newline='') as f:
            data = f.read()
        self.assertIn('\r', data)
        self.assertNotIn('\n', data)
        self.assertEqual(jc.parsers.csv.parse(data, quiet=True), self.generic_csv_insurance_json)


    def test_csv_apostrophes(self):
        """
        Test 'csv-apostrophes.csv' file to ensure apostrophes in field values do not change the quote character
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_apostrophes, quiet=True), self.generic_csv_apostrophes_json)

    def test_csv_apostrophes_pipe(self):
        """
        Test 'csv-apostrophes-pipe.csv' file to ensure apostrophes and delimiters in field values do not change the dialect
        """
        self.assertEqual(jc.parsers.csv.parse(self.generic_csv_apostrophes_pipe, quiet=True), self.generic_csv_apostrophes_pipe_json)

    def test_csv_apostrophes_tab(self):
        """
        Test tab-delimited data with apostrophes in field values
        """
        data = 'id\tname\tnote\n1\talice\t"hi,\'x\',\'"\n2\tbob\tit\'s \'fine\', really\n'
        expected = [
            {'id': '1', 'name': 'alice', 'note': "hi,'x','"},
            {'id': '2', 'name': 'bob', 'note': "it's 'fine', really"}
        ]
        self.assertEqual(jc.parsers.csv.parse(data, quiet=True), expected)


    def test_csv_multiline_cell(self):
        """
        Test 'csv' with line breaks and a blank line inside quoted fields and a blank line between rows
        """
        data = 'id,name,note\n7,"ad\nmin",x\n8,"para one\n\npara two",y\n\n9,z,"last"\n'
        expected = [
            {'id': '7', 'name': 'ad\nmin', 'note': 'x'},
            {'id': '8', 'name': 'para one\n\npara two', 'note': 'y'},
            {'id': '9', 'name': 'z', 'note': 'last'}
        ]
        self.assertEqual(jc.parsers.csv.parse(data, quiet=True), expected)

    def test_csv_multiline_cell_crlf_cr(self):
        """
        Test 'csv' with line breaks inside quoted fields and blank lines in CRLF and CR-only files
        """
        for eol in ('\r\n', '\r'):
            data = f'{eol}{eol}id,name{eol}{eol}7,"ad{eol}min"{eol}{eol}8,b{eol}'
            expected = [
                {'id': '7', 'name': f'ad{eol}min'},
                {'id': '8', 'name': 'b'}
            ]
            self.assertEqual(jc.parsers.csv.parse(data, quiet=True), expected)

    def test_csv_multiline_cell_wrappers(self):
        """
        Test 'tsv', 'csv_ih' and 'tsv_ih' with a line break inside a quoted field
        """
        self.assertEqual(jc.parsers.tsv.parse('a\tb\n1\t"x\ny"\n', quiet=True), [{'a': '1', 'b': 'x\ny'}])
        self.assertEqual(jc.parsers.csv_ih.parse('1,"x\ny"\n2,z\n', quiet=True), [{'c0': '1', 'c1': 'x\ny'}, {'c0': '2', 'c1': 'z'}])
        self.assertEqual(jc.parsers.tsv_ih.parse('1\t"x\ny"\n2\tz\n', quiet=True), [{'c0': '1', 'c1': 'x\ny'}, {'c0': '2', 'c1': 'z'}])

    def test_tsv_ih_empty_first_row(self):
        """
        Test 'tsv_ih' with a first row of empty fields after leading blank lines
        """
        data = '\n\n\t\t\n1\t2\t3\n'
        expected = [
            {'c0': '', 'c1': '', 'c2': ''},
            {'c0': '1', 'c1': '2', 'c2': '3'}
        ]
        self.assertEqual(jc.parsers.tsv_ih.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
