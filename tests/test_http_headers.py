import unittest
import os
import sys
import io
import json
import contextlib
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc.parsers.http_headers

# Execute these steps for standard tests:
# - Save this file as `test_{parser_name}.py` since the helper methods extract parser names from the filename.
# - Organize fixtures in `tests/fixtures` for optimal structure.
# - Format fixtures as follows (using double dashes):
#     - `{parser_name}--{some_test_description}.out` for command output.
#     - `{parser_name}--{some_test_description}.json` for expected JSON after parsing.

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/http_headers--reserved-names.out'), 'r', encoding='utf-8') as f:
        reserved_in = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/http_headers--reserved-names.json'), 'r', encoding='utf-8') as f:
        reserved_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/http_headers--header-names.out'), 'r', encoding='utf-8') as f:
        header_names_in = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/http_headers--header-names.json'), 'r', encoding='utf-8') as f:
        header_names_json = json.loads(f.read())

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
        Test 'http_headers' with a whitespace-only line
        """
        data = 'GET / HTTP/1.1\nHost: example.com\n \nAccept: */*\n'
        expected = [{
            '_type': 'request',
            '_request_method': 'GET',
            '_request_uri': '/',
            '_request_version': 'HTTP/1.1',
            'host': 'example.com',
            'accept': ['*/*'],
        }]
        self.assertEqual(jc.parsers.http_headers.parse(data, quiet=True), expected)

    def test_http_headers_whitespace_only_line_in_response(self):
        """
        Test 'http_headers' with a whitespace-only line in a response
        """
        data = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\t \nServer: nginx\n'
        expected = [{
            '_type': 'response',
            '_response_version': 'HTTP/1.1',
            '_response_status': 200,
            '_response_reason': ['OK'],
            'content-type': 'text/html',
            'server': ['nginx'],
        }]
        self.assertEqual(jc.parsers.http_headers.parse(data, quiet=True), expected)


    def test_http_headers_line_separator(self):
        """
        Test 'http_headers' with a line-break character other than LF inside a field
        """
        data = 'HTTP/1.1 200 OK\r\nContent-Disposition: attachment; filename="a"\u2028HTTP/1.1 302 Found\u2028Location: https://example.com/\r\nContent-Length: 0\r\n\r\n'
        result = jc.parsers.http_headers.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['_response_status'], 200)
        self.assertEqual(result[0]['content-disposition'], 'attachment; filename="a"\u2028HTTP/1.1 302 Found\u2028Location: https://example.com/')

    def test_http_headers_reserved_names_warning(self):
        """
        Test 'http_headers' ignores headers named like generated keys and warns
        """
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            result = jc.parsers.http_headers.parse(self.reserved_in)
        self.assertEqual(result, self.reserved_json)
        self.assertIn('_response_status', err.getvalue())
        self.assertIn('date_epoch_utc', err.getvalue())

    def test_http_headers_reserved_names_quiet(self):
        """
        Test 'http_headers' ignores headers named like generated keys silently when quiet
        """
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            result = jc.parsers.http_headers.parse(self.reserved_in, quiet=True)
        self.assertEqual(result, self.reserved_json)
        self.assertEqual(err.getvalue(), '')

    def test_http_headers_reserved_names_raw(self):
        """
        Test 'http_headers' keeps generated keys intact in raw output
        """
        result = jc.parsers.http_headers.parse(self.reserved_in, raw=True, quiet=True)
        self.assertEqual(result[0]['_response_status'], 451)
        self.assertNotIn('date_epoch_utc', result[0])

    def test_http_headers_header_names(self):
        """
        Test 'http_headers' with headers named like a method or HTTP version and headers with no space after the colon
        """
        self.assertEqual(jc.parsers.http_headers.parse(self.header_names_in, quiet=True), self.header_names_json)


if __name__ == '__main__':
    unittest.main()
