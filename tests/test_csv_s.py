import os
import json
import unittest
import jc.parsers.csv_s
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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-utf-8-bom.csv'), 'r', encoding='utf-8') as f:
        generic_csv_utf8_bom = f.read()

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-utf-8-bom-streaming.json'), 'r', encoding='utf-8') as f:
        generic_csv_utf8_bom_streaming_json = json.loads(f.read())


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

    def test_csv_s_utf8_bom(self):
        """
        Test 'csv-utf-8-bom.csv' file to ensure the first column is correct if UTF-8 BOM bytes are present
        """
        self.assertEqual(list(jc.parsers.csv_s.parse(self.generic_csv_utf8_bom.splitlines(), quiet=True)), self.generic_csv_utf8_bom_streaming_json)


if __name__ == '__main__':
    unittest.main()
