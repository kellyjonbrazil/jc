r"""jc - JSON Convert `.netrc` file parser

This parser will work with `.netrc` and `_netrc` files used by `curl`,
`ftp`, and other tools to store login credentials for remote machines.

`machine`/`default` blocks and `macdef` (macro) blocks are both returned
as items in the same list. Since the two block types don't share fields,
unused fields are set to `null`.

Usage (cli):

    $ cat ~/.netrc | jc --netrc

Usage (module):

    import jc
    result = jc.parse('netrc', netrc_file_output)

Schema:

    [
      {
        "machine":                   string,
        "login":                     string,
        "password":                  string,
        "account":                   string,
        "macdef":                    string,
        "definition": [
                                     string
        ]
      }
    ]

Examples:

    $ cat ~/.netrc | jc --netrc -p
    [
      {
        "machine": "mail.example.com",
        "login": "jdoe",
        "password": "secret123",
        "account": null,
        "macdef": null,
        "definition": null
      },
      {
        "machine": "default",
        "login": "anonymous",
        "password": "user@example.com",
        "account": null,
        "macdef": null,
        "definition": null
      },
      {
        "machine": null,
        "login": null,
        "password": null,
        "account": null,
        "macdef": "init",
        "definition": [
          "cd /pub",
          "mget *"
        ]
      }
    ]
"""
from typing import List, Dict, Optional
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`.netrc` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version

_SEPARATORS = ' \t\n'


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return proc_data


def _new_entry() -> Dict:
    return {
        'machine': None,
        'login': None,
        'password': None,
        'account': None,
        'macdef': None,
        'definition': None
    }


class _Lexer():
    """
    Tokenizer that follows Python's netrc module: tokens are separated by
    space, tab and newline only, double quotes group a token (which may
    contain separators), and a backslash escapes the next character.
    """
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.lineno = 0
        self.token_end_lineno = 0
        self.line_starts = [0] + [i + 1 for i, ch in enumerate(text) if ch == '\n']

    def _read_char(self) -> str:
        if self.pos >= len(self.text):
            return ''
        ch = self.text[self.pos]
        self.pos += 1
        if ch == '\n':
            self.lineno += 1
        return ch

    def _add_char(self, token: List[str], ch: str) -> None:
        if ch == '\\':
            ch = self._read_char()
        token.append(ch)
        self.token_end_lineno = self.lineno

    def get_token(self) -> Optional[str]:
        """Return the next token or None at the end of the input"""
        ch = self._read_char()
        while ch != '' and ch in _SEPARATORS:
            ch = self._read_char()

        if ch == '':
            return None

        token: List[str] = []
        if ch == '"':
            ch = self._read_char()
            while ch not in ('', '"'):
                self._add_char(token, ch)
                ch = self._read_char()
            self.token_end_lineno = self.lineno
            return ''.join(token)

        while ch != '' and ch not in _SEPARATORS:
            self._add_char(token, ch)
            ch = self._read_char()
        return ''.join(token)

    def skip_line(self) -> None:
        """Skip the rest of the current line"""
        self.goto_line(self.lineno + 1)

    def goto_line(self, lineno: int) -> None:
        """Move to the start of a line (or to the end of the input)"""
        if lineno < len(self.line_starts):
            self.pos = self.line_starts[lineno]
            self.lineno = lineno
        else:
            self.pos = len(self.text)
            self.lineno = len(self.line_starts) - 1


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[Dict] = []
    entry: Optional[Dict] = None

    if jc.utils.has_data(data):
        lines = jc.utils.splitlines(data, split_cr=True)
        lexer = _Lexer('\n'.join(lines) + '\n')

        while True:
            tok = lexer.get_token()
            if tok is None:
                break

            # a token starting with '#' comments out the rest of its line.
            # If the newline after the token was already read, the line is done.
            if tok.startswith('#'):
                if lexer.lineno == lexer.token_end_lineno:
                    lexer.skip_line()
                continue

            if tok in ('machine', 'default'):
                if entry is not None:
                    raw_output.append(entry)
                entry = _new_entry()

                if tok == 'machine':
                    name = lexer.get_token()
                    entry['machine'] = tok if name is None else name
                else:
                    entry['machine'] = tok

                continue

            if tok == 'macdef':
                if entry is not None:
                    raw_output.append(entry)
                entry = _new_entry()

                # the macro body is every raw line after the macro name's
                # line, up to (but not including) an empty line or EOF
                body_lineno = lexer.token_end_lineno + 1
                name = lexer.get_token()
                if name is not None:
                    entry['macdef'] = name
                    body_lineno = lexer.token_end_lineno + 1

                definition: List[str] = []
                while body_lineno < len(lines) and lines[body_lineno] != '':
                    definition.append(lines[body_lineno])
                    body_lineno += 1

                entry['definition'] = definition
                raw_output.append(entry)
                entry = None
                lexer.goto_line(body_lineno)
                continue

            # 'user' is an alternate name for 'login'
            if tok in ('login', 'user', 'password', 'account') and entry is not None:
                value = lexer.get_token()
                if value is not None:
                    entry['login' if tok == 'user' else tok] = value
                continue

            # unrecognized token - ignore

        if entry is not None:
            raw_output.append(entry)

    return raw_output if raw else _process(raw_output)
