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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-custom-labels.out'), 'r', encoding='utf-8') as f:
        cef_custom_labels = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-custom-labels-streaming.json'), 'r', encoding='utf-8') as f:
        cef_custom_labels_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-escaped-backslash.out'), 'r', encoding='utf-8') as f:
        cef_escaped_backslash = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-escaped-backslash-streaming.json'), 'r', encoding='utf-8') as f:
        cef_escaped_backslash_streaming_json = json.loads(f.read())

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

    def test_cef_s_custom_labels(self):
        """
        Test cef lines with custom field labels, including epoch fields and unmatched labels
        """
        self.assertEqual(list(jc.parsers.cef_s.parse(self.cef_custom_labels.splitlines(), quiet=True)), self.cef_custom_labels_streaming_json)

    def test_cef_s_escaped_backslash(self):
        """
        Test cef lines with escaped backslashes followed by escapable characters
        """
        self.assertEqual(list(jc.parsers.cef_s.parse(self.cef_escaped_backslash.splitlines(), quiet=True)), self.cef_escaped_backslash_streaming_json)

    def test_cef_s_float_non_finite(self):
        """
        Test 'cef_s' with float fields of inf, nan and 1e999: the text is kept
        """
        data = ['CEF:0|Acme|Sensor|1|100|heartbeat|3|cfp1=1e999 cfp2=nan cfp3=-inf cfp4=2.5']
        result = list(jc.parsers.cef_s.parse(data, quiet=True))
        self.assertEqual(result[0]['cfp1'], '1e999')
        self.assertEqual(result[0]['cfp2'], 'nan')
        self.assertEqual(result[0]['cfp3'], '-inf')
        self.assertEqual(result[0]['cfp4'], 2.5)


    def test_cef_s_unparsable_ignore_exceptions(self):
        """
        Test 'cef_s' with unparsable lines: an unparsable record without ignore_exceptions, an error record with it
        """
        data = ['CEF:0|Acme||1.0|100|Login failed|8|src=10.0.0.2', 'not a CEF line', 'CEF:0|Acme|Gateway|1.0|100|Login|3|src=10.0.0.3']
        result = list(jc.parsers.cef_s.parse(data, quiet=True))
        self.assertEqual(result[0], {'unparsable': data[0]})
        self.assertEqual(result[1], {'unparsable': data[1]})
        self.assertEqual(result[2]['src'], '10.0.0.3')

        result = list(jc.parsers.cef_s.parse(data, quiet=True, ignore_exceptions=True))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {'_jc_meta': {'success': False, 'error': 'ParseError: Blank field(s) in CEF header. Is it valid CEF format?', 'line': data[0]}})
        self.assertEqual(result[1], {'_jc_meta': {'success': False, 'error': 'ParseError: Could not parse record. Is it valid CEF format?', 'line': data[1]}})
        self.assertEqual(result[2]['src'], '10.0.0.3')
        self.assertEqual(result[2]['deviceProduct'], 'Gateway')
        self.assertEqual(result[2]['_jc_meta'], {'success': True})


if __name__ == '__main__':
    unittest.main()
