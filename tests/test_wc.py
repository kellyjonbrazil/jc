import os
import unittest
import json
import jc.parsers.wc

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/wc.out'), 'r', encoding='utf-8') as f:
        centos_7_7_wc = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/wc.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_wc = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/wc-stdin.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_wc_stdin = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/wc-line-separator.out'), 'r', encoding='utf-8') as f:
        generic_wc_line_separator = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/wc.json'), 'r', encoding='utf-8') as f:
        centos_7_7_wc_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/wc.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_wc_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/wc-stdin.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_wc_stdin_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/wc-line-separator.json'), 'r', encoding='utf-8') as f:
        generic_wc_line_separator_json = json.loads(f.read())


    def test_wc_nodata(self):
        """
        Test 'wc' parser with no data
        """
        self.assertEqual(jc.parsers.wc.parse('', quiet=True), [])

    def test_wc_centos_7_7(self):
        """
        Test 'wc' on Centos 7.7
        """
        self.assertEqual(jc.parsers.wc.parse(self.centos_7_7_wc, quiet=True), self.centos_7_7_wc_json)

    def test_wc_osx_10_14_6(self):
        """
        Test 'wc' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.wc.parse(self.osx_10_14_6_wc, quiet=True), self.osx_10_14_6_wc_json)

    def test_wc_stdin_osx_10_14_6(self):
        """
        Test 'wc' from `STDIN` on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.wc.parse(self.osx_10_14_6_wc_stdin, quiet=True), self.osx_10_14_6_wc_stdin_json)

    def test_wc_line_separator(self):
        """
        Test 'wc' with a filename containing U+2028 (LINE SEPARATOR):
        the line must stay a single record
        """
        self.assertEqual(jc.parsers.wc.parse(self.generic_wc_line_separator, quiet=True), self.generic_wc_line_separator_json)

    def test_wc_preserves_leading_filename_whitespace(self):
        """Test 'wc' preserves leading filename whitespace"""
        data = (
            ' 1  2  4   quarterly.csv\n'
            ' 1  2  4 \tarchive.csv\n'
            ' 1  2  4 \u00a0exports.csv\n'
            ' 1  2  4  \n'
            ' 4  8 16 total\n'
        )
        self.assertEqual(
            jc.parsers.wc.parse(data, quiet=True),
            [
                {'filename': '  quarterly.csv', 'lines': 1, 'words': 2, 'characters': 4},
                {'filename': '\tarchive.csv', 'lines': 1, 'words': 2, 'characters': 4},
                {'filename': '\u00a0exports.csv', 'lines': 1, 'words': 2, 'characters': 4},
                {'filename': ' ', 'lines': 1, 'words': 2, 'characters': 4},
                {'filename': 'total', 'lines': 4, 'words': 8, 'characters': 16},
            ],
        )


if __name__ == '__main__':
    unittest.main()
