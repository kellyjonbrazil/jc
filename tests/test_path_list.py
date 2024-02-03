import unittest

from tests import utils_for_test as test_utils


class MyTests(unittest.TestCase):

    def test_path_nodata(self):
        """
        Test 'path_list' with no data
        """
        # self.assertEqual(parse('', quiet=True), [])
        test_utils.run_no_data(self, __file__, [])

    def test_all_fixtures(self):
        """
        Test 'path_list' with various logs
        """

        test_utils.run_all_fixtures(self, __file__)


if __name__ == '__main__':
    unittest.main()