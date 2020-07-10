import unittest
import pygments
from pygments.token import (Name, Number, String, Keyword)
import jc.cli


class MyTests(unittest.TestCase):
    def test_cli_generate_magic_command(self):
        commands = {
            'jc -p systemctl list-sockets': 'systemctl list-sockets | jc --systemctl-ls -p',
            'jc -p systemctl list-unit-files': 'systemctl list-unit-files | jc --systemctl-luf -p',
            'jc -p pip list': 'pip list | jc --pip-list -p',
            'jc -p pip3 list': 'pip3 list | jc --pip-list -p',
            'jc -p pip show jc': 'pip show jc | jc --pip-show -p',
            'jc -p pip3 show jc': 'pip3 show jc | jc --pip-show -p',
            'jc -prd last': 'last | jc --last -prd',
            'jc -prd lastb': 'lastb | jc --last -prd',
            'jc -p airport -I': 'airport -I | jc --airport -p',
            'jc -p -r airport -I': 'airport -I | jc --airport -pr',
            'jc -prd airport -I': 'airport -I | jc --airport -prd',
            'jc -p nonexistent command': 'nonexistent command',
            'jc -ap': None
        }

        for command, expected_command in commands.items():
            self.assertEqual(jc.cli.generate_magic_command(command.split(' '))[1], expected_command)

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
