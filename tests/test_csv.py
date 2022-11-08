import os
import json
import unittest
import jc.parsers.csv

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-utf-8-bom.csv'), 'r', encoding='utf-8') as f:
        generic_csv_utf8_bom = f.read()

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-utf-8-bom.json'), 'r', encoding='utf-8') as f:
        generic_csv_utf8_bom_json = json.loads(f.read())


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


if __name__ == '__main__':
    unittest.main()
