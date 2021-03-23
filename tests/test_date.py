import os
import json
import time
import unittest
import jc.parsers.date

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
time.tzset()


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date.out'), 'r', encoding='utf-8') as f:
            self.generic_date = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/date.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_20_04_date = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date.json'), 'r', encoding='utf-8') as f:
            self.generic_date_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/date.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_20_04_date_json = json.loads(f.read())

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

    def test_date_ubuntu_20_04(self):
        """
        Test 'date' on Ubuntu 20.4
        """
        self.assertEqual(jc.parsers.date.parse(self.ubuntu_20_04_date, quiet=True), self.ubuntu_20_04_date_json)


if __name__ == '__main__':
    unittest.main()
