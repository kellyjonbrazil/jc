import os
import json
import unittest
import jc.parsers.netrc

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netrc.out'), 'r', encoding='utf-8') as f:
        netrc = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netrc-quoting-whitespace.out'), 'r', encoding='utf-8') as f:
        netrc_quoting_whitespace = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netrc.json'), 'r', encoding='utf-8') as f:
        netrc_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netrc-quoting-whitespace.json'), 'r', encoding='utf-8') as f:
        netrc_quoting_whitespace_json = json.loads(f.read())

    # whitespace characters other than space, tab, CR and LF
    other_whitespace = [chr(c) for c in range(0x110000) if chr(c).isspace() and chr(c) not in ' \t\r\n']

    def test_netrc_nodata(self):
        """
        Test 'netrc' with no data
        """
        self.assertEqual(jc.parsers.netrc.parse('', quiet=True), [])

    def test_netrc(self):
        """
        Test a '.netrc' file with:

        - a one-keyword-per-line machine block
        - a machine block written entirely on one line
        - a default block (the bare 'default' keyword, no value)
        - a macdef block whose body is terminated by a blank line
        - a macdef block whose body is terminated by EOF instead of a
          blank line
        - a leading comment line, which should be silently ignored
        """
        self.assertEqual(jc.parsers.netrc.parse(self.netrc, quiet=True), self.netrc_json)

    def test_netrc_quoting_whitespace(self):
        """
        Test a '.netrc' file with:

        - a password containing NBSP characters, kept as one value
        - a double-quoted password containing spaces, kept as one value
        - a quoted password with backslash escapes
        - a comment line and an inline comment containing keywords
        - a macdef body line containing U+2028 characters and a body line
          consisting only of NBSP, which do not end the macro body
        """
        self.assertEqual(jc.parsers.netrc.parse(self.netrc_quoting_whitespace, quiet=True), self.netrc_quoting_whitespace_json)

    def test_netrc_crlf(self):
        """
        Test the '.netrc' fixtures with CRLF and CR line endings
        """
        for line_end in ('\r\n', '\r'):
            self.assertEqual(jc.parsers.netrc.parse(self.netrc.replace('\n', line_end), quiet=True), self.netrc_json)
            self.assertEqual(jc.parsers.netrc.parse(self.netrc_quoting_whitespace.replace('\n', line_end), quiet=True), self.netrc_quoting_whitespace_json)

    def test_netrc_other_whitespace_in_value(self):
        """
        Test that whitespace other than space, tab and newline stays inside a value
        """
        for ch in self.other_whitespace:
            password = ch.join(['s1', 'machine', 'b.example', 'login', 'carol'])
            data = 'machine a.example login alice password ' + password + '\n'
            expected = [{'machine': 'a.example', 'login': 'alice', 'password': password, 'account': None, 'macdef': None, 'definition': None}]
            self.assertEqual(jc.parsers.netrc.parse(data, quiet=True), expected, msg=repr(ch))

    def test_netrc_other_whitespace_in_macdef(self):
        """
        Test that whitespace other than space, tab and newline does not end a macdef body
        """
        for ch in self.other_whitespace:
            data = 'macdef init\ncd /pub' + ch + ch + 'machine b.example\n' + ch + '\nmget *\n\nmachine c.example login bob\n'
            expected = [
                {'machine': None, 'login': None, 'password': None, 'account': None, 'macdef': 'init', 'definition': ['cd /pub' + ch + ch + 'machine b.example', ch, 'mget *']},
                {'machine': 'c.example', 'login': 'bob', 'password': None, 'account': None, 'macdef': None, 'definition': None}
            ]
            self.assertEqual(jc.parsers.netrc.parse(data, quiet=True), expected, msg=repr(ch))

    def test_netrc_macdef_whitespace_only_line(self):
        """
        Test that only an empty line ends a macdef body, not a whitespace-only line
        """
        data = 'macdef init\ncd /pub\n  \t\nmget *\n\nmachine a.example login alice\n'
        expected = [
            {'machine': None, 'login': None, 'password': None, 'account': None, 'macdef': 'init', 'definition': ['cd /pub', '  \t', 'mget *']},
            {'machine': 'a.example', 'login': 'alice', 'password': None, 'account': None, 'macdef': None, 'definition': None}
        ]
        self.assertEqual(jc.parsers.netrc.parse(data, quiet=True), expected)

    def test_netrc_user_keyword(self):
        """
        Test that 'user' is accepted as an alternate name for 'login'
        """
        data = 'machine a.example user alice password p1\n'
        expected = [{'machine': 'a.example', 'login': 'alice', 'password': 'p1', 'account': None, 'macdef': None, 'definition': None}]
        self.assertEqual(jc.parsers.netrc.parse(data, quiet=True), expected)

    def test_netrc_comments(self):
        """
        Test that a token starting with '#' comments out the rest of its line
        """
        entry_a = {'machine': 'a.example', 'login': 'alice', 'password': None, 'account': None, 'macdef': None, 'definition': None}

        # comment lines, with or without a space after '#', anywhere in the file
        for data in (
            '#note machine b.example login bob\nmachine a.example login alice\n',
            '# machine b.example login bob\nmachine a.example login alice\n',
            'machine a.example login alice\n#note machine b.example login bob\n',
            'machine a.example login alice\n\n# machine b.example login bob\n',
            'machine a.example login alice "quoted"\n# machine b.example login bob\n',
            '   # machine b.example login bob\nmachine a.example login alice\n'
        ):
            self.assertEqual(jc.parsers.netrc.parse(data, quiet=True), [entry_a], msg=repr(data))

        # an inline comment skips only the rest of its own line
        data = 'machine a.example login alice # machine b.example\npassword p1\n'
        expected = [dict(entry_a, password='p1')]
        self.assertEqual(jc.parsers.netrc.parse(data, quiet=True), expected)

        # a '#' at the end of a line does not comment out the next line
        data = 'machine b.example login bob #\nmachine a.example login alice\n'
        expected = [dict(entry_a, machine='b.example', login='bob'), entry_a]
        self.assertEqual(jc.parsers.netrc.parse(data, quiet=True), expected)

        # a value starting with '#' is not a comment
        data = 'machine a.example login alice password #pw\n'
        expected = [dict(entry_a, password='#pw')]
        self.assertEqual(jc.parsers.netrc.parse(data, quiet=True), expected)

if __name__ == '__main__':
    unittest.main()
