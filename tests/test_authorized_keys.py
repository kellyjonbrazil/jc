import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()


class MyTests(unittest.TestCase):

    def test_authorized_keys_nodata(self):
        """
        Test 'authorized_keys' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_authorized_keys_all_fixtures(self):
        """
        Test 'authorized_keys' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)


if __name__ == '__main__':
    unittest.main()
