import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
import jc.parsers.curl_head
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


    def test_curl_head_whitespace_only_line(self):
        """
        Test 'curl_head' with whitespace-only lines
        """
        data = 'GET / HTTP/1.1\nHost: example.com\n \nAccept: */*\n'
        expected = [
            {
                '_type': 'request',
                '_request_method': 'GET',
                '_request_uri': '/',
                '_request_version': 'HTTP/1.1',
                'host': 'example.com',
                'accept': ['*/*']
            }
        ]
        self.assertEqual(jc.parsers.curl_head.parse(data, quiet=True), expected)


    def test_curl_head_line_separator(self):
        """
        Test 'curl_head' with a line-break character other than LF inside a field
        """
        data = '*   Trying 127.0.0.1:80...\n> HEAD /download/1 HTTP/1.1\n> \n< HTTP/1.1 200 OK\n< Content-Disposition: attachment; filename="a.txt"\u2028> POST /admin HTTP/1.1\u2028< HTTP/1.1 201 Created\u2028< X-Rest: ""\n< X-Content-Type-Options: nosniff\n< \n'
        result = jc.parsers.curl_head.parse(data, quiet=True)
        self.assertEqual([x['_type'] for x in result], ['request', 'response'])
        self.assertEqual(result[1]['content-disposition'], 'attachment; filename="a.txt"\u2028> POST /admin HTTP/1.1\u2028< HTTP/1.1 201 Created\u2028< X-Rest: ""')
        self.assertEqual(result[1]['x-content-type-options'], 'nosniff')


if __name__ == '__main__':
    unittest.main()
