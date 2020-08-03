import os
import json
import unittest
import jc.parsers.date

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date.out'), 'r', encoding='utf-8') as f:
            self.generic_date = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date.json'), 'r', encoding='utf-8') as f:
            self.generic_date_json = json.loads(f.read())

    def test_date_nodata(self):
        """
        Test 'date' with no data
        """
        self.assertEqual(jc.parsers.date.parse('', quiet=True), {})

    def test_date(self):
        """
        Test 'date'
        """
        self.assertEqual(jc.parsers.date.parse(self.generic_date, quiet=True), self.generic_date_json)


if __name__ == '__main__':
    unittest.main()
