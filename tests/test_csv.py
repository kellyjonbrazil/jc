import os
import json
import unittest
import jc.parsers.csv

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-biostats.csv'), 'r') as f:
            self.generic_csv_biostats = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-cities.csv'), 'r') as f:
            self.generic_csv_cities = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-deniro.csv'), 'r') as f:
            self.generic_csv_deniro = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-example.csv'), 'r') as f:
            self.generic_csv_example = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna.tsv'), 'r') as f:
            self.generic_csv_flyrna = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna2.tsv'), 'r') as f:
            self.generic_csv_flyrna2 = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-pipe.csv'), 'r') as f:
            self.generic_csv_homes_pipe = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes.csv'), 'r') as f:
            self.generic_csv_homes = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-insurance.csv'), 'r') as f:
            self.generic_csv_insurance = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-biostats.json'), 'r') as f:
            self.generic_csv_biostats_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-cities.json'), 'r') as f:
            self.generic_csv_cities_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-deniro.json'), 'r') as f:
            self.generic_csv_deniro_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-example.json'), 'r') as f:
            self.generic_csv_example_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna.json'), 'r') as f:
            self.generic_csv_flyrna_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna2.json'), 'r') as f:
            self.generic_csv_flyrna2_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-pipe.json'), 'r') as f:
            self.generic_csv_homes_pipe_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes.json'), 'r') as f:
            self.generic_csv_homes_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-insurance.json'), 'r') as f:
            self.generic_csv_insurance_json = json.loads(f.read())

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


if __name__ == '__main__':
    unittest.main()
