import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()

# Execute these steps for standard tests:
# - Save this file as `test_{parser_name}.py` since the helper methods extract parser names from the filename.
# - Organize fixtures in `tests/fixtures` for optimal structure.
# - Format fixtures as follows (using double dashes):
#     - `{parser_name}--{some_test_description}.out` for command output.
#     - `{parser_name}--{some_test_description}.json` for expected JSON after parsing.

# create output with:
# curl -ILvs http://google.com 2> curl_head--ILvs-google-com.out
# cat curl_head--ILvs-google-com.out | jc --curl-head > curl_head--ILvs-google-com.json

class MyTests(unittest.TestCase):

    def test_curl_head_nodata(self):
        """
        Test 'curl_head' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_curl_head_all_fixtures(self):
        """
        Test 'curl_head' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)


if __name__ == '__main__':
    unittest.main()
