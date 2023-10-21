import os
import unittest
from datetime import datetime, timezone
try:
    import pygments
    from pygments.token import (Name, Number, String, Keyword)
    PYGMENTS_INSTALLED=True
except ModuleNotFoundError:
    PYGMENTS_INSTALLED=False
from jc.cli import JcCli


class MyTests(unittest.TestCase):
    def test_cli_magic_parser(self):
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

    def test_cli_set_env_colors(self):
        if PYGMENTS_INSTALLED:
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

    def test_cli_json_out(self):
        if PYGMENTS_INSTALLED:
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

    def test_cli_json_out_mono(self):
        if PYGMENTS_INSTALLED:
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

        def test_cli_json_out_pretty(self):
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

    def test_cli_yaml_out(self):
        if PYGMENTS_INSTALLED:
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

    def test_cli_yaml_out_mono(self):
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

    def test_cli_about_jc(self):
        cli = JcCli()
        self.assertEqual(cli.about_jc()['name'], 'jc')
        self.assertGreaterEqual(cli.about_jc()['parser_count'], 55)
        self.assertEqual(cli.about_jc()['parser_count'], len(cli.about_jc()['parsers']))

    def test_add_meta_to_simple_dict(self):
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
        cli = JcCli()
        cli.magic_run_command = ['ping', '-c3', '192.168.1.123']
        cli.magic_returncode = 2
        cli.data_out = {'a': 1, 'b': 2, '_jc_meta': {'foo': 'bar'}}
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.parser_name = 'ping'
        expected = {'a': 1, 'b': 2, '_jc_meta': {'foo': 'bar', 'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}
        cli.add_metadata_to_output()
        self.assertEqual(cli.data_out, expected)

    def test_add_meta_to_list_existing_meta(self):
        cli = JcCli()
        cli.data_out = [{'a': 1, 'b': 2, '_jc_meta': {'foo': 'bar'}},{'a': 3, 'b': 4, '_jc_meta': {'foo': 'bar'}}]
        cli.run_timestamp = datetime(2022, 8, 5, 0, 37, 9, 273349, tzinfo=timezone.utc)
        cli.magic_returncode = 2
        cli.magic_run_command = ['ping', '-c3', '192.168.1.123']
        cli.parser_name = 'ping'
        expected = [{'a': 1, 'b': 2, '_jc_meta': {'foo': 'bar', 'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}, {'a': 3, 'b': 4, '_jc_meta': {'foo': 'bar', 'parser': 'ping', 'magic_command': ['ping', '-c3', '192.168.1.123'], 'magic_command_exit': 2, 'timestamp': 1659659829.273349, 'slice_start': None, 'slice_end': None}}]
        cli.add_metadata_to_output()
        self.assertEqual(cli.data_out, expected)

    def test_slice_none_str(self):
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

if __name__ == '__main__':
    unittest.main()