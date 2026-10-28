r"""jc - JSON Convert `asciitable` parser

This parser converts ASCII and Unicode text tables with single-line rows.

Column headers must be at least two spaces apart from each other and must
be unique. For best results, column headers should be left-justified. If
column separators are present, then non-left-justified headers will be fixed
automatically.

Row separators are optional and are ignored. Each non-row-separator line is
considered a separate row in the table.

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

> Note: To preserve the case of the keys use the `-r` cli option or
> `raw=True` argument in `parse()`.

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
    version = '1.3'
    description = 'ASCII and Unicode table parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['generic', 'string']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    # normalize keys: convert to lowercase. Each distinct key is converted
    # once and the result is shared by all rows.
    lower_keys: Dict[str, str] = {}
    for item in proc_data:
        for key in item.copy():
            if key not in lower_keys:
                lower_keys[key] = key.lower()
            item[lower_keys[key]] = item.pop(key)

    return proc_data


# a complete CSI sequence (e.g. an SGR color code): parameter bytes and a
# final byte. `|` is not taken as the final byte so an incomplete sequence at
# the end of a cell does not remove the padding and separator after it.
_ansi_escape = re.compile(r'(?:\x9B|\x1B\[)[0-?]*[@-{}~]')

# characters that make up a row separator line
_separator_chars = frozenset('-=+|: \t' + ''.join(chr(c) for c in range(0x2500, 0x2580)))


def _remove_ansi(string: str) -> str:
    return _ansi_escape.sub('', string)


def _lstrip(string: str) -> str:
    """find the leftmost non-whitespace character and lstrip to that index"""
    lstrip_list = [x for x in jc.utils.splitlines(string) if not len(x.strip()) == 0]
    start_points = (len(x) - len(x.lstrip()) for x in lstrip_list)
    min_point = min(start_points)
    new_lstrip_list = (x[min_point:] for x in lstrip_list)
    return '\n'.join(new_lstrip_list)


def _rstrip(string: str) -> str:
    """find the rightmost non-whitespace character and rstrip to that index"""
    rstrip_list = [x for x in jc.utils.splitlines(string) if not len(x.strip()) == 0]
    end_points = (len(x.rstrip()) for x in rstrip_list)
    max_point = max(end_points)
    new_rstrip_list = (x[:max_point] for x in rstrip_list)
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

    # a data row can start and end like a separator (e.g. `--name  1  --`)
    if not _separator_chars.issuperset(strip_line):
        return False

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
    Replace spaces between words and special characters with an underscore.
    Ignore the replacement char (�) used for header padding.
    """
    line = re.sub(r'[^a-zA-Z0-9� ]', '_', line)  # special characters
    line = re.sub(r'\b \b', '_', line)           # spaces between words
    return line


_problem_header_pattern = re.compile(r'(?:\| )( +)([^|]+)')


def _normalize_rows(table: str) -> List[str]:
    """
    returns a List of row strings. Header is snake-cased
    """
    result: List[str] = []
    table_lines = jc.utils.splitlines(table)
    max_len = max([len(x) for x in table_lines]) if table_lines else 0
    for line in table_lines:
        # skip blank lines
        if not line.strip():
            continue

        # skip separators
        if _is_separator(line):
            continue

        # header or data row found - remove column separators
        if not result:  # this is the header row
            # pad the header to the table width. Data rows do not need to be
            # padded since sparse_table_parse handles short lines.
            line = line + ' ' * (max_len - len(line))

            # normalize the separator
            line = line.replace('│', '|')\
                       .replace('┃', '|')\
                       .replace('┆', '|')\
                       .replace('┇', '|')\
                       .replace('┊', '|')\
                       .replace('┋', '|')\
                       .replace('╎', '|')\
                       .replace('╏', '|')\
                       .replace('║', '|')

            # find the number of chars to pad in front of headers that are too
            # far away from the separator. Replace spaces with unicode char: �
            # we will remove this char from headers after sparse_table_parse
            # Each header is padded in place, in a single pass.
            line = _problem_header_pattern.sub(
                lambda m: '| ' + '\ufffd' * len(m.group(1)) + m.group(2),
                line
            )

            line = line.replace('|', ' ')
            result.append(_snake_case(line))
            continue

        # this is a data row
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

    return result


def _fixup_headers(table: List[Dict]) -> List[Dict]:
    """remove consecutive underscores and any trailing underscores"""
    new_table = []
    new_keys: Dict[str, str] = {}  # each distinct key is fixed once
    for row in table:
        new_row = row.copy()
        for k in row:
            if k not in new_keys:
                # remove replacement character
                k_new = k.replace('�', '')
                # remove consecutive underscores
                k_new = re.sub(r'__+', '_', k_new)
                # remove trailing underscores
                k_new = re.sub(r'_+$', '', k_new)
                new_keys[k] = k_new
            new_row[new_keys[k]] = new_row.pop(k)
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
