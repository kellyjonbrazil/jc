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


    LINES_AUTHUSER_SPACE = [
        '1.2.3.4 - no body [20/Oct/2026:10:00:00 +0000] "GET /a HTTP/1.1" 200 5 "-" "agent"',
        '1.2.3.4 - x [01/Jan/2000:00:00:00 +0000] \\"GET /fake HTTP/1.1\\" 404 1 [20/Oct/2026:10:00:00 +0000] "GET /b HTTP/1.1" 200 6',
        'www.example.com:80 203.0.113.9 - - [20/Oct/2026:10:00:00 +0000] "GET / HTTP/1.1" 200 1 "-" "x"',
        'Oct 20 10:00:00 host nginx: 1.2.3.4 - - [20/Oct/2026:10:00:00 +0000] "GET / HTTP/1.1" 200 1',
        '1.2.3.4 identd no body [20/Oct/2026:10:00:00 +0000] "GET /a HTTP/1.1" 200 5'
    ]

    def test_clf_authuser_space(self):
        """
        Test 'clf' with spaces in the authuser field: parsed when ident is '-', lines with extra leading columns stay unparsable
        """
        result = parse('\n'.join(self.LINES_AUTHUSER_SPACE), quiet=True)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]['host'], '1.2.3.4')
        self.assertEqual(result[0]['ident'], None)
        self.assertEqual(result[0]['authuser'], 'no body')
        self.assertEqual(result[0]['request_url'], '/a')
        self.assertEqual(result[0]['status'], 200)
        self.assertEqual(result[0]['user_agent'], 'agent')
        self.assertEqual(result[1]['authuser'], 'x [01/Jan/2000:00:00:00 +0000] \\"GET /fake HTTP/1.1\\" 404 1')
        self.assertEqual(result[1]['date'], '20/Oct/2026:10:00:00 +0000')
        self.assertEqual(result[1]['request_url'], '/b')
        self.assertEqual(result[1]['status'], 200)
        for i in (2, 3, 4):
            self.assertEqual(result[i], {'unparsable': self.LINES_AUTHUSER_SPACE[i]})


if __name__ == '__main__':
    unittest.main()
