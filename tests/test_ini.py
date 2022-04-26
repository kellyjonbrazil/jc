import os
import unittest
import json
import jc.parsers.ini

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-test.ini'), 'r', encoding='utf-8') as f:
            self.generic_ini_test = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-iptelserver.ini'), 'r', encoding='utf-8') as f:
            self.generic_ini_iptelserver = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-test.json'), 'r', encoding='utf-8') as f:
            self.generic_ini_test_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-iptelserver.json'), 'r', encoding='utf-8') as f:
            self.generic_ini_iptelserver_json = json.loads(f.read())

    def test_ini_nodata(self):
        """
        Test the test ini file with no data
        """
        self.assertEqual(jc.parsers.ini.parse('', quiet=True), {})

    def test_ini_test(self):
        """
        Test the test ini file
        """
        self.assertEqual(jc.parsers.ini.parse(self.generic_ini_test, quiet=True), self.generic_ini_test_json)

    def test_ini_iptelserver(self):
        """
        Test the iptelserver ini file
        """
        self.assertEqual(jc.parsers.ini.parse(self.generic_ini_iptelserver, quiet=True), self.generic_ini_iptelserver_json)

    def test_ini_duplicate_keys(self):
        """
        Test input that contains duplicate keys. Only the last value should be used.
        """
        data = '''
duplicate_key: value1
another_key = foo
duplicate_key = value2
'''
        expected = {'duplicate_key': 'value2', 'another_key': 'foo'}
        self.assertEqual(jc.parsers.ini.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
