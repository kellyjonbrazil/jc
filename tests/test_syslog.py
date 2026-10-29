import os
import unittest
import json
import jc.parsers.syslog

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424.out'), 'r', encoding='utf-8') as f:
        syslog = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-long-sd.out'), 'r', encoding='utf-8') as f:
        syslog_long_sd = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424.json'), 'r', encoding='utf-8') as f:
        syslog_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-long-sd.json'), 'r', encoding='utf-8') as f:
        syslog_long_sd_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-escaped-backslash.out'), 'r', encoding='utf-8') as f:
        syslog_5424_escaped_backslash = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-5424-escaped-backslash.json'), 'r', encoding='utf-8') as f:
        syslog_5424_escaped_backslash_json = json.loads(f.read())

    def test_syslog_nodata(self):
        """
        Test 'syslog' with no data
        """
        self.assertEqual(jc.parsers.syslog.parse('', quiet=True), [])

    def test_syslog_sample(self):
        """
        Test 'syslog' with sample data
        """
        self.assertEqual(jc.parsers.syslog.parse(self.syslog, quiet=True), self.syslog_json)


    def test_syslog_line_separator(self):
        """
        Test 'syslog' with a line-break character other than LF inside a field
        """
        data = '<13>1 2026-01-01T00:00:00Z web01 webapp - - - login failed for user bob\u2028<86>1 2026-01-01T00:00:00Z dc01 sshd 4242 - - Accepted password for root from 10.0.0.5\n'
        result = jc.parsers.syslog.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['message'], 'login failed for user bob\u2028<86>1 2026-01-01T00:00:00Z dc01 sshd 4242 - - Accepted password for root from 10.0.0.5')

    def test_syslog_5424_long_sd(self):
        """
        Test syslog with a long word in structured data
        """
        self.assertEqual(jc.parsers.syslog.parse(self.syslog_long_sd, quiet=True), self.syslog_long_sd_json)

    def test_syslog_5424_escaped_backslash(self):
        """
        Test syslog 5424 lines with escaped backslashes before escapable characters
        """
        self.assertEqual(jc.parsers.syslog.parse(self.syslog_5424_escaped_backslash, quiet=True), self.syslog_5424_escaped_backslash_json)

    def test_syslog_5424_escaped_quote_in_param_value(self):
        """
        Test 'syslog' with escaped quotes, backslashes and brackets in structured data parameter values
        """
        data = '<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 [exampleSDID@32473 iut="3" eventSource="App \\"lication\\"" path="C:\\\\dir\\\\" note="a\\]b" eventID="1011"] message'
        result = jc.parsers.syslog.parse(data, quiet=True)[0]
        self.assertEqual(result['structured_data'], [{
            'identity': 'exampleSDID@32473',
            'parameters': {'iut': '3', 'eventSource': 'App "lication"', 'path': 'C:\\dir\\', 'note': 'a]b', 'eventID': '1011'}
        }])
        self.assertEqual(result['message'], 'message')


if __name__ == '__main__':
    unittest.main()
