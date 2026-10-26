import os
import json
import unittest
import jc.parsers.cef_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat cef.out | jc --cef-s | jello -c > cef-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef.out'), 'r', encoding='utf-8') as f:
        cef = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-streaming.json'), 'r', encoding='utf-8') as f:
        cef_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-unescaped-equals.out'), 'r', encoding='utf-8') as f:
        cef_unescaped_equals = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-unescaped-equals-streaming.json'), 'r', encoding='utf-8') as f:
        cef_unescaped_equals_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-equals-in-header.out'), 'r', encoding='utf-8') as f:
        cef_equals_in_header = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-equals-in-header-streaming.json'), 'r', encoding='utf-8') as f:
        cef_equals_in_header_streaming_json = json.loads(f.read())

    def test_cef_s_nodata(self):
        """
        Test 'cef' with no data
        """
        self.assertEqual(list(jc.parsers.cef_s.parse([], quiet=True)), [])

    def test_cef_s_sample(self):
        """
        Test with sample cef log
        """
        self.assertEqual(list(jc.parsers.cef_s.parse(self.cef.splitlines(), quiet=True)), self.cef_streaming_json)

    def test_cef_s_unescaped_equals(self):
        """
        Test cef lines with tokens that are not part of a key=value pair
        (unescaped '=' in values, no '=' at all)
        """
        self.assertEqual(list(jc.parsers.cef_s.parse(self.cef_unescaped_equals.splitlines(), quiet=True)), self.cef_unescaped_equals_streaming_json)


    def test_cef_s_crlf_lines(self):
        """
        Test cef with CRLF line endings, split on LF or with line endings kept
        """
        crlf_data = self.cef.replace('\n', '\r\n')
        self.assertEqual(list(jc.parsers.cef_s.parse(crlf_data.split('\n'), quiet=True)), self.cef_streaming_json)
        self.assertEqual(list(jc.parsers.cef_s.parse(crlf_data.splitlines(keepends=True), quiet=True)), self.cef_streaming_json)

    def test_cef_s_equals_in_header(self):
        """
        Test cef lines with '=' and escaped pipes in the header fields
        """
        self.assertEqual(list(jc.parsers.cef_s.parse(self.cef_equals_in_header.splitlines(), quiet=True)), self.cef_equals_in_header_streaming_json)


if __name__ == '__main__':
    unittest.main()
