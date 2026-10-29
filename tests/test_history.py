import os
import json
import unittest
import jc.parsers.history

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/history.out'), 'r', encoding='utf-8') as f:
        centos_7_7_history = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/history.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_history = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/history.json'), 'r', encoding='utf-8') as f:
        centos_7_7_history_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/history.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_history_json = json.loads(f.read())


    def test_history_line_separators(self):
        """
        Test 'history' with line-break characters other than LF in a command
        """
        data = '    1  echo a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\n    2  ls\n'
        result = jc.parsers.history.parse(data, quiet=True)
        self.assertEqual(result[0]['command'], 'echo a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[1]['command'], 'ls')

    def test_history_nodata(self):
        """
        Test 'history' with no data
        """
        self.assertEqual(jc.parsers.history.parse('', quiet=True), [])

    def test_history_centos_7_7(self):
        """
        Test 'history' on Centos 7.7
        """
        self.assertEqual(jc.parsers.history.parse(self.centos_7_7_history, quiet=True), self.centos_7_7_history_json)

    def test_history_ubuntu_18_4(self):
        """
        Test 'history' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.history.parse(self.ubuntu_18_4_history, quiet=True), self.ubuntu_18_4_history_json)


if __name__ == '__main__':
    unittest.main()
