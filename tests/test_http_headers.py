import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
import jc.parsers.http_headers
sys.path.pop()

# Execute these steps for standard tests:
# - Save this file as `test_{parser_name}.py` since the helper methods extract parser names from the filename.
# - Organize fixtures in `tests/fixtures` for optimal structure.
# - Format fixtures as follows (using double dashes):
#     - `{parser_name}--{some_test_description}.out` for command output.
#     - `{parser_name}--{some_test_description}.json` for expected JSON after parsing.

class MyTests(unittest.TestCase):

    def test_http_headers_nodata(self):
        """
        Test 'http_headers' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_http_headers_all_fixtures(self):
        """
        Test 'http_headers' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_http_headers_whitespace_only_line(self):
        """
        Test 'http_headers' with whitespace-only lines in request
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
        self.assertEqual(jc.parsers.http_headers.parse(data, quiet=True), expected)

    def test_http_headers_whitespace_in_response(self):
        """
        Test 'http_headers' with whitespace-only lines in response
        """
        data = 'HTTP/1.1 200 OK\n \t \nContent-Type: text/html\n  \nContent-Length: 12\n'
        expected = [
            {
                '_type': 'response',
                '_response_version': 'HTTP/1.1',
                '_response_status': 200,
                '_response_reason': ['OK'],
                'content-type': 'text/html',
                'content-length': 12
            }
        ]
        self.assertEqual(jc.parsers.http_headers.parse(data, quiet=True), expected)

    def test_http_headers_whitespace_between_messages(self):
        """
        Test 'http_headers' with whitespace-only lines separating request and response
        """
        data = (
            ' \n'
            'GET / HTTP/1.1\n'
            'Host: example.com\n'
            '  \t  \n'
            'HTTP/1.1 200 OK\n'
            'Content-Type: text/plain\n'
            ' \n'
        )
        expected = [
            {
                '_type': 'request',
                '_request_method': 'GET',
                '_request_uri': '/',
                '_request_version': 'HTTP/1.1',
                'host': 'example.com'
            },
            {
                '_type': 'response',
                '_response_version': 'HTTP/1.1',
                '_response_status': 200,
                '_response_reason': ['OK'],
                'content-type': 'text/plain'
            }
        ]
        self.assertEqual(jc.parsers.http_headers.parse(data, quiet=True), expected)

    def test_http_headers_whitespace_only_input(self):
        """
        Test 'http_headers' with input containing only whitespace characters
        """
        data = '   \n \t \n  \n'
        self.assertEqual(jc.parsers.http_headers.parse(data, quiet=True), [])


if __name__ == '__main__':
    unittest.main()
