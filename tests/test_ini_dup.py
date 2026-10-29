import os
import unittest
import json
from jc.exceptions import ParseError
import jc.parsers.ini_dup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # new input/output fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-many-keys.ini'), 'r', encoding='utf-8') as f:
        generic_ini_many_keys = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-dup-many-keys.json'), 'r', encoding='utf-8') as f:
        generic_ini_dup_many_keys_json = json.loads(f.read())


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

    def test_ini_dup_many_keys(self):
        """
        Test 'ini_dup' with many sections and keys, including keys with no value
        """
        self.assertEqual(jc.parsers.ini_dup.parse(self.generic_ini_many_keys, quiet=True), self.generic_ini_dup_many_keys_json)

    def test_ini_dup_empty_key(self):
        """
        Test 'ini_dup' with a line that has a delimiter but no key (raises ParseError)
        """
        for data in ('[a]\nx=1\n=oops\n y\n: z\n', 'x=1\n=oops\n', '[a]\n  = oops\n'):
            with self.subTest(data):
                with self.assertRaises(ParseError):
                    jc.parsers.ini_dup.parse(data, quiet=True)

    def test_ini_dup_many_empty_keys(self):
        """
        Test 'ini_dup' with many lines that have a delimiter but no key (raises ParseError)
        """
        data = '[a]\nx=1\n' + '=oops\n' * 20000
        with self.assertRaises(ParseError):
            jc.parsers.ini_dup.parse(data, quiet=True)


    def test_ini_dup_utf8_bom(self):
        """
        Test 'ini-test.ini' and a file without sections with a leading UTF-8 BOM
        """
        self.assertEqual(jc.parsers.ini_dup.parse('\ufeff' + self.generic_ini_test, quiet=True), self.generic_ini_dup_test_json)
        self.assertEqual(jc.parsers.ini_dup.parse('\ufeffNAME="Debian"\nID=debian\n', quiet=True), {'NAME': ['Debian'], 'ID': ['debian']})


    def test_ini_dup_comment_in_multiline_value(self):
        """
        Test 'ini_dup' with full-line comments inside multi-line values: the value continues after the comment, as in 'ini'
        """
        data = (
            '[testenv]\n'
            'deps =\n'
            '    pytest\n'
            '    # pinned\n'
            '    requests==2.31.0\n'
            '    ; other\n'
            '    six\n'
            '\n'
            '[user1]\n'
            'role = guest\n'
            'bio = first line\n'
            '\t#\n'
            '\t[user2]\n'
            '\trole = admin\n'
            '\n'
            '[user2]\n'
            'role = user\n'
        )
        expected = {
            'testenv': {'deps': ['', 'pytest', 'requests==2.31.0', 'six']},
            'user1': {'role': ['guest'], 'bio': ['first line', '[user2]', 'role = admin']},
            'user2': {'role': ['user']}
        }
        self.assertEqual(jc.parsers.ini_dup.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
