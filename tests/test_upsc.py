import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc.parsers.upsc


class MyTests(unittest.TestCase):

    def test_upsc_nodata(self):
        """
        Test 'upsc' with no data
        """
        test_utils.run_no_data(self, __file__, {})

    def test_upsc_all_fixtures(self):
        """
        Test 'upsc' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_upsc_non_finite_values(self):
        """
        Test 'upsc' with values of nan and inf: the text is kept
        """
        data = 'battery.charge: nan\nbattery.runtime: inf\nbattery.voltage: 13.5\n'
        expected = {'battery_charge': 'nan', 'battery_runtime': 'inf', 'battery_voltage': 13.5}
        self.assertEqual(jc.parsers.upsc.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
