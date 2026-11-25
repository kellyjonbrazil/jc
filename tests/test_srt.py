import os
import unittest
import json
import jc.parsers.srt

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-attack_of_the_clones.srt'), 'r', encoding='utf-8') as f:
        generic_attack_of_the_clones = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-complex.srt'), 'r', encoding='utf-8') as f:
        generic_complex = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-long-digit-content.srt'), 'r', encoding='utf-8') as f:
        generic_long_digit_content = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-attack_of_the_clones_raw.json'), 'r', encoding='utf-8') as f:
        generic_attack_of_the_clones_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-attack_of_the_clones.json'), 'r', encoding='utf-8') as f:
        generic_attack_of_the_clones_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-complex.json'), 'r', encoding='utf-8') as f:
        generic_complex_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-long-digit-content.json'), 'r', encoding='utf-8') as f:
        generic_long_digit_content_json = json.loads(f.read())

    def test_srt_nodata(self):
        """
        Test srt parser with no data
        """
        self.assertEqual(jc.parsers.srt.parse('', quiet=True), [])

    def test_srt_nodata_r(self):
        """
        Test srt parser with no data and raw output
        """
        self.assertEqual(jc.parsers.srt.parse('', raw=True, quiet=True), [])

    def test_srt_attack_of_the_clones_raw(self):
        """
        Test the attack of the clones srt file without post processing
        """
        self.assertEqual(jc.parsers.srt.parse(self.generic_attack_of_the_clones, raw=True, quiet=True), self.generic_attack_of_the_clones_raw_json)

    def test_srt_attack_of_the_clones(self):
        """
        Test the attack of the clones srt file
        """
        self.assertEqual(jc.parsers.srt.parse(self.generic_attack_of_the_clones, quiet=True), self.generic_attack_of_the_clones_json)

    def test_srt_complex(self):
        """
        Test a complex srt file
        """
        self.assertEqual(jc.parsers.srt.parse(self.generic_complex, quiet=True), self.generic_complex_json)

    def test_srt_long_digit_content(self):
        """
        Test an srt file with a long run of digits in the subtitle content
        """
        self.assertEqual(jc.parsers.srt.parse(self.generic_long_digit_content, quiet=True), self.generic_long_digit_content_json)

    def test_srt_long_digit_line_before_first_subtitle(self):
        """
        Test that a long run of digits before the first subtitle is skipped
        """
        data = '1' * 300 + '\n\n1\n00:00:01,000 --> 00:00:02,000\nAfter digits.\n'
        expected = [{'index': 1, 'start': {'hours': 0, 'minutes': 0, 'seconds': 1, 'milliseconds': 0, 'timestamp': '00:00:01,000'}, 'end': {'hours': 0, 'minutes': 0, 'seconds': 2, 'milliseconds': 0, 'timestamp': '00:00:02,000'}, 'content': 'After digits.'}]
        self.assertEqual(jc.parsers.srt.parse(data, quiet=True), expected)

    def test_srt_timestamp_delimiters(self):
        """
        Test srt timestamps with comma, dot, and full-width delimiters
        """
        data = '1\n00:00:01,500 --> 00:00:02.250\nComma and dot.\n\n2\n00\uff1a00\uff1a03\uff0c100 --> 00\uff1a00\uff1a04\uff0e200\nFull width.\n'
        expected = [
            {'index': '1', 'start': {'hours': '00', 'minutes': '00', 'seconds': '01', 'milliseconds': '500', 'timestamp': '00:00:01,500'}, 'end': {'hours': '00', 'minutes': '00', 'seconds': '02', 'milliseconds': '250', 'timestamp': '00:00:02.250'}, 'content': 'Comma and dot.'},
            {'index': '2', 'start': {'hours': '00', 'minutes': '00', 'seconds': '03', 'milliseconds': '100', 'timestamp': '00\uff1a00\uff1a03\uff0c100'}, 'end': {'hours': '00', 'minutes': '00', 'seconds': '04', 'milliseconds': '200', 'timestamp': '00\uff1a00\uff1a04\uff0e200'}, 'content': 'Full width.'}
        ]
        self.assertEqual(jc.parsers.srt.parse(data, raw=True, quiet=True), expected)

    def test_srt_timestamp_optional_milliseconds(self):
        """
        Test srt timestamps with a missing, empty, or undelimited milliseconds field
        """
        data = '1\n00:00:01 --> 00:00:02,\nNo milliseconds.\n\n2\n00:00:03:400 --> 00:00:04400\nColon and no delimiter.\n'
        expected = [
            {'index': 1, 'start': {'hours': 0, 'minutes': 0, 'seconds': 1, 'milliseconds': None, 'timestamp': '00:00:01'}, 'end': {'hours': 0, 'minutes': 0, 'seconds': 2, 'milliseconds': None, 'timestamp': '00:00:02,'}, 'content': 'No milliseconds.'},
            {'index': 2, 'start': {'hours': 0, 'minutes': 0, 'seconds': 3, 'milliseconds': 400, 'timestamp': '00:00:03:400'}, 'end': {'hours': 0, 'minutes': 0, 'seconds': 4400, 'milliseconds': None, 'timestamp': '00:00:04400'}, 'content': 'Colon and no delimiter.'}
        ]
        self.assertEqual(jc.parsers.srt.parse(data, quiet=True), expected)

    def test_srt_index_variants(self):
        """
        Test srt negative, float, and missing indexes after leading blank lines
        """
        data = '  \n\n-3\n00:00:01,000 --> 00:00:02,000\nNegative.\n\n2.5\n00:00:03,000 --> 00:00:04,000\nFloat.\n\n00:00:05,000 --> 00:00:06,000\nNo index.\n'
        result = jc.parsers.srt.parse(data, raw=True, quiet=True)
        self.assertEqual([x['index'] for x in result], ['-3', '2.5', None])
        self.assertEqual([x['content'] for x in result], ['Negative.', 'Float.', 'No index.'])

    def test_srt_parse_timestamp(self):
        """
        Test splitting srt timestamps into fields
        """
        self.assertEqual(jc.parsers.srt.parse_timestamp('1:2:345'), {'hours': '1', 'minutes': '2', 'seconds': '345', 'milliseconds': '', 'timestamp': '1:2:345'})
        self.assertEqual(jc.parsers.srt.parse_timestamp('1:2:3,45'), {'hours': '1', 'minutes': '2', 'seconds': '3', 'milliseconds': '45', 'timestamp': '1:2:3,45'})
        self.assertEqual(jc.parsers.srt.parse_timestamp('1:2:3:4'), {'hours': '1', 'minutes': '2', 'seconds': '3', 'milliseconds': '4', 'timestamp': '1:2:3:4'})
        self.assertEqual(jc.parsers.srt.parse_timestamp('1:2:3,'), {'hours': '1', 'minutes': '2', 'seconds': '3', 'milliseconds': '', 'timestamp': '1:2:3,'})
        self.assertEqual(jc.parsers.srt.parse_timestamp('1:2'), {})
        self.assertEqual(jc.parsers.srt.parse_timestamp('1:2:' + '3' * 50 + 'x'), {})

    def test_srt_positional_coordinates(self):
        """
        Test 'srt' with positional coordinates after the end timestamp
        """
        data = (
            '1\n00:00:01,000 --> 00:00:04,000 X1:40 X2:600 Y1:20 Y2:50\nHello\n\n'
            '2\n00:00:05,000 --> 00:00:06,000\nWorld\n\n'
        )
        result = jc.parsers.srt.parse(data, quiet=True)
        self.assertEqual([x['index'] for x in result], [1, 2])
        self.assertEqual(result[0]['proprietary'], 'X1:40 X2:600 Y1:20 Y2:50')
        self.assertEqual(result[0]['content'], 'Hello')
        self.assertEqual(result[0]['end']['timestamp'], '00:00:04,000')
        self.assertNotIn('proprietary', result[1])
        self.assertEqual(result[1]['content'], 'World')


if __name__ == '__main__':
    unittest.main()
