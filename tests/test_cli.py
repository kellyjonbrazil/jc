import os
import unittest
import jc.cli


class MyTests(unittest.TestCase):
    def test_cli(self):
        commands = {
            "jc -p systemctl list-sockets": "systemctl list-sockets | jc --systemctl-ls -p",
            "jc -p systemctl list-unit-files": "systemctl list-unit-files | jc --systemctl-luf -p",
        }

        for command, expected_command in commands.items():
            self.assertEquals(jc.cli.generate_magic_command(command.split(" "))[1], expected_command)
