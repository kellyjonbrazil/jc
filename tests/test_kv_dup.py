import os
import unittest
import jc.parsers.kv_dup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def test_kv_dup_nodata(self):
        """
        Test the test kv file with no data
        """
        self.assertEqual(jc.parsers.kv_dup.parse('', quiet=True), {})

    def test_kv_dup_duplicate_keys(self):
        """
        Test input that contains duplicate keys
        """
        data = '''
duplicate_key: value1
another_key = foo
duplicate_key = value2
'''
        expected = {"duplicate_key":["value1","value2"],"another_key":["foo"]}
        self.assertEqual(jc.parsers.kv_dup.parse(data, quiet=True), expected)

    def test_kv_dup_null_values(self):
        """
        Test input that contains duplicate keys and null values
        """
        data = '''
normal_key: "hello world"
no_val
some_vals = 1
some_vals
some_vals:3
'''
        expected = {"normal_key":["hello world"],"no_val":[""],"some_vals":["1","","3"]}
        self.assertEqual(jc.parsers.kv_dup.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
