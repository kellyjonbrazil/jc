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
    version = '1.0'
    description = '`.netrc` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version


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

    lines = data.splitlines()

    # flatten every line into (token, line_number) pairs so a macdef's
    # body (which is not tokenized) can pick up right after the line
    # its macro name token was on
    tokens: List = []
    for lineno, line in enumerate(lines):
        for tok in line.split():
            tokens.append((tok, lineno))

    if jc.utils.has_data(data):
        i = 0
        while i < len(tokens):
            tok, lineno = tokens[i]

            if tok in ('machine', 'default'):
                if entry is not None:
                    raw_output.append(entry)
                entry = _new_entry()

                if tok == 'machine' and i + 1 < len(tokens):
                    i += 1
                    entry['machine'] = tokens[i][0]
                else:
                    entry['machine'] = tok

                i += 1
                continue

            if tok == 'macdef':
                if entry is not None:
                    raw_output.append(entry)
                entry = _new_entry()

                macro_lineno = lineno
                if i + 1 < len(tokens):
                    i += 1
                    tok, macro_lineno = tokens[i]
                    entry['macdef'] = tok

                # the macro body is every raw line after the macro name's
                # line, up to (but not including) a blank line or EOF
                definition: List[str] = []
                body_lineno = macro_lineno + 1
                while body_lineno < len(lines) and lines[body_lineno].strip() != '':
                    definition.append(lines[body_lineno])
                    body_lineno += 1

                entry['definition'] = definition
                raw_output.append(entry)
                entry = None

                # skip past every token that was consumed as part of the
                # macro body so it isn't re-parsed as a keyword
                i += 1
                while i < len(tokens) and tokens[i][1] < body_lineno:
                    i += 1
                continue

            if tok in ('login', 'password', 'account') and entry is not None:
                if i + 1 < len(tokens):
                    i += 1
                    entry[tok] = tokens[i][0]

                i += 1
                continue

            # unrecognized token (e.g. a comment word) - ignore
            i += 1

        if entry is not None:
            raw_output.append(entry)

    return raw_output if raw else _process(raw_output)
