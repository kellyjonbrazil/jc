import unittest
import pygments
from pygments.token import (Name, Number, String, Keyword)
import jc.cli


class MyTests(unittest.TestCase):
    def test_cli_magic_parser(self):
        commands = {
            'jc -p systemctl list-sockets': (True, ['systemctl', 'list-sockets'], '--systemctl-ls', ['p']),
            'jc -p systemctl list-unit-files': (True, ['systemctl', 'list-unit-files'], '--systemctl-luf', ['p']),
            'jc -p pip list': (True, ['pip', 'list'], '--pip-list', ['p']),
            'jc -p pip3 list': (True, ['pip3', 'list'], '--pip-list', ['p']),
            'jc -p pip show jc': (True, ['pip', 'show', 'jc'], '--pip-show', ['p']),
            'jc -p pip3 show jc': (True, ['pip3', 'show', 'jc'], '--pip-show', ['p']),
            'jc -prd last': (True, ['last'], '--last', ['p', 'r', 'd']),
            'jc -prdd lastb': (True, ['lastb'], '--last', ['p', 'r', 'd', 'd']),
            'jc -p airport -I': (True, ['airport', '-I'], '--airport', ['p']),
            'jc -p -r airport -I': (True, ['airport', '-I'], '--airport', ['p', 'r']),
            'jc -prd airport -I': (True, ['airport', '-I'], '--airport', ['p', 'r', 'd']),
            'jc -p nonexistent command': (False, ['nonexistent', 'command'], None, ['p']),
            'jc -ap': (False, None, None, []),
            'jc -a arp -a': (False, None, None, []),
            'jc -v': (False, None, None, []),
            'jc -h': (False, None, None, []),
            'jc -h --arp': (False, None, None, []),
            'jc -h arp': (False, None, None, []),
            'jc -h arp -a': (False, None, None, [])
        }

        for command, expected_command in commands.items():
            self.assertEqual(jc.cli.magic_parser(command.split(' ')), expected_command)

    def test_cli_set_env_colors(self):
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
            self.assertEqual(jc.cli.set_env_colors(jc_colors), expected_colors)

    def test_cli_json_out(self):
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
            self.assertEqual(jc.cli.json_out(test_dict), expected_json)

    def test_cli_json_out_mono(self):
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
            self.assertEqual(jc.cli.json_out(test_dict, mono=True), expected_json)

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
            self.assertEqual(jc.cli.json_out(test_dict, pretty=True), expected_json)

    def test_cli_yaml_out(self):
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
            self.assertEqual(jc.cli.yaml_out(test_dict), expected_json)

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
            self.assertEqual(jc.cli.yaml_out(test_dict, mono=True), expected_json)

    def test_cli_about_jc(self):
        self.assertEqual(jc.cli.about_jc()['name'], 'jc')
        self.assertGreaterEqual(jc.cli.about_jc()['parser_count'], 55)
        self.assertEqual(jc.cli.about_jc()['parser_count'], len(jc.cli.about_jc()['parsers']))

if __name__ == '__main__':
    unittest.main()