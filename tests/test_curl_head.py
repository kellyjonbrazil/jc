import unittest
import os
import sys
import io
import json
import contextlib
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

    def test_curl_head_reserved_names(self):
        """
        Test 'curl_head' ignores headers named like generated keys
        """
        data = '* Connected\n> HEAD / HTTP/1.1\n> Host: a\n> \n' + ''.join('< ' + x + '\n' for x in self.reserved_in.splitlines())
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            result = jc.parsers.curl_head.parse(data)
        self.assertEqual(result[1], self.reserved_json[0])
        self.assertEqual(result[0]['_type'], 'request')
        self.assertIn('_response_status', err.getvalue())

        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            jc.parsers.curl_head.parse(data, quiet=True)
        self.assertEqual(err.getvalue(), '')

    def test_curl_head_header_names(self):
        """
        Test 'curl_head' with headers named like a method or HTTP version and headers with no space after the colon
        """
        data = '* Connected\n> HEAD / HTTP/1.1\n> Host: a\n> \n' + ''.join('< ' + x + '\n' for x in self.header_names_in.splitlines())
        result = jc.parsers.curl_head.parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['_type'], 'request')
        self.assertEqual(result[1], self.header_names_json[0])


if __name__ == '__main__':
    unittest.main()
