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


if __name__ == '__main__':
    unittest.main()
