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


    def test_syslog_bsd_s_unparsable_ignore_exceptions(self):
        """
        Test 'syslog_bsd_s' with an unparsable line: an unparsable record without ignore_exceptions, an error record with it
        """
        data = ['<3444>Oct 11 22:14:15 mymachine su: failed', '<34>Oct 11 22:14:15 mymachine su: failed']
        result = list(jc.parsers.syslog_bsd_s.parse(data, quiet=True))
        self.assertEqual(result[0], {'unparsable': data[0]})
        self.assertEqual(result[1]['hostname'], 'mymachine')

        result = list(jc.parsers.syslog_bsd_s.parse(data, quiet=True, ignore_exceptions=True))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {'_jc_meta': {'success': False, 'error': 'ParseError: Not syslog data', 'line': data[0]}})
        self.assertEqual(result[1]['hostname'], 'mymachine')
        self.assertEqual(result[1]['content'], 'failed')
        self.assertEqual(result[1]['_jc_meta'], {'success': True})


if __name__ == '__main__':
    unittest.main()
