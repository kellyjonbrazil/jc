import unittest
from jc.shell_completions import bash_completion, zsh_completion, xonsh_completion


class MyTests(unittest.TestCase):
    def test_bash_completion(self):
        """
        Test the Bash completion script generation
        """
        completion = bash_completion()
        self.assertIn('complete -F _jc jc', completion)
        self.assertIn('--xonsh-comp -X', completion)

    def test_zsh_completion(self):
        """
        Test the Zsh completion script generation
        """
        completion = zsh_completion()
        self.assertIn('#compdef jc', completion)
        self.assertIn('--xonsh-comp -X', completion)

    def test_xonsh_completion_is_valid_python(self):
        """
        Test that the Xonsh completion script is valid python
        """
        compile(xonsh_completion(), 'jc_xonsh_completion.py', 'exec')

    def test_xonsh_completion_registers_completer(self):
        """
        Test that the Xonsh completion script registers the jc completer
        """
        completion = xonsh_completion()
        self.assertIn("@contextual_command_completer_for('jc')", completion)
        self.assertIn("add_one_completer('jc', _jc_completer, 'start')", completion)

    def test_xonsh_completion_contents(self):
        """
        Test that the Xonsh completion script contains the expected options,
        parsers, and magic commands
        """
        completion = xonsh_completion()
        self.assertIn("'--pretty': 'pretty print output',", completion)
        self.assertIn("'-p': 'pretty print output',", completion)
        self.assertIn("'--about': 'about jc',", completion)
        self.assertIn("'--help': 'help", completion)
        self.assertIn("'--version': 'version info',", completion)
        self.assertIn("'--xonsh-comp': 'gen Xonsh completion", completion)
        self.assertIn("'--arp': '`arp` command parser',", completion)
        self.assertIn("'arp': 'run \"arp\" command with magic syntax.',", completion)

        # special, about, and help options must not be in the standard options
        options_block = completion.split('jc_options = {')[1].split('}')[0]
        self.assertNotIn("'--version'", options_block)
        self.assertNotIn("'--about'", options_block)
        self.assertNotIn("'--help'", options_block)


if __name__ == '__main__':
    unittest.main()
