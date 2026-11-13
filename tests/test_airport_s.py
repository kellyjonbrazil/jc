import os
import unittest
import json
import jc.parsers.airport_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/airport-s.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_airport_s = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/airport-s.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_airport_s_json = json.loads(f.read())

    def test_airport_s_nodata(self):
        """
        Test 'airport -s' with no data
        """
        self.assertEqual(jc.parsers.airport_s.parse('', quiet=True), [])

    def test_airport_s_osx_10_14_6(self):
        """
        Test 'airport -s' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.airport_s.parse(self.osx_10_14_6_airport_s, quiet=True), self.osx_10_14_6_airport_s_json)


    def test_airport_s_line_separator(self):
        """
        Test 'airport_s' with a line-break character other than LF inside a field
        """
        data = '                            SSID BSSID             RSSI CHANNEL HT CC SECURITY (auth/unicast/group)\n                    Guest\x0cLounge 02:de:ad:be:ef:01 -40  6       Y  US NONE\n'
        result = jc.parsers.airport_s.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['ssid'], 'Guest\x0cLounge')
        self.assertEqual(result[0]['bssid'], '02:de:ad:be:ef:01')


if __name__ == '__main__':
    unittest.main()
