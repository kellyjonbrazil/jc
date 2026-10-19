r"""jc - JSON Convert `asciitable` parser

This parser converts ASCII and Unicode text tables with single-line rows.

Column headers must be at least two spaces apart from each other and must
be unique. For best results, column headers should be left-justified. If
column separators are present, then non-left-justified headers will be fixed
automatically.

Row separators are optional and are ignored. Each non-row-separator line is
considered a separate row in the table.

Tables without a header row are also supported. Since there are no headers to
detect, the column names must be supplied with the `columns` argument (Python
library) or the `JC_ASCIITABLE_COLS` environment variable (cli) as a
comma-separated list. When column names are supplied, every row in the input
is treated as a data row.

Values without a header row are split on two or more spaces. Use the
`separator` argument or the `JC_ASCIITABLE_SEPARATOR` environment variable to
split on an explicit string instead. This is useful for single-space,
comma, or tab separated data. Rows that contain more values than there are
column names keep only the first values that fit.

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

    or for tables without a header row:

    $ JC_ASCIITABLE_COLS='name,version' cat table.txt | jc --asciitable

Usage (module):

    import jc
    result = jc.parse('asciitable', asciitable_string)

    or for tables without a header row:

    result = jc.parse('asciitable', asciitable_string, columns=['name', 'version'])

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

    $ printf 'nginx 1.24.0\nredis 7.2.4\n' | JC_ASCIITABLE_COLS='name,version' \
    >   JC_ASCIITABLE_SEPARATOR=' ' jc --asciitable -p
    [
      {
        "name": "nginx",
        "version": "1.24.0"
      },
      {
        "name": "redis",
        "version": "7.2.4"
      }
    ]
"""
import os
import re
from functools import lru_cache
from typing import List, Dict, Optional, Union
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
    # normalize keys: convert to lowercase
    for item in proc_data:
        for key in item.copy():
            k_new = key.lower()
            item[k_new] = item.pop(key)

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
    Replace spaces between words and special characters with an underscore.
    Ignore the replacement char (�) used for header padding.
    """
    line = re.sub(r'[^a-zA-Z0-9� ]', '_', line)  # special characters
    line = re.sub(r'\b \b', '_', line)           # spaces between words
    return line


def _normalize_rows(table: str) -> List[str]:
    """
    returns a List of row strings. Header is snake-cased
    """
    result: List[str] = []
    for line in table.splitlines():
        # skip blank lines
        if not line.strip():
            continue

        # skip separators
        if _is_separator(line):
            continue

        # header or data row found - remove column separators
        if not result:  # this is the header row
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
            problem_header_pattern = re.compile(r'(?:\| )( +)([^|]+)')
            problem_headers = problem_header_pattern.findall(line)
            if problem_headers:
                for p_header in problem_headers:
                    old_header = p_header[0] + p_header[1]
                    sub_chars = '�' * len(p_header[0])
                    new_header = sub_chars + p_header[1]
                    line = line.replace(old_header, new_header)

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


def _fixup_header_name(name: str) -> str:
    """remove the replacement char, consecutive underscores, and trailing underscores"""
    name = name.replace('�', '')
    # remove consecutive underscores
    name = re.sub(r'__+', '_', name)
    # remove trailing underscores
    name = re.sub(r'_+$', '', name)
    return name


def _fixup_headers(table: List[Dict]) -> List[Dict]:
    """remove consecutive underscores and any trailing underscores"""
    new_table = []
    for row in table:
        new_row = row.copy()
        for k in row:
            new_row[_fixup_header_name(k)] = new_row.pop(k)
        new_table.append(new_row)

    return new_table


def _columns_from_env() -> List[str]:
    """get the header names from the JC_ASCIITABLE_COLS environment variable"""
    columns = os.environ.get('JC_ASCIITABLE_COLS', '')
    return [column.strip() for column in columns.split(',') if column.strip()]


def _split_row(line: str, separator: Optional[str]) -> List[str]:
    """split a headerless row into stripped values"""
    if separator:
        values = line.split(separator)
        # ignore a leading and trailing separator (e.g. the outer pipes of a
        # Markdown table)
        if values and not values[0].strip():
            values = values[1:]
        if values and not values[-1].strip():
            values = values[:-1]
        return [value.strip() for value in values]

    return [value.strip() for value in re.split(r'\s{2,}', line.strip())]


def _parse_headerless(data: str, columns: List[str], separator: Optional[str]) -> List[Dict]:
    """
    Create the table for input that has no header row. Every non-blank and
    non-separator line is a data row. Missing values are set to None.
    """
    result: List[Dict] = []

    for line in data.splitlines():
        # skip blank lines
        if not line.strip():
            continue

        # skip separators
        if _is_separator(line):
            continue

        values = _split_row(line, separator)
        row: Dict[str, Optional[str]] = {}
        for index, column in enumerate(columns):
            value = values[index] if index < len(values) else ''
            row[column] = value if value else None

        result.append(row)

    return result


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False,
    columns: Optional[Union[List[str], str]] = None,
    separator: Optional[str] = None
) -> List[Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True
        columns:     (list)    header names for tables without a header row.
                               A comma-separated string is also accepted.
                               Overrides the JC_ASCIITABLE_COLS environment
                               variable.
        separator:   (string)  value separator for tables without a header
                               row. Default is two or more spaces. Overrides
                               the JC_ASCIITABLE_SEPARATOR environment
                               variable.

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List = []

    if jc.utils.has_data(data):
        data = _remove_ansi(data)
        data = _strip(data)

        column_names = columns if columns else _columns_from_env()
        if isinstance(column_names, str):
            column_names = [column.strip() for column in column_names.split(',') if column.strip()]
        if column_names:
            separator = separator if separator is not None else os.environ.get('JC_ASCIITABLE_SEPARATOR')
            headers = [_fixup_header_name(_snake_case(column.strip())) for column in column_names]
            raw_output = _parse_headerless(data, headers, separator)
        else:
            data_list = _normalize_rows(data)
            raw_table = sparse_table_parse(data_list)
            raw_output = _fixup_headers(raw_table)

    return raw_output if raw else _process(raw_output)
