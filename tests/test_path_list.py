import unittest
import jc.parsers.path_list
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()


class MyTests(unittest.TestCase):

    def test_path_list_nodata(self):
        """
        Test 'path_list' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_path_list_all_fixtures(self):
        """
        Test 'path_list' with various logs
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_path_list_blank_and_empty_entries(self):
        """
        Test 'path_list' with whitespace-only input and empty entries
        """
        self.assertEqual(jc.parsers.path_list.parse('   \n', quiet=True), [])
        self.assertEqual(jc.parsers.path_list.parse('', quiet=True), [])
        self.assertEqual(len(jc.parsers.path_list.parse('/a::/b', quiet=True)), 3)


if __name__ == '__main__':
    unittest.main()
