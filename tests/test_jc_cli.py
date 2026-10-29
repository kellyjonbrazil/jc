import contextlib
import io
import json
import os
import sys
import tempfile
import types
import unittest
from unittest import mock
from datetime import datetime, timezone

try:
    import pygments
    from pygments.token import (Name, Number, String, Keyword)
    PYGMENTS_INSTALLED=True
except ImportError:
    PYGMENTS_INSTALLED=False

try:
    import ruamel.yaml
    RUAMELYAML_INSTALLED = True
except ImportError:
    RUAMELYAML_INSTALLED = False

from jc.cli import JcCli
from jc.exceptions import ParseError
import jc.utils
import jc.parsers.url as url_parser
import jc.parsers.proc as proc_parser
import jc.parsers.ls_s as ls_s_parser


class MyTests(unittest.TestCase):
    def test_cli_magic_parser(self):
        """
        Test that magic syntax command lines map to the right parser, options and command
        """
        commands = {
            'jc -p systemctl list-sockets': ('--systemctl-ls', ['p'], ['systemctl', 'list-sockets']),
            'jc -p systemctl list-unit-files': ('--systemctl-luf', ['p'], ['systemctl', 'list-unit-files']),
            'jc -p pip list': ('--pip-list', ['p'], ['pip', 'list']),
            'jc -p pip3 list': ('--pip-list', ['p'], ['pip3', 'list']),
            'jc -p pip show jc': ('--pip-show', ['p'], ['pip', 'show', 'jc']),
            'jc -p pip3 show jc': ('--pip-show', ['p'], ['pip3', 'show', 'jc']),
            'jc -prd last': ('--last', ['p', 'r', 'd'], ['last']),
            'jc -prdd lastb': ('--last', ['p', 'r', 'd', 'd'], ['lastb']),
            'jc -p airport -I': ('--airport', ['p'], ['airport', '-I']),
            'jc -p -r airport -I': ('--airport', ['p', 'r'], ['airport', '-I']),
            'jc -prd airport -I': ('--airport', ['p', 'r', 'd'], ['airport', '-I']),
            'jc -p nonexistent command': (None, ['p'], ['nonexistent', 'command']),
            'jc -ap': (None, [], None),
            'jc -a arp -a': ('--arp', ['a'], ['arp', '-a']),
            'jc -v': (None, [], None),
            'jc -h': (None, [], None),
            'jc -h --arp': (None, [], None),
            'jc -h arp': ('--arp', ['h'], ['arp']),
            'jc -h arp -a': ('--arp', ['h'], ['arp', '-a']),
            'jc -v arp -a': ('--arp', ['v'], ['arp', '-a']),
            'jc --pretty dig': ('--dig', ['p'], ['dig']),
            'jc --pretty --monochrome --quiet --raw dig': ('--dig', ['p', 'm', 'q', 'r'], ['dig']),
            'jc --about --yaml-out': (None, [], None)
        }

        for command, expected in commands.items():
            cli = JcCli()
            cli.args = command.split()
            cli.magic_parser()
            resulting_attributes = (cli.magic_found_parser, cli.magic_options, cli.magic_run_command)
            self.assertEqual(expected, resulting_attributes)

    @unittest.skipIf(not PYGMENTS_INSTALLED, 'pygments library not installed')
    def test_cli_set_env_colors(self):
        """
        Test custom colors from the JC_COLORS environment variable, including invalid values that fall back to the defaults
        """
        if pygments.__version__.startswith('2.3.'):
            env = {
                '': {
                    Name.Tag: 'bold #ansidarkblue',
                    Keyword: '#ansidarkgray',
                    Number: '#ansipurple',
                    String: '#ansidarkgreen'
                },
                ' ': {
                    Name.Tag: 'bold #ansidarkblue',
                    Keyword: '#ansidarkgray',
                    Number: '#ansipurple',
                    String: '#ansidarkgreen'
                },
                'default,default,default,default': {
                    Name.Tag: 'bold #ansidarkblue',
                    Keyword: '#ansidarkgray',
                    Number: '#ansipurple',
                    String: '#ansidarkgreen'
                },
                'red,red,red,red': {
                    Name.Tag: 'bold #ansidarkred',
                    Keyword: '#ansidarkred',
                    Number: '#ansidarkred',
                    String: '#ansidarkred'
                },
                'red,red,yada,red': {
                    Name.Tag: 'bold #ansidarkblue',
                    Keyword: '#ansidarkgray',
                    Number: '#ansipurple',
                    String: '#ansidarkgreen'
                },
                'red,red,red': {
                    Name.Tag: 'bold #ansidarkblue',
                    Keyword: '#ansidarkgray',
                    Number: '#ansipurple',
                    String: '#ansidarkgreen'
                },
                'red,red,red,red,red,red': {
                    Name.Tag: 'bold #ansidarkblue',
                    Keyword: '#ansidarkgray',
                    Number: '#ansipurple',
                    String: '#ansidarkgreen'
                }
            }
        else:
            env = {
                '': {
                    Name.Tag: 'bold ansiblue',
                    Keyword: 'ansibrightblack',
                    Number: 'ansimagenta',
                    String: 'ansigreen'
                },
                ' ': {
                    Name.Tag: 'bold ansiblue',
                    Keyword: 'ansibrightblack',
                    Number: 'ansimagenta',
                    String: 'ansigreen'
                },
                'default,default,default,default': {
                    Name.Tag: 'bold ansiblue',
                    Keyword: 'ansibrightblack',
                    Number: 'ansimagenta',
                    String: 'ansigreen'
                },
                'red,red,red,red': {
                    Name.Tag: 'bold ansired',
                    Keyword: 'ansired',
                    Number: 'ansired',
                    String: 'ansired'
                },
                'red,red,yada,red': {
                    Name.Tag: 'bold ansiblue',
                    Keyword: 'ansibrightblack',
                    Number: 'ansimagenta',
                    String: 'ansigreen'
                },
                'red,red,red': {
                    Name.Tag: 'bold ansiblue',
                    Keyword: 'ansibrightblack',
                    Number: 'ansimagenta',
                    String: 'ansigreen'
                },
                'red,red,red,red,red,red': {
                    Name.Tag: 'bold ansiblue',
                    Keyword: 'ansibrightblack',
                    Number: 'ansimagenta',
                    String: 'ansigreen'
                }
            }

        for jc_colors, expected_colors in env.items():
            cli = JcCli()
            os.environ["JC_COLORS"] = jc_colors
            cli.set_custom_colors()
            self.assertEqual(cli.custom_colors, expected_colors)

    @unittest.skipIf(not PYGMENTS_INSTALLED, 'pygments library not installed')
    def test_cli_json_out(self):
        """
        Test JSON output with color
        """
        test_input = [
            None,
            {},
            [],
            '',
            {"key1": "value1", "key2": 2, "key3": None, "key4": 3.14, "key5": True},
        ]

        if pygments.__version__.startswith('2.3.'):
            expected_output = [
                '\x1b[30;01mnull\x1b[39;00m',
                '{}',
                '[]',
                '\x1b[32m""\x1b[39m',
                '{\x1b[34;01m"key1"\x1b[39;00m:\x1b[32m"value1"\x1b[39m,\x1b[34;01m"key2"\x1b[39;00m:\x1b[35m2\x1b[39m,\x1b[34;01m"key3"\x1b[39;00m:\x1b[30;01mnull\x1b[39;00m,\x1b[34;01m"key4"\x1b[39;00m:\x1b[35m3.14\x1b[39m,\x1b[34;01m"key5"\x1b[39;00m:\x1b[30;01mtrue\x1b[39;00m}'
            ]
        else:
            expected_output = [
                '\x1b[90mnull\x1b[39m',
                '{}',
                '[]',
                '\x1b[32m""\x1b[39m',
                '{\x1b[34;01m"key1"\x1b[39;00m:\x1b[32m"value1"\x1b[39m,\x1b[34;01m"key2"\x1b[39;00m:\x1b[35m2\x1b[39m,\x1b[34;01m"key3"\x1b[39;00m:\x1b[90mnull\x1b[39m,\x1b[34;01m"key4"\x1b[39;00m:\x1b[35m3.14\x1b[39m,\x1b[34;01m"key5"\x1b[39;00m:\x1b[90mtrue\x1b[39m}'
            ]

        for test_dict, expected_json in zip(test_input, expected_output):
            cli = JcCli()
            os.environ["JC_COLORS"] = "default,default,default,default"
            cli.set_custom_colors()
            cli.data_out = test_dict
            self.assertEqual(cli.json_out(), expected_json)

    @unittest.skipIf(not PYGMENTS_INSTALLED, 'pygments library not installed')
    def test_cli_json_out_mono(self):
        """
        Test JSON output without color
        """
        test_input = [
            None,
            {},
            [],
            '',
            {"key1": "value1", "key2": 2, "key3": None, "key4": 3.14, "key5": True},
        ]

        expected_output = [
            'null',
            '{}',
            '[]',
            '""',
            '{"key1":"value1","key2":2,"key3":null,"key4":3.14,"key5":true}'
        ]

        for test_dict, expected_json in zip(test_input, expected_output):
            cli = JcCli()
            cli.set_custom_colors()
            cli.mono = True
            cli.data_out = test_dict
            self.assertEqual(cli.json_out(), expected_json)

    def test_cli_json_out_non_finite(self):
        """
        Test JSON output with inf and nan floats nested in lists, dictionaries
        and tuples, and as dictionary keys: they are written as null
        """
        inf = float('inf')
        nan = float('nan')
        test_input = [
            inf,
            [1.5, -inf, {'a': nan, 'b': [nan, (inf, 2)]}],
            {'x': {'y': [inf]}, nan: 1, inf: 2, 'z': 'inf'},
        ]
        expected_output = [
            'null',
            '[1.5,null,{"a":null,"b":[null,[null,2]]}]',
            '{"x":{"y":[null]},"NaN":1,"Infinity":2,"z":"inf"}',
        ]

        for test_data, expected_json in zip(test_input, expected_output):
            cli = JcCli()
            cli.set_custom_colors()
            cli.mono = True
            cli.data_out = test_data
            self.assertEqual(cli.json_out(), expected_json)

        cli = JcCli()
        cli.set_custom_colors()
        cli.mono = True
        cli.pretty = True
        cli.data_out = {'a': [inf]}
        self.assertEqual(cli.json_out(), '{\n  "a": [\n    null\n  ]\n}')

    def test_cli_json_out_finite_unchanged(self):
        """
        Test JSON output without inf or nan is the same as plain json.dumps()
        and the data is not changed
        """
        test_data = [
            {'a': 1.5, 'b': [1e308, -0.0, 2], 'c': {'d': None, 'e': 'caf\xe9'}, 'f': True},
            [[[[1]]], (1, 2), {'g': 3.14}],
        ]
        for data in test_data:
            expected = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            original = repr(data)
            cli = JcCli()
            cli.set_custom_colors()
            cli.mono = True
            cli.data_out = data
            self.assertEqual(cli.json_out(), expected)
            self.assertIs(cli.data_out, data)
            self.assertEqual(repr(data), original)

    def test_cli_non_finite_standard_and_streaming_output(self):
        """
        Test standard and streaming parser output with inf and nan: each JSON
        document or line has null in their place
        """
        inf = float('inf')
        nan = float('nan')
        parser = types.ModuleType('fake_parser')

        def parse(data, raw=False, quiet=False, ignore_exceptions=False):
            return [{'a': inf, 'b': [nan, 1.5]}, {'c': {'d': -inf}}]

        def parse_s(data, raw=False, quiet=False, ignore_exceptions=False):
            for line in data:
                yield {'line': line.rstrip('\n'), 'v': [inf, {'w': nan}]}

        parser.parse = parse
        cli = JcCli()
        cli.parser_module = parser
        cli.mono = True
        f = io.StringIO()
        stdin = io.TextIOWrapper(io.BytesIO(b'x\n'), encoding='utf-8')
        with mock.patch('sys.stdin', stdin), contextlib.redirect_stdout(f):
            cli.standard_parse_and_print()
        self.assertEqual(f.getvalue(), '[{"a":null,"b":[null,1.5]},{"c":{"d":null}}]\n')

        parser.parse = parse_s
        cli = JcCli()
        cli.parser_module = parser
        cli.mono = True
        f = io.StringIO()
        stdin = io.TextIOWrapper(io.BytesIO(b'x\ny\n'), encoding='utf-8')
        with mock.patch('sys.stdin', stdin), contextlib.redirect_stdout(f):
            cli.streaming_parse_and_print()
        self.assertEqual(f.getvalue(), '{"line":"x","v":[null,{"w":null}]}\n{"line":"y","v":[null,{"w":null}]}\n')

    @unittest.skipIf(not PYGMENTS_INSTALLED, 'pygments library not installed')
    def test_cli_json_out_pretty(self):
        """
        Test pretty-printed JSON output with color
        """
        test_input = [
            {"key1": "value1", "key2": 2, "key3": None, "key4": 3.14, "key5": True},
            {"key1": [{"subkey1": "subvalue1"}, {"subkey2": [1, 2, 3]}], "key2": True}
        ]

        if pygments.__version__.startswith('2.3.'):
            expected_output = [
                '{\n  \x1b[34;01m"key1"\x1b[39;00m: \x1b[32m"value1"\x1b[39m,\n  \x1b[34;01m"key2"\x1b[39;00m: \x1b[35m2\x1b[39m,\n  \x1b[34;01m"key3"\x1b[39;00m: \x1b[30;01mnull\x1b[39;00m,\n  \x1b[34;01m"key4"\x1b[39;00m: \x1b[35m3.14\x1b[39m,\n  \x1b[34;01m"key5"\x1b[39;00m: \x1b[30;01mtrue\x1b[39;00m\n}',
                '{\n  \x1b[34;01m"key1"\x1b[39;00m: [\n    {\n      \x1b[34;01m"subkey1"\x1b[39;00m: \x1b[32m"subvalue1"\x1b[39m\n    },\n    {\n      \x1b[34;01m"subkey2"\x1b[39;00m: [\n        \x1b[35m1\x1b[39m,\n        \x1b[35m2\x1b[39m,\n        \x1b[35m3\x1b[39m\n      ]\n    }\n  ],\n  \x1b[34;01m"key2"\x1b[39;00m: \x1b[30;01mtrue\x1b[39;00m\n}'
            ]
        else:
            expected_output = [
                '{\n  \x1b[34;01m"key1"\x1b[39;00m: \x1b[32m"value1"\x1b[39m,\n  \x1b[34;01m"key2"\x1b[39;00m: \x1b[35m2\x1b[39m,\n  \x1b[34;01m"key3"\x1b[39;00m: \x1b[90mnull\x1b[39m,\n  \x1b[34;01m"key4"\x1b[39;00m: \x1b[35m3.14\x1b[39m,\n  \x1b[34;01m"key5"\x1b[39;00m: \x1b[90mtrue\x1b[39m\n}',
                '{\n  \x1b[34;01m"key1"\x1b[39;00m: [\n    {\n      \x1b[34;01m"subkey1"\x1b[39;00m: \x1b[32m"subvalue1"\x1b[39m\n    },\n    {\n      \x1b[34;01m"subkey2"\x1b[39;00m: [\n        \x1b[35m1\x1b[39m,\n        \x1b[35m2\x1b[39m,\n        \x1b[35m3\x1b[39m\n      ]\n    }\n  ],\n  \x1b[34;01m"key2"\x1b[39;00m: \x1b[90mtrue\x1b[39m\n}'
            ]

        for test_dict, expected_json in zip(test_input, expected_output):
            cli = JcCli()
            cli.pretty = True
            cli.set_custom_colors()
            cli.data_out = test_dict
            self.assertEqual(cli.json_out(), expected_json)

    @unittest.skipIf(PYGMENTS_INSTALLED, 'pygments library installed')
    def test_cli_json_out_pretty_no_pygments(self):
        """
        Test pretty-printed JSON output when pygments is not installed
        """
        test_input = [
            {"key1": "value1", "key2": 2, "key3": None, "key4": 3.14, "key5": True},
            {"key1": [{"subkey1": "subvalue1"}, {"subkey2": [1, 2, 3]}], "key2": True}
        ]

        expected_output = [
            '{\n  "key1": "value1",\n  "key2": 2,\n  "key3": null,\n  "key4": 3.14,\n  "key5": true\n}',
            '{\n  "key1": [\n    {\n      "subkey1": "subvalue1"\n    },\n    {\n      "subkey2": [\n        1,\n        2,\n        3\n      ]\n    }\n  ],\n  "key2": true\n}'
        ]

        for test_dict, expected_json in zip(test_input, expected_output):
            cli = JcCli()
            cli.pretty = True
            cli.set_custom_colors()
            cli.data_out = test_dict
            self.assertEqual(cli.json_out(), expected_json)

    @unittest.skipIf(not PYGMENTS_INSTALLED, 'pygments library not installed')
    def test_cli_yaml_out(self):
        """
        Test YAML output with color
        """
        test_input = [
            None,
            {},
            [],
            '',
            {"key1": "value1", "key2": 2, "key3": None, "key4": 3.14, "key5": True},
        ]

        if pygments.__version__.startswith('2.3.'):
            expected_output = [
                '---\n...',
                '--- {}',
                '--- []',
                "--- \x1b[32m'\x1b[39m\x1b[32m'\x1b[39m",
                '---\nkey1: value1\nkey2: 2\nkey3:\nkey4: 3.14\nkey5: true'
            ]
        else:
            expected_output = [
                '---\n...',
                '--- {}',
                '--- []',
                "--- \x1b[32m'\x1b[39m\x1b[32m'\x1b[39m",
                '---\n\x1b[34;01mkey1\x1b[39;00m: value1\n\x1b[34;01mkey2\x1b[39;00m: 2\n\x1b[34;01mkey3\x1b[39;00m:\n\x1b[34;01mkey4\x1b[39;00m: 3.14\n\x1b[34;01mkey5\x1b[39;00m: true'
            ]

        for test_dict, expected_json in zip(test_input, expected_output):
            cli = JcCli()
            os.environ["JC_COLORS"] = "default,default,default,default"
            cli.set_custom_colors()
            cli.data_out = test_dict
            self.assertEqual(cli.yaml_out(), expected_json)

    @unittest.skipIf(not RUAMELYAML_INSTALLED, 'ruamel.yaml library not installed')
    def test_cli_yaml_out_mono(self):
        """
        Test YAML output without color
        """
        test_input = [
            None,
            {},
            [],
            '',
            {'ipv6': 'fe80::5a37:f41:1076:ba24:'},  # test for colon at the end
            {"key1": "value1", "key2": 2, "key3": None, "key4": 3.14, "key5": True},
        ]

        expected_output = [
            '---\n...',
            '--- {}',
            '--- []',
            "--- ''",
            "---\nipv6: 'fe80::5a37:f41:1076:ba24:'",
            '---\nkey1: value1\nkey2: 2\nkey3:\nkey4: 3.14\nkey5: true'
        ]

        for test_dict, expected_json in zip(test_input, expected_output):
            cli = JcCli()
            cli.set_custom_colors()
            cli.mono = True
            cli.data_out = test_dict
            self.assertEqual(cli.yaml_out(), expected_json)

    @unittest.skipIf(not RUAMELYAML_INSTALLED, 'ruamel.yaml library not installed')
    def test_cli_yaml_out_yaml11_strings_quoted(self):
        """
        Test YAML output quotes strings that a YAML 1.1 reader would load as
        a boolean or a number (yes/no/on/off, sexagesimal), in values and keys
        """
        test_input = [
            {'filename': 'yes'},
            {'filename': 'No'},
            {'filename': 'ON'},
            {'filename': 'off'},
            {'filename': 'y'},
            {'filename': 'N'},
            {'login_at': '1:30'},
            {'login_at': '10:25'},
            {'login_at': '12:30:45'},
            {'login_at': '-1:30.5'},
            {'login_at': '09:53'},
            {'filename': 'yesterday'},
            {'filename': 'yEs'},
            {'filename': 'normal.txt'},
            {'yes': '1', 'on': '2'},
            {'filename': 'true'},
            {'key1': 'value1', 'key2': 2, 'key3': None, 'key4': 3.14, 'key5': True}
        ]

        expected_output = [
            "---\nfilename: 'yes'",
            "---\nfilename: 'No'",
            "---\nfilename: 'ON'",
            "---\nfilename: 'off'",
            "---\nfilename: 'y'",
            "---\nfilename: 'N'",
            "---\nlogin_at: '1:30'",
            "---\nlogin_at: '10:25'",
            "---\nlogin_at: '12:30:45'",
            "---\nlogin_at: '-1:30.5'",
            '---\nlogin_at: 09:53',
            '---\nfilename: yesterday',
            '---\nfilename: yEs',
            '---\nfilename: normal.txt',
            "---\n'yes': '1'\n'on': '2'",
            "---\nfilename: 'true'",
            '---\nkey1: value1\nkey2: 2\nkey3:\nkey4: 3.14\nkey5: true'
        ]

        for test_dict, expected_yaml in zip(test_input, expected_output):
            cli = JcCli()
            cli.set_custom_colors()
            cli.mono = True
            cli.data_out = test_dict
            output = cli.yaml_out()
            self.assertEqual(output, expected_yaml)
            # a YAML 1.1 reader loads the same data
            yaml11 = ruamel.yaml.YAML(typ='safe', pure=True)
            self.assertEqual(yaml11.load('%YAML 1.1\n' + output + '\n'), test_dict)

    @unittest.skipIf(not RUAMELYAML_INSTALLED, 'ruamel.yaml library not installed')
    def test_cli_yaml_out_no_side_effects(self):
        """
        Test YAML output leaves the ruamel.yaml classes unchanged for other
        code in the same process
        """
        representer = ruamel.yaml.representer.RoundTripRepresenter
        # official_plug_ins() was added in ruamel.yaml 0.15.x
        plug_ins = getattr(ruamel.yaml.YAML, 'official_plug_ins', None)
        ignore_aliases = representer.ignore_aliases
        representers = representer.yaml_representers.copy()
        shared = ['a']
        cli = JcCli()
        cli.set_custom_colors()
        cli.mono = True
        cli.data_out = {'key1': shared, 'key2': shared}
        self.assertEqual(cli.yaml_out(), '---\nkey1:\n- a\nkey2:\n- a')
        self.assertIs(getattr(ruamel.yaml.YAML, 'official_plug_ins', None), plug_ins)
        self.assertIs(representer.ignore_aliases, ignore_aliases)
        self.assertEqual(representer.yaml_representers, representers)

    def test_cli_about_jc(self):
        """
        Test the about information and parser count
        """
        cli = JcCli()
        self.assertEqual(cli.about_jc()['name'], 'jc')
        self.assertGreaterEqual(cli.about_jc()['parser_count'], 55)
        self.assertEqual(cli.about_jc()['parser_count'], len(cli.about_jc()['parsers']))

    def test_cli_parsers_text(self):
        """
        Test that the parser list text for help is not empty
        """
        cli = JcCli()
        self.assertIsNot(cli.parsers_text, '')

    def test_add_meta_to_simple_dict(self):
        """
        Test adding metadata to a dictionary
        """
        cli = JcCli()
        cli.data_out = {'a': 1, 'b': 2}
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.magic_returncode = 2
        cli.magic_run_command = ['ping', '-c3', '192.168.1.123']
        cli.parser_name = 'ping'
        expected = {'a': 1, 'b': 2, '_jc_meta': {'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}
        cli.add_metadata_to_output()
        self.assertEqual(cli.data_out, expected)

    def test_add_meta_to_simple_list(self):
        """
        Test adding metadata to each dictionary in a list
        """
        cli = JcCli()
        cli.data_out = [{'a': 1, 'b': 2},{'a': 3, 'b': 4}]
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.magic_returncode = 2
        cli.magic_run_command = ['ping', '-c3', '192.168.1.123']
        cli.parser_name = 'ping'
        expected = [{'a': 1, 'b': 2, '_jc_meta': {'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}, {'a': 3, 'b': 4, '_jc_meta': {'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}]
        cli.add_metadata_to_output()
        self.assertEqual(cli.data_out, expected)

    def test_add_meta_to_dict_existing_meta(self):
        """
        Test merging metadata into an existing _jc_meta object in a dictionary (streaming parsers)
        """
        cli = JcCli()
        cli.magic_run_command = ['ping', '-c3', '192.168.1.123']
        cli.magic_returncode = 2
        cli.data_out = {'a': 1, 'b': 2, '_jc_meta': {'foo': 'bar'}}
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.parser_name = 'ping'
        expected = {'a': 1, 'b': 2, '_jc_meta': {'foo': 'bar', 'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}
        cli.add_metadata_to_output(merge=True)
        self.assertEqual(cli.data_out, expected)

    def test_add_meta_to_list_existing_meta(self):
        """
        Test merging metadata into existing _jc_meta objects in a list (streaming parsers)
        """
        cli = JcCli()
        cli.data_out = [{'a': 1, 'b': 2, '_jc_meta': {'foo': 'bar'}},{'a': 3, 'b': 4, '_jc_meta': {'foo': 'bar'}}]
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.magic_returncode = 2
        cli.magic_run_command = ['ping', '-c3', '192.168.1.123']
        cli.parser_name = 'ping'
        expected = [{'a': 1, 'b': 2, '_jc_meta': {'foo': 'bar', 'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}, {'a': 3, 'b': 4, '_jc_meta': {'foo': 'bar', 'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}]
        cli.add_metadata_to_output(merge=True)
        self.assertEqual(cli.data_out, expected)

    def test_add_meta_replaces_meta_from_parsed_data(self):
        """
        Test that metadata replaces a _jc_meta field that came from the parsed data
        """
        cli = JcCli()
        cli.quiet = True
        cli.data_out = {'a': 1, '_jc_meta': {'magic_command': ['cat', 'x'], 'magic_command_exit': 0}}
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.parser_name = 'toml'
        expected = {'a': 1, '_jc_meta': {'parser': 'toml', 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}
        cli.add_metadata_to_output()
        self.assertEqual(cli.data_out, expected)

    def test_add_meta_replaces_non_dict_meta(self):
        """
        Test that metadata replaces a _jc_meta field that is not an object
        """
        cli = JcCli()
        cli.quiet = True
        cli.data_out = [{'server': ['nginx'], '_jc_meta': 'anything'}]
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.parser_name = 'http-headers'
        expected = [{'server': ['nginx'], '_jc_meta': {'parser': 'http-headers', 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}]
        cli.add_metadata_to_output()
        self.assertEqual(cli.data_out, expected)

    def test_add_meta_merge_replaces_non_dict_meta(self):
        """
        Test that merging replaces a _jc_meta field that is not an object
        """
        cli = JcCli()
        cli.quiet = True
        cli.data_out = {'a': '1', '_jc_meta': 'x'}
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.parser_name = 'csv-s'
        expected = {'a': '1', '_jc_meta': {'parser': 'csv-s', 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}
        cli.add_metadata_to_output(merge=True)
        self.assertEqual(cli.data_out, expected)

    def test_add_meta_replace_warning_once(self):
        """
        Test that replacing _jc_meta fields prints one warning
        """
        cli = JcCli()
        cli.data_out = [{'a': 1, '_jc_meta': 1}, {'a': 2, '_jc_meta': 2}]
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.parser_name = 'yaml'
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            cli.add_metadata_to_output()
        self.assertEqual(f.getvalue().count('Warning'), 1)
        self.assertIn('_jc_meta', f.getvalue())

    def test_cli_json_out_escapes_c1_controls(self):
        """
        Test that JSON output escapes DEL, C1 control characters and lone surrogates
        """
        cli = JcCli()
        cli.set_custom_colors()
        cli.mono = True
        cli.data_out = {'name': 'a\x9b2Jb\x7fc\xa9\u00e9', 'x': '\udc9b'}
        expected = '{"name":"a\\u009b2Jb\\u007fc\xa9\u00e9","x":"\\udc9b"}'
        self.assertEqual(cli.json_out(), expected)

    def test_slice_none_str(self):
        """
        Test line slicing of a string with no start or end
        """
        cli = JcCli()
        cli.slice_start = None
        cli.slice_end = None
        cli.data_in = '''\
        row0
        row1
        row2
        row3
        row4
        row5'''
        expected = '''\
        row0
        row1
        row2
        row3
        row4
        row5'''
        cli.slicer()
        self.assertEqual(cli.data_in, expected)

    def test_slice_positive_str(self):
        """
        Test line slicing of a string with a positive start and end
        """
        cli = JcCli()
        cli.slice_start = 1
        cli.slice_end = 5
        cli.data_in = '''\
        row0
        row1
        row2
        row3
        row4
        row5'''
        expected = '''\
        row1
        row2
        row3
        row4'''
        cli.slicer()
        self.assertEqual(cli.data_in, expected)

    def test_slice_negative_str(self):
        """
        Test line slicing of a string with a negative end
        """
        cli = JcCli()
        cli.slice_start = 1
        cli.slice_end = -1
        cli.data_in = '''\
        row0
        row1
        row2
        row3
        row4
        row5'''
        expected = '''\
        row1
        row2
        row3
        row4'''
        cli.slicer()
        self.assertEqual(cli.data_in, expected)

    def test_slice_none_iter(self):
        """
        Test line slicing of an iterable with no start or end
        """
        cli = JcCli()
        cli.slice_start = None
        cli.slice_end = None
        cli.data_in = [
            'row0',
            'row1',
            'row2',
            'row3',
            'row4',
            'row5'
        ]
        expected = [
            'row0',
            'row1',
            'row2',
            'row3',
            'row4',
            'row5'
        ]
        cli.slicer()
        self.assertEqual(cli.data_in, expected)

    def test_slice_positive_iter(self):
        """
        Test line slicing of an iterable with a positive start and end
        """
        cli = JcCli()
        cli.slice_start = 1
        cli.slice_end = 5
        cli.data_in = [
            'row0',
            'row1',
            'row2',
            'row3',
            'row4',
            'row5'
        ]
        expected = [
            'row1',
            'row2',
            'row3',
            'row4'
        ]
        cli.slicer()
        self.assertEqual(list(cli.data_in), expected)

    def test_slice_negative_iter(self):
        """
        Test line slicing of an iterable with a negative end
        """
        cli = JcCli()
        cli.slice_start = 1
        cli.slice_end = -1
        cli.data_in = [
            'row0',
            'row1',
            'row2',
            'row3',
            'row4',
            'row5'
        ]
        expected = [
            'row1',
            'row2',
            'row3',
            'row4'
        ]
        cli.slicer()
        self.assertEqual(list(cli.data_in), expected)

    def test_slurp_standard(self):
        """
        Test --slurp with a standard parser
        """
        cli = JcCli()
        cli.parser_module = url_parser
        cli.data_in = '''http://www.google.com
            https://www.kelly.com/testing
            https://mail.apple.com'''
        expected = [{"url":"http://www.google.com","scheme":"http","netloc":"www.google.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"query_obj":None,"fragment":None,"username":None,"password":None,"hostname":"www.google.com","port":None,"encoded":{"url":"http://www.google.com","scheme":"http","netloc":"www.google.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"fragment":None,"username":None,"password":None,"hostname":"www.google.com","port":None},"decoded":{"url":"http://www.google.com","scheme":"http","netloc":"www.google.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"fragment":None,"username":None,"password":None,"hostname":"www.google.com","port":None}},{"url":"https://www.kelly.com/testing","scheme":"https","netloc":"www.kelly.com","path":"/testing","parent":"/","filename":"testing","stem":"testing","extension":None,"path_list":["testing"],"query":None,"query_obj":None,"fragment":None,"username":None,"password":None,"hostname":"www.kelly.com","port":None,"encoded":{"url":"https://www.kelly.com/testing","scheme":"https","netloc":"www.kelly.com","path":"/testing","parent":"/","filename":"testing","stem":"testing","extension":None,"path_list":["testing"],"query":None,"fragment":None,"username":None,"password":None,"hostname":"www.kelly.com","port":None},"decoded":{"url":"https://www.kelly.com/testing","scheme":"https","netloc":"www.kelly.com","path":"/testing","parent":"/","filename":"testing","stem":"testing","extension":None,"path_list":["testing"],"query":None,"fragment":None,"username":None,"password":None,"hostname":"www.kelly.com","port":None}},{"url":"https://mail.apple.com","scheme":"https","netloc":"mail.apple.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"query_obj":None,"fragment":None,"username":None,"password":None,"hostname":"mail.apple.com","port":None,"encoded":{"url":"https://mail.apple.com","scheme":"https","netloc":"mail.apple.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"fragment":None,"username":None,"password":None,"hostname":"mail.apple.com","port":None},"decoded":{"url":"https://mail.apple.com","scheme":"https","netloc":"mail.apple.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"fragment":None,"username":None,"password":None,"hostname":"mail.apple.com","port":None}}]
        cli.create_slurp_output()
        self.assertEqual(cli.data_out, expected)

    def test_slurp_line_separator(self):
        """
        Test that --slurp splits lines on LF, CRLF and lone CR but not on other line-break characters
        """
        cli = JcCli()
        cli.parser_module = url_parser
        cli.data_in = 'https://a.example/a\nhttps://b.example/x\u2028https://c.example/y\r\nhttps://d.example/d\rhttps://e.example/e\n'
        expected = ['https://a.example/a', 'https://b.example/x\u2028https://c.example/y', 'https://d.example/d', 'https://e.example/e']
        cli.create_slurp_output()
        self.assertEqual(cli.inputlist, expected)
        self.assertEqual(len(cli.data_out), 4)

    def test_slurp_standard_with_meta_out(self):
        """
        Test --slurp with a standard parser and metadata output
        """
        cli = JcCli()
        cli.meta_out = True
        cli.parser_module = url_parser
        cli.data_in = '''http://www.google.com
            https://www.kelly.com/testing
            https://mail.apple.com'''
        expected = {"result":[{"url":"http://www.google.com","scheme":"http","netloc":"www.google.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"query_obj":None,"fragment":None,"username":None,"password":None,"hostname":"www.google.com","port":None,"encoded":{"url":"http://www.google.com","scheme":"http","netloc":"www.google.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"fragment":None,"username":None,"password":None,"hostname":"www.google.com","port":None},"decoded":{"url":"http://www.google.com","scheme":"http","netloc":"www.google.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"fragment":None,"username":None,"password":None,"hostname":"www.google.com","port":None}},{"url":"https://www.kelly.com/testing","scheme":"https","netloc":"www.kelly.com","path":"/testing","parent":"/","filename":"testing","stem":"testing","extension":None,"path_list":["testing"],"query":None,"query_obj":None,"fragment":None,"username":None,"password":None,"hostname":"www.kelly.com","port":None,"encoded":{"url":"https://www.kelly.com/testing","scheme":"https","netloc":"www.kelly.com","path":"/testing","parent":"/","filename":"testing","stem":"testing","extension":None,"path_list":["testing"],"query":None,"fragment":None,"username":None,"password":None,"hostname":"www.kelly.com","port":None},"decoded":{"url":"https://www.kelly.com/testing","scheme":"https","netloc":"www.kelly.com","path":"/testing","parent":"/","filename":"testing","stem":"testing","extension":None,"path_list":["testing"],"query":None,"fragment":None,"username":None,"password":None,"hostname":"www.kelly.com","port":None}},{"url":"https://mail.apple.com","scheme":"https","netloc":"mail.apple.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"query_obj":None,"fragment":None,"username":None,"password":None,"hostname":"mail.apple.com","port":None,"encoded":{"url":"https://mail.apple.com","scheme":"https","netloc":"mail.apple.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"fragment":None,"username":None,"password":None,"hostname":"mail.apple.com","port":None},"decoded":{"url":"https://mail.apple.com","scheme":"https","netloc":"mail.apple.com","path":None,"parent":None,"filename":None,"stem":None,"extension":None,"path_list":None,"query":None,"fragment":None,"username":None,"password":None,"hostname":"mail.apple.com","port":None}}],"_jc_meta":{"parser":"url","timestamp":1659659829.273349,"slice_start":None,"slice_end":None,"input_list":["http://www.google.com","https://www.kelly.com/testing","https://mail.apple.com"]}}
        cli.create_slurp_output()
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.parser_name = 'url'
        cli.add_metadata_to_output()
        self.assertEqual(cli.data_out, expected)

    def test_slurp_proc(self):
        """
        Test --slurp with a list of /proc files
        """
        cli = JcCli()
        cli.parser_module = proc_parser
        cli.inputlist = ['/proc/stat', '/proc/cpuinfo']
        cli.data_in = [
'''cpu  6002 152 8398 3444436 448 0 1174 0 0 0
cpu0 2784 137 4367 1732802 225 0 221 0 0 0
cpu1 3218 15 4031 1711634 223 0 953 0 0 0
intr 2496709 18 73 0 0 0 0 0 0 1 0 0 0 18 0 0 0 4219 37341 423366 128490 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9063 2363 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
ctxt 4622716
btime 1662154781
processes 9831
procs_running 1
procs_blocked 0
softirq 3478985 35230 1252057 3467 128583 51014 0 171199 1241297 0 596138
''',
'''processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 142
model name	: Intel(R) Core(TM) i5-7360U CPU @ 2.30GHz
stepping	: 9
cpu MHz		: 2303.998
cache size	: 4096 KB
physical id	: 0
siblings	: 1
core id		: 0
cpu cores	: 1
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 22
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc eagerfpu pni pclmulqdq monitor ssse3 cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d
bogomips	: 4607.99
clflush size	: 64
cache_alignment	: 64
address sizes	: 39 bits physical, 48 bits virtual
power management:
'''
        ]
        expected = [{"cpu":{"user":6002,"nice":152,"system":8398,"idle":3444436,"iowait":448,"irq":0,"softirq":1174,"steal":0,"guest":0,"guest_nice":0},"cpu0":{"user":2784,"nice":137,"system":4367,"idle":1732802,"iowait":225,"irq":0,"softirq":221,"steal":0,"guest":0,"guest_nice":0},"cpu1":{"user":3218,"nice":15,"system":4031,"idle":1711634,"iowait":223,"irq":0,"softirq":953,"steal":0,"guest":0,"guest_nice":0},"interrupts":[2496709,18,73,0,0,0,0,0,0,1,0,0,0,18,0,0,0,4219,37341,423366,128490,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9063,2363,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"context_switches":4622716,"boot_time":1662154781,"processes":9831,"processes_running":1,"processes_blocked":0,"softirq":[3478985,35230,1252057,3467,128583,51014,0,171199,1241297,0,596138],"_file":"/proc/stat"},[{"processor":0,"vendor_id":"GenuineIntel","cpu family":6,"model":142,"model name":"Intel(R) Core(TM) i5-7360U CPU @ 2.30GHz","stepping":9,"cpu MHz":2303.998,"cache size":"4096 KB","physical id":0,"siblings":1,"core id":0,"cpu cores":1,"apicid":0,"initial apicid":0,"fpu":True,"fpu_exception":True,"cpuid level":22,"wp":True,"flags":["fpu","vme","de","pse","tsc","msr","pae","mce","cx8","apic","sep","mtrr","pge","mca","cmov","pat","pse36","clflush","mmx","fxsr","sse","sse2","ht","syscall","nx","rdtscp","lm","constant_tsc","rep_good","nopl","xtopology","nonstop_tsc","eagerfpu","pni","pclmulqdq","monitor","ssse3","cx16","pcid","sse4_1","sse4_2","x2apic","movbe","popcnt","aes","xsave","avx","rdrand","hypervisor","lahf_lm","abm","3dnowprefetch","fsgsbase","avx2","invpcid","rdseed","clflushopt","md_clear","flush_l1d"],"bogomips":4607.99,"clflush size":64,"cache_alignment":64,"address sizes":"39 bits physical, 48 bits virtual","power management":None,"address_size_physical":39,"address_size_virtual":48,"cache_size_num":4096,"cache_size_unit":"KB","_file":"/proc/cpuinfo"}]]
        cli.quiet = True
        cli.create_slurp_output()
        self.assertEqual(cli.data_out, expected)

    def test_slurp_proc_with_meta_out(self):
        """
        Test --slurp with a list of /proc files and metadata output
        """
        cli = JcCli()
        cli.meta_out = True
        cli.parser_module = proc_parser
        cli.magic_run_command = ['/proc/stat', '/proc/cpuinfo']
        cli.magic_returncode = 0
        cli.inputlist = ['/proc/stat', '/proc/cpuinfo']
        cli.data_in = [
'''cpu  6002 152 8398 3444436 448 0 1174 0 0 0
cpu0 2784 137 4367 1732802 225 0 221 0 0 0
cpu1 3218 15 4031 1711634 223 0 953 0 0 0
intr 2496709 18 73 0 0 0 0 0 0 1 0 0 0 18 0 0 0 4219 37341 423366 128490 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9063 2363 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
ctxt 4622716
btime 1662154781
processes 9831
procs_running 1
procs_blocked 0
softirq 3478985 35230 1252057 3467 128583 51014 0 171199 1241297 0 596138
''',
'''processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 142
model name	: Intel(R) Core(TM) i5-7360U CPU @ 2.30GHz
stepping	: 9
cpu MHz		: 2303.998
cache size	: 4096 KB
physical id	: 0
siblings	: 1
core id		: 0
cpu cores	: 1
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 22
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc eagerfpu pni pclmulqdq monitor ssse3 cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d
bogomips	: 4607.99
clflush size	: 64
cache_alignment	: 64
address sizes	: 39 bits physical, 48 bits virtual
power management:
'''
        ]
        expected = {"result":[{"cpu":{"user":6002,"nice":152,"system":8398,"idle":3444436,"iowait":448,"irq":0,"softirq":1174,"steal":0,"guest":0,"guest_nice":0},"cpu0":{"user":2784,"nice":137,"system":4367,"idle":1732802,"iowait":225,"irq":0,"softirq":221,"steal":0,"guest":0,"guest_nice":0},"cpu1":{"user":3218,"nice":15,"system":4031,"idle":1711634,"iowait":223,"irq":0,"softirq":953,"steal":0,"guest":0,"guest_nice":0},"interrupts":[2496709,18,73,0,0,0,0,0,0,1,0,0,0,18,0,0,0,4219,37341,423366,128490,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9063,2363,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"context_switches":4622716,"boot_time":1662154781,"processes":9831,"processes_running":1,"processes_blocked":0,"softirq":[3478985,35230,1252057,3467,128583,51014,0,171199,1241297,0,596138],"_file":"/proc/stat"},[{"processor":0,"vendor_id":"GenuineIntel","cpu family":6,"model":142,"model name":"Intel(R) Core(TM) i5-7360U CPU @ 2.30GHz","stepping":9,"cpu MHz":2303.998,"cache size":"4096 KB","physical id":0,"siblings":1,"core id":0,"cpu cores":1,"apicid":0,"initial apicid":0,"fpu":True,"fpu_exception":True,"cpuid level":22,"wp":True,"flags":["fpu","vme","de","pse","tsc","msr","pae","mce","cx8","apic","sep","mtrr","pge","mca","cmov","pat","pse36","clflush","mmx","fxsr","sse","sse2","ht","syscall","nx","rdtscp","lm","constant_tsc","rep_good","nopl","xtopology","nonstop_tsc","eagerfpu","pni","pclmulqdq","monitor","ssse3","cx16","pcid","sse4_1","sse4_2","x2apic","movbe","popcnt","aes","xsave","avx","rdrand","hypervisor","lahf_lm","abm","3dnowprefetch","fsgsbase","avx2","invpcid","rdseed","clflushopt","md_clear","flush_l1d"],"bogomips":4607.99,"clflush size":64,"cache_alignment":64,"address sizes":"39 bits physical, 48 bits virtual","power management":None,"address_size_physical":39,"address_size_virtual":48,"cache_size_num":4096,"cache_size_unit":"KB","_file":"/proc/cpuinfo"}]],"_jc_meta":{"parser":"proc","timestamp":1659659829.273349,"slice_start":None,"slice_end":None,"magic_command":["/proc/stat","/proc/cpuinfo"],"magic_command_exit":0,"input_list":["/proc/stat","/proc/cpuinfo"]}}
        cli.quiet = True
        cli.create_slurp_output()
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.parser_name = 'proc'
        cli.add_metadata_to_output()
        self.assertEqual(cli.data_out, expected)

    def test_slurp_non_utf8_raises(self):
        """
        Test that --slurp raises an error for input that is not valid UTF-8
        """
        cli = JcCli()
        cli.parser_module = url_parser
        cli.data_in = b'https://a.example/a\n\xff\n'
        with self.assertRaises(TypeError):
            cli.create_slurp_output()

    def test_slurp_non_utf8_exit_code(self):
        """
        Test that --slurp exits with an error and no output for input that is not valid UTF-8
        """
        stdin = io.TextIOWrapper(io.BytesIO(b'a\n\xff\n'), encoding='utf-8')
        out = io.StringIO()
        err = io.StringIO()
        with mock.patch('sys.argv', ['jc', '--slurp', '--path']), \
             mock.patch('sys.stdin', stdin), \
             contextlib.redirect_stdout(out), \
             contextlib.redirect_stderr(err):
            with self.assertRaises(SystemExit) as cm:
                JcCli().run()
        self.assertEqual(100, cm.exception.code)
        self.assertEqual('', out.getvalue())
        self.assertIn('path parser could not parse the input data', err.getvalue())

    def test_streaming_error_message_qq(self):
        """
        Test the error message of a streaming parser error: the -qq hint is shown only when -qq is not used
        """
        for options, hint in ((['-q'], True), (['-qq'], False)):
            err = io.StringIO()
            # STDIN must look piped, or run() stops at 'Missing piped data' when
            # the tests are run from a terminal
            with mock.patch('sys.argv', ['jc'] + options + ['--ls-s']), \
                 mock.patch('sys.stdin', io.StringIO()), \
                 mock.patch.object(JcCli, 'streaming_parse_and_print', side_effect=ValueError('x')), \
                 mock.patch.object(jc.utils, 'CLI_QUIET', False), \
                 contextlib.redirect_stdout(io.StringIO()), \
                 contextlib.redirect_stderr(err):
                with self.assertRaises(SystemExit) as cm:
                    JcCli().run()
            self.assertEqual(100, cm.exception.code)
            self.assertIn('ls-s parser could not parse the input data', err.getvalue())
            self.assertEqual(hint, 'Use the -qq option' in err.getvalue())

    def test_slice_multiple_proc_files(self):
        """
        Test that line slicing a list of /proc files exits with an error
        """
        cli = JcCli()
        cli.slice_str = '-1:'
        cli.inputlist = ['/proc/uptime', '/proc/loadavg']
        cli.data_in = ['1.0 2.0\n', '0.1 0.2 0.3 1/2 3\n']
        with self.assertRaises(SystemExit) as cm:
            with contextlib.redirect_stderr(io.StringIO()) as err:
                cli.slicer()
        self.assertEqual(100, cm.exception.code)
        self.assertIn('Line slicing is not supported with multiple /proc files', err.getvalue())

    def test_magic_proc_path_traversal(self):
        """
        Test that a /proc path that leads outside of /proc exits with an error
        """
        # traversal outside of /proc should exit with an error instead of opening the file
        cli = JcCli()
        cli.magic_run_command = ['/proc/../etc/hosts']
        cli.magic_run_command_str = '/proc/../etc/hosts'
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()) as err:
                cli.do_magic()
        self.assertIsNone(cli.magic_stdout)
        self.assertIn('/proc/../etc/hosts', err.getvalue())

    @unittest.skipIf(not os.path.exists('/proc/uptime'), '/proc not available')
    def test_magic_proc_path_traversal_multiple_files(self):
        """
        Test that a /proc file list with a path outside of /proc exits with an error
        """
        # a bad entry in the file list should exit with an error, even if the first entry is valid
        cli = JcCli()
        cli.magic_run_command = ['/proc/uptime', '/proc/../etc/hosts']
        cli.magic_run_command_str = '/proc/uptime /proc/../etc/hosts'
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()) as err:
                cli.do_magic()
        self.assertIsNone(cli.magic_stdout)
        self.assertIn('/proc/../etc/hosts', err.getvalue())

    @unittest.skipIf(not os.path.exists('/proc/uptime'), '/proc not available')
    def test_magic_proc_single_file(self):
        """
        Test magic syntax with a single /proc file
        """
        cli = JcCli()
        cli.magic_run_command = ['/proc/uptime']
        cli.magic_run_command_str = '/proc/uptime'
        cli.do_magic()
        self.assertEqual('proc', cli.magic_found_parser)
        self.assertIsInstance(cli.magic_stdout, str)

    @unittest.skipIf(not os.path.exists('/proc/uptime'), '/proc not available')
    def test_magic_proc_empty_file_does_not_read_stdin(self):
        """
        Test magic syntax with an empty /proc file (e.g. /proc/<pid>/maps of a
        zombie process): STDIN is not read
        """
        cli = JcCli()
        cli.magic_run_command = ['/proc/uptime']
        cli.magic_run_command_str = '/proc/uptime'
        with mock.patch.object(JcCli, 'open_text_file', return_value=''):
            cli.do_magic()
        self.assertEqual('', cli.magic_stdout)
        cli.parser_module = proc_parser
        with mock.patch('sys.stdin') as mock_stdin:
            mock_stdin.buffer.read.return_value = b'0.13 0.23 0.25 1/185 1758\n'
            self.assertRaises(ParseError, cli.standard_parse_and_print)
        mock_stdin.buffer.read.assert_not_called()

    @unittest.skipIf(not os.path.exists('/proc/self/status'), '/proc not available')
    def test_magic_proc_symlinked_file(self):
        """
        Test magic syntax with a /proc file reached through a symlink
        """
        # /proc/self is a symlink and must still be readable
        cli = JcCli()
        cli.magic_run_command = ['/proc/self/status']
        cli.magic_run_command_str = '/proc/self/status'
        cli.do_magic()
        self.assertIsInstance(cli.magic_stdout, str)

    @unittest.skipIf(not os.path.exists('/proc/uptime'), '/proc not available')
    def test_magic_proc_multiple_files(self):
        """
        Test magic syntax with a list of /proc files
        """
        cli = JcCli()
        cli.magic_run_command = ['/proc/uptime', '/proc/stat']
        cli.magic_run_command_str = '/proc/uptime /proc/stat'
        cli.do_magic()
        self.assertTrue(cli.slurp)
        self.assertEqual(['/proc/uptime', '/proc/stat'], cli.inputlist)
        self.assertEqual(2, len(cli.magic_stdout))

    def test_magic_is_proc_path(self):
        """
        Test detection of paths inside /proc
        """
        paths = {
            '/proc': True,
            '/proc/uptime': True,
            '/proc/self/status': True,
            '/proc/1/fd/1': True,
            '/proc//uptime': True,
            '//proc/uptime': True,
            '/proc/./uptime': True,
            '/proc/': True,
            '/proc/../proc/uptime': True,
            '/proc/../etc/hosts': False,
            '/proc/..': False,
            '/proc/./..': False,
            '/proc/../tmp/uptime': False,
            '/procfs/uptime': False,
            '/etc/hosts': False
        }

        for path, expected in paths.items():
            self.assertEqual(expected, JcCli.is_proc_path(path), path)

    def test_magic_open_text_file_no_newline_translation(self):
        """
        Test that /proc files are read without newline translation
        """
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'wb') as f:
                f.write(b'1 (a\rb) S 0\nc\r\n')
            self.assertEqual('1 (a\rb) S 0\nc\r\n', JcCli.open_text_file(path))
        finally:
            os.remove(path)

    def test_magic_run_user_command_no_newline_translation(self):
        """
        Test that magic command output is read without newline translation
        """
        code = ("import sys; "
                "sys.stdout.buffer.write(b'a\\rb\\r\\nc\\n'); "
                "sys.stderr.buffer.write(b'e\\rf\\n')")
        cli = JcCli()
        cli.magic_run_command = [sys.executable, '-c', code]
        cli.run_user_command()
        self.assertEqual('a\rb\r\nc\n', cli.magic_stdout)
        self.assertEqual('e\rf\n', cli.magic_stderr)
        self.assertEqual(0, cli.magic_returncode)

    def test_magic_run_user_command_empty_output(self):
        """
        Test a magic command with no output
        """
        cli = JcCli()
        cli.magic_run_command = [sys.executable, '-c', 'pass']
        cli.run_user_command()
        self.assertEqual('\n', cli.magic_stdout)
        self.assertEqual('', cli.magic_stderr)
        self.assertEqual(0, cli.magic_returncode)


    def test_stdin_lines(self):
        """
        Test that STDIN lines are split on LF and CRLF, keeping a lone CR in the line
        """
        stdin = io.TextIOWrapper(io.BytesIO(b'a\r\nb\rc\nd'), encoding='utf-8', errors='strict')
        self.assertEqual(['a\n', 'b\rc\n', 'd'], list(JcCli.stdin_lines(stdin)))

    def test_stdin_lines_no_buffer(self):
        """
        Test reading STDIN lines from a text stream without a binary buffer
        """
        stdin = io.StringIO('a\nb\n')
        self.assertEqual(['a\n', 'b\n'], list(JcCli.stdin_lines(stdin)))

    def _streaming_ls_records(self, data):
        stdin = io.TextIOWrapper(io.BytesIO(data), encoding='utf-8', errors='strict')
        cli = JcCli()
        cli.parser_module = ls_s_parser
        cli.mono = True
        cli.quiet = True
        cli.ignore_exceptions = True
        f = io.StringIO()
        with mock.patch('sys.stdin', stdin), contextlib.redirect_stdout(f):
            cli.streaming_parse_and_print()
        records = [json.loads(x) for x in f.getvalue().splitlines()]
        return records

    def test_streaming_line_endings(self):
        """
        Test streaming parser output for LF, CRLF and lone CR line endings
        """
        data = (b'-rw-r--r-- 1 root root 0 Jan  1 00:00 aaa\n'
                b'-rw-r--r-- 1 root root 0 Jan  1 00:00 m\rmm\n'
                b'-rw-r--r-- 1 root root 0 Jan  1 00:00 zzz\r\n')
        records = self._streaming_ls_records(data)
        self.assertEqual(['aaa', 'm\rmm', 'zzz'], [x['filename'] for x in records])
        self.assertTrue(all(x['_jc_meta']['success'] for x in records))

    def test_streaming_non_utf8(self):
        """
        Test that streaming parsers show input bytes that are not valid UTF-8 as escapes
        """
        data = (b'-rw-r--r-- 1 root root 0 Jan  1 00:00 aaa\n'
                b'-rw-r--r-- 1 root root 0 Jan  1 00:00 mmm\xff\n'
                b'-rw-r--r-- 1 root root 0 Jan  1 00:00 zzz\n')
        records = self._streaming_ls_records(data)
        self.assertEqual(['aaa', 'mmm\\xff', 'zzz'], [x['filename'] for x in records])
        self.assertTrue(all(x['_jc_meta']['success'] for x in records))

if __name__ == '__main__':
    unittest.main()
