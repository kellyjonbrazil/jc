import os
import unittest
import json
import jc.parsers.airport_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/airport-s.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_airport_s = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/airport-s.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_airport_s_json = json.loads(f.read())

    def test_airport_s_osx_10_14_6(self):
        """
        Test 'airport -s' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.airport_s.parse(self.osx_10_14_6_airport_s, quiet=True), self.osx_10_14_6_airport_s_json)


if __name__ == '__main__':
    unittest.main()
