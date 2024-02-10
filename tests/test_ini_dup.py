import os
import unittest
import json
import jc.parsers.ini_dup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-test.ini'), 'r', encoding='utf-8') as f:
        generic_ini_test = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-iptelserver.ini'), 'r', encoding='utf-8') as f:
        generic_ini_iptelserver = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-double-quote.ini'), 'r', encoding='utf-8') as f:
        generic_ini_double_quote = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-single-quote.ini'), 'r', encoding='utf-8') as f:
        generic_ini_single_quote = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-mariadb.ini'), 'r', encoding='utf-8') as f:
        generic_ini_mariadb = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-dup-test.json'), 'r', encoding='utf-8') as f:
        generic_ini_dup_test_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-dup-iptelserver.json'), 'r', encoding='utf-8') as f:
        generic_ini_dup_iptelserver_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-dup-double-quote.json'), 'r', encoding='utf-8') as f:
        generic_ini_dup_double_quote_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-dup-single-quote.json'), 'r', encoding='utf-8') as f:
        generic_ini_dup_single_quote_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-dup-mariadb.json'), 'r', encoding='utf-8') as f:
        generic_ini_dup_mariadb_json = json.loads(f.read())


    def test_ini_dup_nodata(self):
        """
        Test the test ini file with no data
        """
        self.assertEqual(jc.parsers.ini_dup.parse('', quiet=True), {})

    def test_ini_dup_test(self):
        """
        Test the test ini file
        """
        self.assertEqual(jc.parsers.ini_dup.parse(self.generic_ini_test, quiet=True), self.generic_ini_dup_test_json)

    def test_ini_dup_iptelserver(self):
        """
        Test the iptelserver ini file
        """
        self.assertEqual(jc.parsers.ini_dup.parse(self.generic_ini_iptelserver, quiet=True), self.generic_ini_dup_iptelserver_json)

    def test_ini_dup_mariadb(self):
        """
        Test the mariadb ini file
        """
        self.assertEqual(jc.parsers.ini_dup.parse(self.generic_ini_mariadb, quiet=True), self.generic_ini_dup_mariadb_json)

    def test_ini_dup_duplicate_keys(self):
        """
        Test input that contains duplicate keys.
        """
        data = '''
[section]
duplicate_key: value1
another_key = foo
duplicate_key = value2
'''
        expected = {"section":{"duplicate_key":["value1","value2"],"another_key":["foo"]}}
        self.assertEqual(jc.parsers.ini_dup.parse(data, quiet=True), expected)

    def test_ini_dup_missing_top_section(self):
        """
        Test INI file missing top-level section header.
        """
        data = '''
key: value1
another_key = foo
[section2]
key3: bar
key4 =
[section 3]
key5 = "quoted"
'''
        expected = {"key":["value1"],"another_key":["foo"],"section2":{"key3":["bar"],"key4":[""]},"section 3":{"key5":["quoted"]}}
        self.assertEqual(jc.parsers.ini_dup.parse(data, quiet=True), expected)

    def test_ini_dup_doublequote(self):
        """
        Test ini file with double quotes around a value
        """
        self.assertEqual(jc.parsers.ini_dup.parse(self.generic_ini_double_quote, quiet=True), self.generic_ini_dup_double_quote_json)

    def test_ini_dup_singlequote(self):
        """
        Test ini file with single quotes around a value
        """
        self.assertEqual(jc.parsers.ini_dup.parse(self.generic_ini_single_quote, quiet=True), self.generic_ini_dup_single_quote_json)

    def test_ini_dup_single_key_no_value(self):
        """
        Test ini file with a single item with no value.
        """
        data = '''[data]
novalue
'''
        expected = {"data":{"novalue":[""]}}
        self.assertEqual(jc.parsers.ini_dup.parse(data, quiet=True), expected)

if __name__ == '__main__':
    unittest.main()
