import contextlib
import io
import sys
from copy import deepcopy
import unittest
from typing import Generator
from types import ModuleType
import jc.lib
import jc.parsers.csv as csv_parser
import jc.parsers.disabled_parser as disabled_parser


class MyTests(unittest.TestCase):
    def test_lib_get_parser_string(self):
        p = jc.lib.get_parser('arp')
        self.assertIsInstance(p, ModuleType)

    def test_lib_get_parser_broken_parser(self):
        """get_parser substitutes the disabled_parser if a parser is broken"""
        jc.lib.parsers.append('broken-parser')
        try:
            broken = jc.lib.get_parser('broken_parser')
        finally:
            jc.lib.parsers.remove('broken-parser')
        self.assertIs(broken, disabled_parser)

    def test_lib_get_parser_unknown_name(self):
        """
        Test get_parser, parse and parser_info with a name that is not a
        registered parser: ModuleNotFoundError and no warning
        """
        disabled_name = disabled_parser.__name__
        for name in ('not_a_parser', 'not-a-parser', '--not-a-parser', '\x1b[2J', 'foo', 'foo_s', 'disabled_parser'):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertRaises(ModuleNotFoundError, jc.lib.get_parser, name)
                self.assertRaises(ModuleNotFoundError, jc.lib.parse, name, 'a=1', quiet=True)
                self.assertRaises(ModuleNotFoundError, jc.lib.parser_info, name)
            self.assertEqual(stderr.getvalue(), '')
        self.assertEqual(disabled_parser.__name__, disabled_name)

    def test_lib_get_parser_unregistered_module(self):
        """
        Test get_parser with the name of a module under jc/parsers that is
        not a parser: it is not imported
        """
        sys.modules.pop('jc.parsers.asn1crypto.pkcs12', None)
        self.assertRaises(ModuleNotFoundError, jc.lib.get_parser, 'asn1crypto.pkcs12')
        self.assertNotIn('jc.parsers.asn1crypto.pkcs12', sys.modules)

    def test_lib_get_parser_name_variants(self):
        """
        Test get_parser with module, cli and argument names of a parser
        """
        for name in ('ini_dup', 'ini-dup', '--ini-dup'):
            self.assertEqual(jc.lib.get_parser(name).__name__, 'jc.parsers.ini_dup')

    def test_lib_alias_parsers_keep_wrapped_parser_info(self):
        """
        Test parser_info and all_parser_info after each alias parser has run:
        the parsers they call are still reported as themselves
        """
        aliases = {
            'kv': 'a=1\n',
            'kv_dup': 'a=1\n',
            'os_release': 'NAME=x\n',
            'lsb_release': 'Distributor ID:\tUbuntu\n',
            'apt_cache_show': 'Package: x\nVersion: 1\n',
            'pkg_index_deb': 'Package: x\nVersion: 1\n',
            'curl_head': 'HTTP/1.1 200 OK\nX-A: b\n',
            'path_list': '/a/b:/c\n',
        }
        for name, data in aliases.items():
            jc.lib.parse(name, data, quiet=True)

        wrapped = {
            'ini': ('--ini', 'INI file parser'),
            'ini_dup': ('--ini-dup', 'INI with duplicate key file parser'),
            'rpm_qi': ('--rpm-qi', '`rpm -qi` command parser'),
            'http_headers': ('--http-headers', 'HTTP headers parser'),
            'path': ('--path', 'POSIX path string parser'),
        }
        for name, (argument, description) in wrapped.items():
            info = jc.lib.parser_info(name)
            self.assertEqual(info['name'], name)
            self.assertEqual(info['argument'], argument)
            self.assertEqual(info['description'], description)

        self.assertEqual(jc.lib.parser_info('rpm_qi')['compatible'], ['linux'])
        self.assertEqual(jc.lib.parser_info('curl_head')['magic_commands'], ['curl'])
        self.assertNotIn('magic_commands', jc.lib.parser_info('http_headers'))

        names = [p['name'] for p in jc.lib.all_parser_info(show_hidden=True, show_deprecated=True)]
        self.assertEqual(len(names), len(set(names)))
        for name in list(aliases) + list(wrapped):
            self.assertIn(name, names)

    def test_lib_get_parser_module(self):
        p = jc.lib.get_parser(csv_parser)
        self.assertIsInstance(p, ModuleType)

    def test_lib_parse_csv(self):
        data = {
            '': [],
            'a,b,c\n1,2,3': [{'a':'1', 'b':'2', 'c':'3'}]
        }

        for test_data, expected_output in data.items():
            self.assertEqual(jc.lib.parse('csv', test_data), expected_output)

    def test_lib_parse_csv_s_is_generator(self):
        self.assertIsInstance(jc.lib.parse('csv_s', 'a,b,c\n1,2,3'), Generator)

    def test_lib_parse_kv(self):
        data = {
            '': {},
            'a=1\nb=2\nc=3': {'a':'1', 'b':'2', 'c':'3'}
        }

        for test_data, expected_output in data.items():
            self.assertEqual(jc.lib.parse('kv', test_data), expected_output)

    def test_lib_parser_mod_list_is_list(self):
        self.assertIsInstance(jc.lib.parser_mod_list(), list)

    def test_lib_parser_mod_list_contains_csv(self):
        self.assertTrue('csv' in jc.lib.parser_mod_list())

    def test_lib_parser_mod_list_length(self):
        self.assertGreaterEqual(len(jc.lib.parser_mod_list()), 80)

    def test_lib_parser_info_is_dict(self):
        self.assertIsInstance(jc.lib.parser_info('csv'), dict)

    def test_lib_parser_info_csv(self):
        self.assertTrue(jc.lib.parser_info('csv')['name'] == 'csv')

    def test_lib_all_parser_info_is_list_of_dicts(self):
        self.assertIsInstance(jc.lib.all_parser_info(), list)
        self.assertIsInstance(jc.lib.all_parser_info()[0], dict)

    def test_lib_all_parser_info_contains_csv(self):
        p_list = []
        for p in jc.lib.all_parser_info():
            p_list.append(p['name'])
        self.assertTrue('csv' in p_list)

    def test_lib_all_parser_info_length(self):
        self.assertGreaterEqual(len(jc.lib.all_parser_info()), 80)

    def test_lib_all_parser_hidden_length(self):
        reg_length = len(jc.lib.all_parser_info())
        hidden_length = len(jc.lib.all_parser_info(show_hidden=True))
        self.assertGreater(hidden_length, reg_length)

    def test_lib_plugin_parser_mod_list_is_list(self):
        self.assertIsInstance(jc.lib.plugin_parser_mod_list(), list)

    def test_lib_plugin_parser_mod_list_length_is_zero(self):
        """Ensure there are no plugin parsers present during test/build."""
        self.assertEqual(len(jc.lib.plugin_parser_mod_list()), 0)

    def test_lib_cliname_to_modname(self):
        self.assertEqual(jc.lib._cliname_to_modname('module-name'), 'module_name')

    def test_lib_argumentname_to_modname(self):
        self.assertEqual(jc.lib._cliname_to_modname('--module-name'), 'module_name')

    def test_lib_modname_to_cliname(self):
        self.assertEqual(jc.lib._modname_to_cliname('module_name'), 'module-name')

    def test_lib_all_parser_info_show_deprecated(self):
        # save old state
        old_parsers = deepcopy(jc.lib.parsers)
        old_get_parser = deepcopy(jc.lib.get_parser)

        # mock data
        class mock_parser_info:
            version = "1.1"
            description = "`deprecated` command parser"
            author = "nobody"
            author_email = "nobody@gmail.com"
            compatible = ["linux", "darwin"]
            magic_commands = ["deprecated"]
            deprecated = True

        class mock_parser:
            info = mock_parser_info
            def parse():
                pass

        jc.lib.parsers = ['deprecated']
        jc.lib.get_parser = lambda x: mock_parser  # type: ignore
        result = jc.lib.all_parser_info(show_deprecated=True)

        # reset
        jc.lib.parsers = old_parsers
        jc.lib.get_parser = old_get_parser

        self.assertEqual(len(result), 1)

    def test_lib_all_parser_info_show_hidden(self):
        # save old state
        old_parsers = deepcopy(jc.lib.parsers)
        old_get_parser = deepcopy(jc.lib.get_parser)

        # mock data
        class mock_parser_info:
            version = "1.1"
            description = "`deprecated` command parser"
            author = "nobody"
            author_email = "nobody@gmail.com"
            compatible = ["linux", "darwin"]
            magic_commands = ["deprecated"]
            hidden = True

        class mock_parser:
            info = mock_parser_info
            def parse():
                pass

        jc.lib.parsers = ['deprecated']
        jc.lib.get_parser = lambda x: mock_parser  # type: ignore
        result = jc.lib.all_parser_info(show_hidden=True)

        # reset
        jc.lib.parsers = old_parsers
        jc.lib.get_parser = old_get_parser

        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()