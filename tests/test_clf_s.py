import os
import json
import unittest
from typing import Dict
from jc.parsers.clf_s import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat clf.out | jc --clf-s | jello -c > clf-streaming.json


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'clf_s': (
                'fixtures/generic/common-log-format.log',
                'fixtures/generic/common-log-format-streaming.json'),
            'clf_s_escaped_quotes': (
                'fixtures/generic/common-log-format-escaped-quotes.log',
                'fixtures/generic/common-log-format-escaped-quotes-streaming.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_clf_s_nodata(self):
        """
        Test 'clf-s' with no data
        """
        self.assertEqual(list(parse([], quiet=True)), [])


    def test_clf_s_centos_7_7(self):
        """
        Test 'clf-s' with various logs
        """
        self.assertEqual(
            list(parse(self.f_in['clf_s'].splitlines(), quiet=True)),
            self.f_json['clf_s']
        )


    def test_clf_s_crlf_lines(self):
        """
        Test 'clf-s' with CRLF line endings, split on LF or with line endings kept
        """
        crlf_data = self.f_in['clf_s'].replace('\n', '\r\n')
        self.assertEqual(
            list(parse(crlf_data.split('\n'), quiet=True)),
            self.f_json['clf_s']
        )
        self.assertEqual(
            list(parse(crlf_data.splitlines(keepends=True), quiet=True)),
            self.f_json['clf_s']
        )


    def test_clf_s_escaped_quotes(self):
        """
        Test 'clf-s' with backslash-escaped quotes and backslashes in quoted fields
        """
        self.assertEqual(
            list(parse(self.f_in['clf_s_escaped_quotes'].splitlines(), quiet=True)),
            self.f_json['clf_s_escaped_quotes']
        )


    def test_clf_s_unparsable_ignore_exceptions(self):
        """
        Test 'clf_s' with an unparsable line: an unparsable record without ignore_exceptions, an error record with it
        """
        data = ['not a log line', '1.2.3.4 - - [20/Oct/2026:10:00:00 +0000] "GET /a HTTP/1.1" 200 5']
        result = list(parse(data, quiet=True))
        self.assertEqual(result[0], {'unparsable': data[0]})
        self.assertEqual(result[1]['host'], '1.2.3.4')

        result = list(parse(data, quiet=True, ignore_exceptions=True))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {'_jc_meta': {'success': False, 'error': 'ParseError: Not Common Log Format data', 'line': data[0]}})
        self.assertEqual(result[1]['host'], '1.2.3.4')
        self.assertEqual(result[1]['request_url'], '/a')
        self.assertEqual(result[1]['_jc_meta'], {'success': True})


if __name__ == '__main__':
    unittest.main()
