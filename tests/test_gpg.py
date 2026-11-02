import os
import unittest
import json
import jc.parsers.gpg

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/gpg.out'), 'r', encoding='utf-8') as f:
        gpg = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/gpg.json'), 'r', encoding='utf-8') as f:
        gpg_json = json.loads(f.read())


    def test_gpg_line_separators(self):
        """
        Test 'gpg --with-colons' with line-break characters other than LF in a user ID
        """
        data = 'pub:f:1024:17:6C7EE1B8621CC013:899817715:1055898235::m:::scESC:\nuid:f::::::::Werner a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j <wk@g10code.com>:\nuid:f::::::::Werner Koch <wk@gnupg.org>:\n'
        result = jc.parsers.gpg.parse(data, quiet=True)
        self.assertEqual(result[1]['user_id'], 'Werner a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j <wk@g10code.com>')
        self.assertEqual(result[2]['user_id'], 'Werner Koch <wk@gnupg.org>')

    def test_gpg_nodata(self):
        """
        Test 'gpg' with no data
        """
        self.assertEqual(jc.parsers.gpg.parse('', quiet=True), [])

    def test_gpg(self):
        """
        Test 'gpg --with-colons --list-keys --with-fingerprint --with-fingerprint wk@gnupg.org'
        """
        self.assertEqual(jc.parsers.gpg.parse(self.gpg, quiet=True), self.gpg_json)


if __name__ == '__main__':
    unittest.main()
