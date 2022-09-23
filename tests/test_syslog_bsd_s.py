import os
import json
import unittest
import jc.parsers.syslog_bsd_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat syslog.out | jc --syslog-bsd-s | jello -c > syslog-bsd-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-3164.out'), 'r', encoding='utf-8') as f:
        syslog_bsd = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-3164-streaming.json'), 'r', encoding='utf-8') as f:
        syslog_bsd_streaming_json = json.loads(f.read())


    def test_syslog_bsd_s_nodata(self):
        """
        Test 'syslog_bsd' with no data
        """
        self.assertEqual(list(jc.parsers.syslog_bsd_s.parse([], quiet=True)), [])

    def test_syslog_bsd_s(self):
        """
        Test bsd Syslog
        """
        self.assertEqual(list(jc.parsers.syslog_bsd_s.parse(self.syslog_bsd.splitlines(), quiet=True)), self.syslog_bsd_streaming_json)


if __name__ == '__main__':
    unittest.main()
