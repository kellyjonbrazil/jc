import os
import unittest
import json
import jc.parsers.find

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/find.out'), 'r', encoding='utf-8') as f:
        centos_7_7_find = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/find.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_find = f.read()

    #output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/find.json'), 'r', encoding='utf-8') as f:
        centos_7_7_find_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/find.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_find_json = json.loads(f.read())

    def test_find_line_separators(self):
        """
        Test 'find' with line-break characters other than LF in a file name
        """
        data = './a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\n./b\n'
        result = jc.parsers.find.parse(data, quiet=True)
        self.assertEqual(result[0]['node'], 'a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[1]['node'], 'b')

    def test_find_nodata(self):
        """
        Test 'find' with no data
        """
        self.assertEqual(jc.parsers.find.parse('', quiet=True), [])

    def test_find_centos_7_7(self):
        """
        Test 'find' on Centos 7.7
        """
        self.assertEqual(jc.parsers.find.parse(self.centos_7_7_find, quiet=True), self.centos_7_7_find_json)

    def test_find_ubuntu_18_4(self):
        """
        Test 'find' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.find.parse(self.ubuntu_18_4_find, quiet=True), self.ubuntu_18_4_find_json)
    def test_find_no_slash(self):
        """
        Test 'find' with lines that have no slash
        """
        self.assertEqual(jc.parsers.find.parse('file.txt\n.\n./\n./a/b\n/etc\n', quiet=True), [
            {'path': None, 'node': 'file.txt'},
            {'path': None, 'node': '.'},
            {'path': '.', 'node': None},
            {'path': './a', 'node': 'b'},
            {'path': None, 'node': 'etc'}
        ])


if __name__ == '__main__':
    unittest.main()