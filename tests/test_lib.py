import unittest
from typing import Generator
import jc.lib


class MyTests(unittest.TestCase):
    def test_jc_lib_parse_csv(self):
        data = {
            '': [],
            'a,b,c\n1,2,3': [{'a':'1', 'b':'2', 'c':'3'}]
        }

        for test_data, expected_output in data.items():
            self.assertEqual(jc.lib.parse('csv', test_data), expected_output)

    def test_jc_lib_parse_csv_s_is_generator(self):
        self.assertIsInstance(jc.lib.parse('csv_s', 'a,b,c\n1,2,3'), Generator)

    def test_jc_lib_parse_kv(self):
        data = {
            '': {},
            'a=1\nb=2\nc=3': {'a':'1', 'b':'2', 'c':'3'}
        }

        for test_data, expected_output in data.items():
            self.assertEqual(jc.lib.parse('kv', test_data), expected_output)

    def test_jc_lib_parser_mod_list_is_list(self):
        self.assertIsInstance(jc.lib.parser_mod_list(), list)

    def test_jc_lib_parser_mod_list_contains_csv(self):
        self.assertTrue('csv' in jc.lib.parser_mod_list())

    def test_jc_lib_parser_mod_list_length(self):
        self.assertGreaterEqual(len(jc.lib.parser_mod_list()), 80)

    def test_jc_lib_plugin_parser_mod_list_is_list(self):
        self.assertIsInstance(jc.lib.plugin_parser_mod_list(), list)

if __name__ == '__main__':
    unittest.main()