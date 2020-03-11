import unittest
import jc.cli


class MyTests(unittest.TestCase):
    def test_cli(self):
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
