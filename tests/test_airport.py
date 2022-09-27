import os
import unittest
import json
import jc.parsers.airport

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/airport-I.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_airport_I = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/airport-I.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_airport_I_json = json.loads(f.read())

    def test_airport_I_nodata(self):
        """
        Test 'airport -I' with no data
        """
        self.assertEqual(jc.parsers.airport.parse('', quiet=True), {})

    def test_airport_I_osx_10_14_6(self):
        """
        Test 'airport -I' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.airport.parse(self.osx_10_14_6_airport_I, quiet=True), self.osx_10_14_6_airport_I_json)


if __name__ == '__main__':
    unittest.main()
