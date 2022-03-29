"""jc - JSON Convert `asciitable` parser

This parser converts ASCII and Unicode text tables with single-line rows.

Column headers must be at least two spaces apart from each other and must
be unique.

For example:

    ╒══════════╤═════════╤════════╕
    │ foo      │ bar     │ baz    │
    ╞══════════╪═════════╪════════╡
    │ good day │         │ 12345  │
    ├──────────┼─────────┼────────┤
    │ hi there │ abc def │ 3.14   │
    ╘══════════╧═════════╧════════╛

or

    +-----------------------------+
    | foo        bar       baz    |
    +-----------------------------+
    | good day             12345  |
    | hi there   abc def   3.14   |
    +-----------------------------+

or

    | foo      | bar     | baz    |
    |----------|---------|--------|
    | good day |         | 12345  |
    | hi there | abc def | 3.14   |

or

    foo        bar       baz
    ---------  --------  ------
    good day             12345
    hi there   abc def   3.14

or

    foo        bar       baz
    good day             12345
    hi there   abc def   3.14

etc...

Headers (keys) are converted to snake-case. All values are returned as
strings, except empty strings, which are converted to None/null.

Usage (cli):

    $ cat table.txt | jc --asciitable

Usage (module):

    import jc
    result = jc.parse('asciitable', asciitable_string)

Schema:

    [
      {
        "column_name1":     string,    # empty string is null
        "column_name2":     string     # empty string is null
      }
    ]

Examples:

    $ echo '
    >     ╒══════════╤═════════╤════════╕
    >     │ foo      │ bar     │ baz    │
    >     ╞══════════╪═════════╪════════╡
    >     │ good day │         │ 12345  │
    >     ├──────────┼─────────┼────────┤
    >     │ hi there │ abc def │ 3.14   │
    >     ╘══════════╧═════════╧════════╛' | jc --asciitable -p
    [
      {
        "foo": "good day",
        "bar": null,
        "baz": "12345"
      },
      {
        "foo": "hi there",
        "bar": "abc def",
        "baz": "3.14"
      }
    ]

    $ echo '
    >     foo        bar       baz
    >     ---------  --------  ------
    >     good day             12345
    >     hi there   abc def   3.14'  | jc --asciitable -p
    [
      {
        "foo": "good day",
        "bar": null,
        "baz": "12345"
      },
      {
        "foo": "hi there",
        "bar": "abc def",
        "baz": "3.14"
      }
    ]
"""
import re
from functools import lru_cache
from typing import List, Dict
import jc.utils
from jc.parsers.universal import sparse_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'ASCII and Unicode table parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return proc_data


def _remove_ansi(string: str) -> str:
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', string)


def _lstrip(string: str) -> str:
    """find the leftmost non-whitespace character and lstrip to that index"""
    lstrip_list = [x for x in string.splitlines() if not len(x.strip()) == 0]
    start_points = (len(x) - len(x.lstrip()) for x in lstrip_list)
    min_point = min(start_points)
    new_lstrip_list = (x[min_point:] for x in lstrip_list)
    return '\n'.join(new_lstrip_list)


def _rstrip(string: str) -> str:
    """find the rightmost non-whitespace character and rstrip and pad to that index"""
    rstrip_list = [x for x in string.splitlines() if not len(x.strip()) == 0]
    end_points = (len(x.rstrip()) for x in rstrip_list)
    max_point = max(end_points)
    new_rstrip_list = ((x + ' ' * max_point)[:max_point] for x in rstrip_list)
    return '\n'.join(new_rstrip_list)


def _strip(string: str) -> str:
    string = _lstrip(string)
    string = _rstrip(string)
    return string

