import os
import unittest
import json
from typing import Dict
from jc.parsers.clf import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'clf': (
                'fixtures/generic/common-log-format.log',
                'fixtures/generic/common-log-format.json'),
            'clf_escaped_quotes': (
                'fixtures/generic/common-log-format-escaped-quotes.log',
                'fixtures/generic/common-log-format-escaped-quotes.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_clf_nodata(self):
        """
        Test 'clf' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_clf(self):
        """
        Test 'clf' with various log lines
        """
        self.assertEqual(
            parse(self.f_in['clf'], quiet=True),
            self.f_json['clf']
        )


    def test_clf_line_separator(self):
        """
        Test 'clf' with a line-break character other than LF inside a field
        """
        data = '1.2.3.4 - - [01/Jan/2026:00:00:00 +0000] "GET / HTTP/1.1" 200 1 "-" "ua\u20289.9.9.9 - admin [01/Jan/2026:00:00:00 +0000] "GET /admin HTTP/1.1" 200 1 "-" "x"\n'
        result = parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['host'], '1.2.3.4')
        self.assertIn('\u2028', result[0]['user_agent'])


    def test_clf_escaped_quotes(self):
        """
        Test 'clf' with backslash-escaped quotes and backslashes in quoted fields
        """
        self.assertEqual(
            parse(self.f_in['clf_escaped_quotes'], quiet=True),
            self.f_json['clf_escaped_quotes']
        )


if __name__ == '__main__':
    unittest.main()
