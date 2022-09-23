import os
import unittest
import json
import jc.parsers.syslog_bsd

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-3164.out'), 'r', encoding='utf-8') as f:
        syslog = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/syslog-3164.json'), 'r', encoding='utf-8') as f:
        syslog_json = json.loads(f.read())


    def test_syslog_bsd_nodata(self):
        """
        Test 'syslog_bsd' with no data
        """
        self.assertEqual(jc.parsers.syslog_bsd.parse('', quiet=True), [])

    def test_syslog_bsd_sample(self):
        """
        Test 'syslog_bsd' with sample data
        """
        self.assertEqual(jc.parsers.syslog_bsd.parse(self.syslog, quiet=True), self.syslog_json)


if __name__ == '__main__':
    unittest.main()
