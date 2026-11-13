import os
import unittest
import json
import jc.parsers.hash

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/hash.out'), 'r', encoding='utf-8') as f:
        centos_7_7_hash = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/hash.json'), 'r', encoding='utf-8') as f:
        centos_7_7_hash_json = json.loads(f.read())


    def test_hash_line_separators(self):
        """
        Test 'hash' with line-break characters other than LF in a command path
        """
        data = 'hits\tcommand\n   2\t/usr/bin/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\n   1\t/usr/bin/ls\n'
        result = jc.parsers.hash.parse(data, quiet=True)
        self.assertEqual(result[0]['command'], '/usr/bin/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[1]['command'], '/usr/bin/ls')

    def test_hash_nodata(self):
        """
        Test 'hash' parser with no data
        """
        self.assertEqual(jc.parsers.hash.parse('', quiet=True), [])

    def test_hash_centos_7_7(self):
        """
        Test 'hash' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hash.parse(self.centos_7_7_hash, quiet=True), self.centos_7_7_hash_json)


if __name__ == '__main__':
    unittest.main()
