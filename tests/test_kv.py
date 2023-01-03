import os
import unittest
import json
import jc.parsers.kv

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/keyvalue.txt'), 'r', encoding='utf-8') as f:
        generic_ini_keyvalue = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/keyvalue-ifcfg.txt'), 'r', encoding='utf-8') as f:
        generic_ini_keyvalue_ifcfg = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/keyvalue.json'), 'r', encoding='utf-8') as f:
        generic_ini_keyvalue_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/keyvalue-ifcfg.json'), 'r', encoding='utf-8') as f:
        generic_ini_keyvalue_ifcfg_json = json.loads(f.read())


    def test_kv_nodata(self):
        """
        Test the test kv file with no data
        """
        self.assertEqual(jc.parsers.kv.parse('', quiet=True), {})

    def test_kv_keyvalue(self):
        """
        Test a file that only includes key/value lines
        """
        self.assertEqual(jc.parsers.kv.parse(self.generic_ini_keyvalue, quiet=True), self.generic_ini_keyvalue_json)

    def test_kv_keyvalue_ifcfg(self):
        """
        Test a sample ifcfg key/value file that has quotation marks in the values
        """
        self.assertEqual(jc.parsers.kv.parse(self.generic_ini_keyvalue_ifcfg, quiet=True), self.generic_ini_keyvalue_ifcfg_json)

    def test_kv_duplicate_keys(self):
        """
        Test input that contains duplicate keys. Only the last value should be used.
        """
        data = '''
duplicate_key: value1
another_key = foo
duplicate_key = value2
'''
        expected = {'duplicate_key': 'value2', 'another_key': 'foo'}
        self.assertEqual(jc.parsers.kv.parse(data, quiet=True), expected)

    def test_kv_doublequote(self):
        """
        Test kv string with double quotes around a value
        """
        data = '''
key1: "value1"
key2: value2
        '''
        expected = {'key1': 'value1', 'key2': 'value2'}
        self.assertEqual(jc.parsers.kv.parse(data, quiet=True), expected)

    def test_kv_singlequote(self):
        """
        Test kv string with double quotes around a value
        """
        data = '''
key1: 'value1'
key2: value2
        '''
        expected = {'key1': 'value1', 'key2': 'value2'}
        self.assertEqual(jc.parsers.kv.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
