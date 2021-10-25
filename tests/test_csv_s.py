import os
import json
import unittest
import jc.parsers.csv_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# To create streaming output use:
# $ cat file.csv | jc --csv-s | jello -c > csv-file-streaming.json


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-biostats.csv'), 'r', encoding='utf-8') as f:
            self.generic_csv_biostats = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-cities.csv'), 'r', encoding='utf-8') as f:
            self.generic_csv_cities = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-deniro.csv'), 'r', encoding='utf-8') as f:
            self.generic_csv_deniro = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-example.csv'), 'r', encoding='utf-8') as f:
            self.generic_csv_example = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna.tsv'), 'r', encoding='utf-8') as f:
            self.generic_csv_flyrna = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna2.tsv'), 'r', encoding='utf-8') as f:
            self.generic_csv_flyrna2 = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-pipe.csv'), 'r', encoding='utf-8') as f:
            self.generic_csv_homes_pipe = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes.csv'), 'r', encoding='utf-8') as f:
            self.generic_csv_homes = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-insurance.csv'), 'r', encoding='utf-8') as f:
            self.generic_csv_insurance = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-biostats-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_csv_biostats_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-cities-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_csv_cities_streaming_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-deniro-streaming.json'), 'r', encoding='utf-8') as f:
        #     self.generic_csv_deniro_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-example-streaming.json'), 'r', encoding='utf-8') as f:
        #     self.generic_csv_example_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna-streaming.json'), 'r', encoding='utf-8') as f:
        #     self.generic_csv_flyrna_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-flyrna2-streaming.json'), 'r', encoding='utf-8') as f:
        #     self.generic_csv_flyrna2_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-pipe-streaming.json'), 'r', encoding='utf-8') as f:
        #     self.generic_csv_homes_pipe_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-homes-streaming.json'), 'r', encoding='utf-8') as f:
        #     self.generic_csv_homes_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/csv-insurance-streaming.json'), 'r', encoding='utf-8') as f:
        #     self.generic_csv_insurance_json = json.loads(f.read())

    def test_csv_s_nodata(self):
        """
        Test CSV parser with no data
        """
        self.assertEqual(list(jc.parsers.csv_s.parse('', quiet=True)), [])

    # no test for unparsable rows yet - CSV library fails right away if it can't decode the data
    # def test_csv_unparsable(self):
    #     data = 'unparsable data'
    #     g = jc.parsers.csv_s.parse(data.splitlines(), quiet=True)
    #     with self.assertRaises(ParseError):
    #         list(g)

    # def test_vmstat_centos_7_7(self):
    #     """
    #     Test 'vmstat' on Centos 7.7
    #     """
    #     self.assertEqual(list(jc.parsers.vmstat_s.parse(self.centos_7_7_vmstat.splitlines(), quiet=True)), self.centos_7_7_vmstat_streaming_json)

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

    # def test_csv_deniro(self):
    #     """
    #     Test 'deniro.csv' file
    #     """
    #     self.assertEqual(jc.parsers.csv.parse(self.generic_csv_deniro, quiet=True), self.generic_csv_deniro_json)

    # def test_csv_example(self):
    #     """
    #     Test 'example.csv' file
    #     """
    #     self.assertEqual(jc.parsers.csv.parse(self.generic_csv_example, quiet=True), self.generic_csv_example_json)

    # def test_csv_flyrna(self):
    #     """
    #     Test 'flyrna.tsv' file
    #     """
    #     self.assertEqual(jc.parsers.csv.parse(self.generic_csv_flyrna, quiet=True), self.generic_csv_flyrna_json)

    # def test_csv_flyrna2(self):
    #     """
    #     Test 'flyrna2.tsv' file
    #     """
    #     self.assertEqual(jc.parsers.csv.parse(self.generic_csv_flyrna2, quiet=True), self.generic_csv_flyrna2_json)

    # def test_csv_homes_pipe(self):
    #     """
    #     Test 'homes-pipe.csv' file
    #     """
    #     self.assertEqual(jc.parsers.csv.parse(self.generic_csv_homes_pipe, quiet=True), self.generic_csv_homes_pipe_json)

    # def test_csv_homes(self):
    #     """
    #     Test 'homes.csv' file
    #     """
    #     self.assertEqual(jc.parsers.csv.parse(self.generic_csv_homes, quiet=True), self.generic_csv_homes_json)

    # def test_csv_insurance(self):
    #     """
    #     Test 'insurance.csv' file
    #     """
    #     self.assertEqual(jc.parsers.csv.parse(self.generic_csv_insurance, quiet=True), self.generic_csv_insurance_json)


if __name__ == '__main__':
    unittest.main()
