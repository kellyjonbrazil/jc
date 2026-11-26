import os
import unittest
import json
import jc.parsers.cksum

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/cksum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_cksum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/cksum.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_cksum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/sum.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_sum = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/cksum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_cksum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/cksum.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_cksum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/sum.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_sum_json = json.loads(f.read())

    def test_cksum_line_separators(self):
        """
        Test 'cksum' with line-break characters other than LF in a file name
        """
        data = '3194693727 24150660 a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j.rpm\n1851496064 1196 digout\n'
        result = jc.parsers.cksum.parse(data, quiet=True)
        self.assertEqual(result[0]['filename'], 'a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j.rpm')
        self.assertEqual(result[1]['filename'], 'digout')

    def test_cksum_preserves_leading_filename_whitespace(self):
        """
        Test 'cksum' and 'sum' keep whitespace at the start of a file name
        """
        data = (
            '4294967295 0  quarterly.csv\n'
            '4294967295 0 \tarchive.csv\n'
            '4294967295 0 \u00a0exports.csv\n'
            '4294967295 0  \n'
            '00000     0  report.txt\n'
            '0 0  notes.txt\n'
        )
        self.assertEqual(
            jc.parsers.cksum.parse(data, quiet=True),
            [
                {'filename': ' quarterly.csv', 'checksum': 4294967295, 'blocks': 0},
                {'filename': '\tarchive.csv', 'checksum': 4294967295, 'blocks': 0},
                {'filename': '\u00a0exports.csv', 'checksum': 4294967295, 'blocks': 0},
                {'filename': ' ', 'checksum': 4294967295, 'blocks': 0},
                {'filename': ' report.txt', 'checksum': 0, 'blocks': 0},
                {'filename': ' notes.txt', 'checksum': 0, 'blocks': 0},
            ]
        )

    def test_cksum_nodata(self):
        """
        Test 'cksum' parser with no data
        """
        self.assertEqual(jc.parsers.cksum.parse('', quiet=True), [])

    def test_cksum_stdin_no_filename(self):
        """
        Test 'cksum' output from a pipe (checksum and blocks only, no filename)
        """
        self.assertEqual(
            jc.parsers.cksum.parse('1479881546 3', quiet=True),
            [{'filename': None, 'checksum': 1479881546, 'blocks': 3}]
        )

    def test_sum_stdin_no_filename(self):
        """
        Test 'sum' output from a pipe (checksum and blocks only, no filename)
        """
        self.assertEqual(
            jc.parsers.cksum.parse('32856 1', quiet=True),
            [{'filename': None, 'checksum': 32856, 'blocks': 1}]
        )

    def test_cksum_centos_7_7(self):
        """
        Test 'cksum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.cksum.parse(self.centos_7_7_cksum, quiet=True), self.centos_7_7_cksum_json)

    def test_sum_centos_7_7(self):
        """
        Test 'sum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.cksum.parse(self.centos_7_7_sum, quiet=True), self.centos_7_7_sum_json)

    def test_cksum_osx_10_14_6(self):
        """
        Test 'cksum' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.cksum.parse(self.osx_10_14_6_cksum, quiet=True), self.osx_10_14_6_cksum_json)

    def test_sum_osx_10_14_6(self):
        """
        Test 'sum' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.cksum.parse(self.osx_10_14_6_sum, quiet=True), self.osx_10_14_6_sum_json)


if __name__ == '__main__':
    unittest.main()
