import os
import json
import unittest
import jc.parsers.syslog_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat syslog.out | jc --syslog-s | jello -c > syslog-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424.out'), 'r', encoding='utf-8') as f:
        syslog = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-long-sd.out'), 'r', encoding='utf-8') as f:
        syslog_long_sd = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-streaming.json'), 'r', encoding='utf-8') as f:
        syslog_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-long-sd-streaming.json'), 'r', encoding='utf-8') as f:
        syslog_long_sd_streaming_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-escaped-backslash.out'), 'r', encoding='utf-8') as f:
        syslog_5424_escaped_backslash = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-escaped-backslash-streaming.json'), 'r', encoding='utf-8') as f:
        syslog_5424_escaped_backslash_streaming_json = json.loads(f.read())

    def test_syslog_s_nodata(self):
        """
        Test 'syslog' with no data
        """
        self.assertEqual(list(jc.parsers.syslog_s.parse([], quiet=True)), [])

    def test_syslog_s(self):
        """
        Test syslog file
        """
        self.assertEqual(list(jc.parsers.syslog_s.parse(self.syslog.splitlines(), quiet=True)), self.syslog_streaming_json)

    def test_syslog_s_5424_escaped_quote_in_param_value(self):
        """
        Test 'syslog_s' with escaped quotes, backslashes and brackets in structured data parameter values
        """
        data = '<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 [exampleSDID@32473 iut="3" eventSource="App \\"lication\\"" path="C:\\\\dir\\\\" note="a\\]b" eventID="1011"] message'
        result = list(jc.parsers.syslog_s.parse([data], quiet=True))[0]
        self.assertEqual(result['structured_data'], [{
            'identity': 'exampleSDID@32473',
            'parameters': {'iut': '3', 'eventSource': 'App "lication"', 'path': 'C:\\dir\\', 'note': 'a]b', 'eventID': '1011'}
        }])
        self.assertEqual(result['message'], 'message')

    def test_syslog_s_5424_long_sd(self):
        """
        Test syslog_s with a long word in structured data
        """
        self.assertEqual(list(jc.parsers.syslog_s.parse(self.syslog_long_sd.splitlines(), quiet=True)), self.syslog_long_sd_streaming_json)

    def test_syslog_s_5424_escaped_backslash(self):
        """
        Test syslog 5424 lines with escaped backslashes before escapable characters
        """
        self.assertEqual(list(jc.parsers.syslog_s.parse(self.syslog_5424_escaped_backslash.splitlines(), quiet=True)), self.syslog_5424_escaped_backslash_streaming_json)


    def test_syslog_s_unparsable_ignore_exceptions(self):
        """
        Test 'syslog_s' with an unparsable line: an unparsable record without ignore_exceptions, an error record with it
        """
        data = ['not a syslog line', '<34>1 2003-10-11T22:14:15.003Z mymachine su - ID47 - message']
        result = list(jc.parsers.syslog_s.parse(data, quiet=True))
        self.assertEqual(result[0], {'unparsable': data[0]})
        self.assertEqual(result[1]['hostname'], 'mymachine')

        result = list(jc.parsers.syslog_s.parse(data, quiet=True, ignore_exceptions=True))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {'_jc_meta': {'success': False, 'error': 'ParseError: Not syslog data', 'line': data[0]}})
        self.assertEqual(result[1]['hostname'], 'mymachine')
        self.assertEqual(result[1]['message'], 'message')
        self.assertEqual(result[1]['_jc_meta'], {'success': True})


if __name__ == '__main__':
    unittest.main()
