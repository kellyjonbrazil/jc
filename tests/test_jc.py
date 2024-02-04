import unittest
from typing import Generator
import jc


class MyTests(unittest.TestCase):
    def test_jc_parse_csv(self):
        data = {
            '': [],
            'a,b,c\n1,2,3': [{'a':'1', 'b':'2', 'c':'3'}]
        }

        for test_data, expected_output in data.items():
            self.assertEqual(jc.parse('csv', test_data), expected_output)

    def test_jc_parse_csv_s_is_generator(self):
        self.assertIsInstance(jc.parse('csv_s', 'a,b,c\n1,2,3'), Generator)

    def test_jc_parse_kv(self):
        data = {
            '': {},
            'a=1\nb=2\nc=3': {'a':'1', 'b':'2', 'c':'3'}
        }

        for test_data, expected_output in data.items():
            self.assertEqual(jc.parse('kv', test_data), expected_output)

    def test_jc_parser_mod_list_is_list(self):
        self.assertIsInstance(jc.parser_mod_list(), list)

    def test_jc_parser_mod_list_contains_csv(self):
        self.assertTrue('csv' in jc.parser_mod_list())

    def test_jc_parser_mod_list_length(self):
        self.assertGreaterEqual(len(jc.parser_mod_list()), 80)

    def test_jc_plugin_parser_mod_list_is_list(self):
        self.assertIsInstance(jc.plugin_parser_mod_list(), list)

    def test_jc_slurpable_parser_mod_list_is_list(self):
        self.assertIsInstance(jc.slurpable_parser_mod_list(), list)

if __name__ == '__main__':
    unittest.main()