@lru_cache(maxsize=32)
def _is_separator(line: str) -> bool:
    """returns true if a table separator line is found"""
    # This function is cacheable since tables have identical separators
    strip_line = line.strip()
    if any((
        strip_line.startswith('|-') and strip_line.endswith('-|'),
        strip_line.startswith('━━') and strip_line.endswith('━━'),
        strip_line.startswith('──') and strip_line.endswith('──'),
        strip_line.startswith('┄┄') and strip_line.endswith('┄┄'),
        strip_line.startswith('┅┅') and strip_line.endswith('┅┅'),
        strip_line.startswith('┈┈') and strip_line.endswith('┈┈'),
        strip_line.startswith('┉┉') and strip_line.endswith('┉┉'),
        strip_line.startswith('══') and strip_line.endswith('══'),
        strip_line.startswith('--') and strip_line.endswith('--'),
        strip_line.startswith('==') and strip_line.endswith('=='),
        strip_line.startswith('+=') and strip_line.endswith('=+'),
        strip_line.startswith('+-') and strip_line.endswith('-+'),
        strip_line.startswith('╒') and strip_line.endswith('╕'),
        strip_line.startswith('╞') and strip_line.endswith('╡'),
        strip_line.startswith('╘') and strip_line.endswith('╛'),
        strip_line.startswith('┏') and strip_line.endswith('┓'),
        strip_line.startswith('┣') and strip_line.endswith('┫'),
        strip_line.startswith('┗') and strip_line.endswith('┛'),
        strip_line.startswith('┡') and strip_line.endswith('┩'),
        strip_line.startswith('┢') and strip_line.endswith('┪'),
        strip_line.startswith('┟') and strip_line.endswith('┧'),
        strip_line.startswith('┞') and strip_line.endswith('┦'),
        strip_line.startswith('┠') and strip_line.endswith('┨'),
        strip_line.startswith('┝') and strip_line.endswith('┥'),
        strip_line.startswith('┍') and strip_line.endswith('┑'),
        strip_line.startswith('┕') and strip_line.endswith('┙'),
        strip_line.startswith('┎') and strip_line.endswith('┒'),
        strip_line.startswith('┖') and strip_line.endswith('┚'),
        strip_line.startswith('╓') and strip_line.endswith('╖'),
        strip_line.startswith('╟') and strip_line.endswith('╢'),
        strip_line.startswith('╙') and strip_line.endswith('╜'),
        strip_line.startswith('╔') and strip_line.endswith('╗'),
        strip_line.startswith('╠') and strip_line.endswith('╣'),
        strip_line.startswith('╚') and strip_line.endswith('╝'),
        strip_line.startswith('┌') and strip_line.endswith('┐'),
        strip_line.startswith('├') and strip_line.endswith('┤'),
        strip_line.startswith('└') and strip_line.endswith('┘'),
        strip_line.startswith('╭') and strip_line.endswith('╮'),
        strip_line.startswith('╰') and strip_line.endswith('╯')
    )):
        return True
    return False


def _snake_case(line: str) -> str:
    """
    replace spaces between words and special characters with an underscore
    and set to lowercase
    """
    line = re.sub(r'[^a-zA-Z0-9 ]', '_', line)
    return re.sub(r'\b \b', '_', line).lower()


def _normalize_rows(table: str) -> List[str]:
    """
    returns a List of row strings. Header is snake-cased
    """
    result = []
    for line in table.splitlines():
        # skip blank lines
        if not line.strip():
            continue

        # skip separators
        if _is_separator(line):
            continue

        # data row - remove column separators
        line = line.replace('|', ' ')\
                   .replace('│', ' ')\
                   .replace('┃', ' ')\
                   .replace('┆', ' ')\
                   .replace('┇', ' ')\
                   .replace('┊', ' ')\
                   .replace('┋', ' ')\
                   .replace('╎', ' ')\
                   .replace('╏', ' ')\
                   .replace('║', ' ')
        result.append(line)

    result[0] = _snake_case(result[0])
    return result


def _fixup_headers(table: List[Dict]) -> List[Dict]:
    """remove consecutive underscores and any trailing underscores"""
    new_table = []
    for row in table:
        new_row = row.copy()
        for k in row:
            k_new = k
            # remove consecutive underscores
            k_new = re.sub(r'__+', '_', k_new)
            # remove trailing underscores
            k_new = re.sub(r'_+$', '', k_new)
            new_row[k_new] = new_row.pop(k)
        new_table.append(new_row)

    return new_table


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []

    if jc.utils.has_data(data):
        data = _remove_ansi(data)
        data = _strip(data)
        data_list = _normalize_rows(data)
        raw_table = sparse_table_parse(data_list)
        raw_output = _fixup_headers(raw_table)

    return raw_output if raw else _process(raw_output)
