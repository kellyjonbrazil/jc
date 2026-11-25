import os
import unittest
import json
import jc.parsers.cef

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef.out'), 'r', encoding='utf-8') as f:
        cef = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef.json'), 'r', encoding='utf-8') as f:
        cef_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-unescaped-equals.out'), 'r', encoding='utf-8') as f:
        cef_unescaped_equals = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-unescaped-equals.json'), 'r', encoding='utf-8') as f:
        cef_unescaped_equals_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-equals-in-header.out'), 'r', encoding='utf-8') as f:
        cef_equals_in_header = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-equals-in-header.json'), 'r', encoding='utf-8') as f:
        cef_equals_in_header_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-custom-labels.out'), 'r', encoding='utf-8') as f:
        cef_custom_labels = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-custom-labels.json'), 'r', encoding='utf-8') as f:
        cef_custom_labels_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-escaped-backslash.out'), 'r', encoding='utf-8') as f:
        cef_escaped_backslash = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef-escaped-backslash.json'), 'r', encoding='utf-8') as f:
        cef_escaped_backslash_json = json.loads(f.read())

    def test_cef_nodata(self):
        """
        Test 'cef' with no data
        """
        self.assertEqual(jc.parsers.cef.parse('', quiet=True), [])

    def test_cef_sample(self):
        """
        Test with sample cef log
        """
        self.assertEqual(jc.parsers.cef.parse(self.cef, quiet=True), self.cef_json)

    def test_cef_unescaped_equals(self):
        """
        Test cef lines with tokens that are not part of a key=value pair
        (unescaped '=' in values, no '=' at all)
        """
        self.assertEqual(jc.parsers.cef.parse(self.cef_unescaped_equals, quiet=True), self.cef_unescaped_equals_json)

    def test_cef_long_token_without_value(self):
        """
        Test that long tokens that are not part of a key=value pair are
        parsed in linear time
        """
        header = 'CEF:0|Vendor|Product|1.0|100|Name|5|'
        for msg in ('c' * 35000 + '=', 'c\\=' * 12000 + '='):
            data = header + 'src=10.0.0.1 msg=' + msg + ' dst=2.1.2.2'
            result = jc.parsers.cef.parse(data, quiet=True)
            self.assertEqual(result[0]['src'], '10.0.0.1')
            self.assertEqual(result[0]['dst'], '2.1.2.2')


    def test_cef_line_separator(self):
        """
        Test 'cef' with a line-break character other than LF inside a field
        """
        data = 'CEF:0|V|P|1|100|name|5|msg=hi\u2028CEF:0|V|P|1|999|other|10|msg=x\n'
        result = jc.parsers.cef.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['deviceEventClassId'], '100')
        self.assertEqual(result[0]['agentSeverity'], '5')
        self.assertEqual(result[0]['name'], 'name')

        data = 'CEF:0|V|P|1|100|name|5|msg=hi\u2028there src=1.2.3.4\n'
        result = jc.parsers.cef.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['msg'], 'hi\u2028there')
        self.assertEqual(result[0]['src'], '1.2.3.4')

    def test_cef_equals_in_header(self):
        """
        Test cef lines with '=' and escaped pipes in the header fields
        """
        self.assertEqual(jc.parsers.cef.parse(self.cef_equals_in_header, quiet=True), self.cef_equals_in_header_json)

    def test_cef_custom_labels(self):
        """
        Test cef lines with custom field labels, including epoch fields and unmatched labels
        """
        self.assertEqual(jc.parsers.cef.parse(self.cef_custom_labels, quiet=True), self.cef_custom_labels_json)

    def test_cef_escaped_backslash(self):
        """
        Test cef lines with escaped backslashes followed by escapable characters
        """
        self.assertEqual(jc.parsers.cef.parse(self.cef_escaped_backslash, quiet=True), self.cef_escaped_backslash_json)

    def test_cef_float_non_finite(self):
        """
        Test 'cef' with float fields of inf, nan and 1e999: the text is kept
        """
        data = 'CEF:0|Acme|Sensor|1|100|heartbeat|3|cfp1=1e999 cfp2=nan cfp3=-inf cfp4=2.5\n'
        result = jc.parsers.cef.parse(data, quiet=True)
        self.assertEqual(result[0]['cfp1'], '1e999')
        self.assertEqual(result[0]['cfp2'], 'nan')
        self.assertEqual(result[0]['cfp3'], '-inf')
        self.assertEqual(result[0]['cfp4'], 2.5)


if __name__ == '__main__':
    unittest.main()
