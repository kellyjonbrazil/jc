r"""jc - JSON Convert `asciitable-m` parser

This parser converts various styles of ASCII and Unicode text tables with
multi-line rows. Tables must have a header row and separator line between
rows.

For example:

    ╒══════════╤═════════╤════════╕
    │ foo      │ bar baz │ fiz    │
    │          │         │ buz    │
    ╞══════════╪═════════╪════════╡
    │ good day │ 12345   │        │
    │ mate     │         │        │
    ├──────────┼─────────┼────────┤
    │ hi there │ abc def │ 3.14   │
    │          │         │        │
    ╘══════════╧═════════╧════════╛

Cells with multiple lines within rows will be joined with a newline
character ('\\n').

Headers (keys) are converted to snake-case and newlines between multi-line
headers are joined with an underscore. All values are returned as strings,
except empty strings, which are converted to None/null.

> Note: To preserve the case of the keys use the `-r` cli option or
> `raw=True` argument in `parse()`.

> Note: table column separator characters (e.g. `|`) cannot be present
> inside the cell data. If detected, a warning message will be printed to
> `STDERR` and the line will be skipped. The warning message can be
> suppressed by using the `-q` command option or by setting `quiet=True` in
> `parse()`.

Usage (cli):

    $ cat table.txt | jc --asciitable-m

Usage (module):

    import jc
    result = jc.parse('asciitable_m', asciitable-string)

Schema:

    [
      {
        "column_name1":     string,    # empty string is null
        "column_name2":     string     # empty string is null
      }
    ]

Examples:

    $ echo '
    > +----------+---------+--------+
    > | foo      | bar     | baz    |
    > |          |         | buz    |
    > +==========+=========+========+
    > | good day | 12345   |        |
    > | mate     |         |        |
    > +----------+---------+--------+
    > | hi there | abc def | 3.14   |
    > |          |         |        |
    > +==========+=========+========+' | jc --asciitable-m -p
    [
      {
        "foo": "good day\\nmate",
        "bar": "12345",
        "baz_buz": null
      },
      {
        "foo": "hi there",
        "bar": "abc def",
        "baz_buz": "3.14"
      }
    ]

    $ echo '
    > ╒══════════╤═════════╤════════╕
    > │ foo      │ bar     │ baz    │
    > │          │         │ buz    │
    > ╞══════════╪═════════╪════════╡
    > │ good day │ 12345   │        │
    > │ mate     │         │        │
    > ├──────────┼─────────┼────────┤
    > │ hi there │ abc def │ 3.14   │
    > │          │         │        │
    > ╘══════════╧═════════╧════════╛' | jc --asciitable-m -p
    [
      {
        "foo": "good day\\nmate",
        "bar": "12345",
        "baz_buz": null
      },
      {
        "foo": "hi there",
        "bar": "abc def",
        "baz_buz": "3.14"
      }
    ]
"""
import re
from functools import lru_cache
from typing import Iterable, Tuple, List, Dict, Optional
import jc.utils
from jc.parsers.universal import _char_width
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = 'multi-line ASCII and Unicode table parser'
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

# characters a right table border or frame ends with
_RIGHT_EDGE_CHARS = frozenset('+|' + ''.join(chr(c) for c in range(0x2500, 0x2580)))


def _remove_ansi(string: str) -> str:
    return _ansi_escape.sub('', string)


def _lstrip(string: str) -> str:
    """find the leftmost non-whitespace character and lstrip to that index"""
    lstrip_list = [x for x in jc.utils.splitlines(string) if not len(x.strip()) == 0]
    start_points = (len(x) - len(x.lstrip()) for x in lstrip_list)
    min_point = min(start_points)
    new_lstrip_list = (x[min_point:] for x in lstrip_list)
    return '\n'.join(new_lstrip_list)


def _display_width(string: str) -> int:
    """number of terminal cells a string fills"""
    return sum(1 if c < '\x80' else _char_width(c) for c in string)


def _cut_cells(string: str, cells: int) -> str:
    """return the leading characters of a string that fit in the given cells"""
    used = 0
    for i, char in enumerate(string):
        used += 1 if char < '\x80' else _char_width(char)
        if used > cells:
            return string[:i]

    return string


def _rstrip(string: str) -> str:
    """
    Remove the padding after the right edge of the table. If the table has a
    right border (decided once for the whole table) the border is the last
    character of every line. Otherwise find the rightmost
    non-whitespace cell and rstrip to that cell. Lines shorter than that cell
    get one trailing space so they still end in whitespace, the same as if
    they were padded to the full width. Widths are display widths, so wide
    characters count as two cells.
    """
    rstrip_list = [x for x in jc.utils.splitlines(string) if not len(x.strip()) == 0]

    # a table has a right border if its first line ends with one and every
    # line ends at the same place, measured in cells or in characters
    first = rstrip_list[0].rstrip()
    if first[-1] in _RIGHT_EDGE_CHARS:
        first_width = _display_width(first)
        if all(
            len(x.rstrip()) == len(first) or _display_width(x.rstrip()) == first_width
            for x in rstrip_list
        ):
            return '\n'.join(x.rstrip() for x in rstrip_list)

    max_point = max(_display_width(x.rstrip()) for x in rstrip_list)
    new_rstrip_list = (
        _cut_cells(x, max_point) if _display_width(x) >= max_point else x + ' '
        for x in rstrip_list
    )
    return '\n'.join(new_rstrip_list)


def _strip(string: str) -> str:
    string = _lstrip(string)
    string = _rstrip(string)
    return string


def _table_sniff(string: str) -> str:
    """find the table-type via heuristics"""
    # pretty tables
    for line in jc.utils.splitlines(string):
        line = line.strip()
        if any((
            line.startswith('╞') and line.endswith('╡'),
            line.startswith('├') and line.endswith('┤'),
            line.startswith('┡') and line.endswith('┩'),
            line.startswith('┣') and line.endswith('┫'),
            line.startswith('┢') and line.endswith('┪'),
            line.startswith('┟') and line.endswith('┧'),
            line.startswith('┞') and line.endswith('┦'),
            line.startswith('┠') and line.endswith('┨'),
            line.startswith('┝') and line.endswith('┥'),
            line.startswith('╟') and line.endswith('╢'),
            line.startswith('╠') and line.endswith('╣'),
            line.startswith('+=') and line.endswith('=+'),
            line.startswith('+-') and line.endswith('-+')
        )):
            return 'pretty'

    # markdown tables
    second_line = jc.utils.splitlines(string)[1]
    if second_line.startswith('|-') and second_line.endswith('-|'):
        return 'markdown'

    # simple tables
    return 'simple'

@lru_cache(maxsize=32)
def _is_separator(line: str) -> bool:
    """returns true if a table separator line is found"""
    # This function is cacheable since tables have identical separators
    strip_line = line.strip()

    # a data row can start and end like a separator (e.g. `--name  1  --`)
    if not _separator_chars.issuperset(strip_line):
        return False

    if any((
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
        strip_line.startswith('╰') and strip_line.endswith('╯'),
        strip_line.startswith('+=') and strip_line.endswith('=+'),
        strip_line.startswith('+-') and strip_line.endswith('-+')
    )):
        return True
    return False


def _snake_case(line: str) -> str:
    """
    replace spaces between words and special characters with an underscore.
    """
    # must include all column separator characters in regex
    line = re.sub(r'[^a-zA-Z0-9 |│┃┆┇┊┋╎╏║]', '_', line)
    return re.sub(r'\b \b', '_', line)


def _fixup_separators(line: str) -> str:
    """normalize separators, and remove first and last separators"""
    # normalize separator
    line = line.replace('│', '|')\
               .replace('┃', '|')\
               .replace('┆', '|')\
               .replace('┇', '|')\
               .replace('┊', '|')\
               .replace('┋', '|')\
               .replace('╎', '|')\
               .replace('╏', '|')\
               .replace('║', '|')

    # remove first separator if it is the first char in the line
    if line[0] == '|':
        line = line.replace('|', ' ', 1)

    # remove last separator if it is the last char in the line
    if line[-1] == '|':
        line = line[::-1].replace('|', ' ', 1)[::-1]

    return line


def _normalize_rows(table_lines: Iterable[str]) -> List[Tuple[int, List[str]]]:
    """return a List of tuples of row-counters and data lines."""
    result = []
    header_found = False
    data_found = False
    row_counter = 0

    for line in table_lines:
        # skip blank lines
        if not line.strip():
            continue

        # skip top table frame
        if not header_found and not data_found and _is_separator(line):
            continue

        # first header row found
        if not header_found and not data_found and not _is_separator(line):
            header_found = True
            line = _snake_case(line)
            line = _fixup_separators(line)
            line_list =  line.split('|')
            line_list = [x.strip() for x in line_list]
            result.append((row_counter, line_list))
            continue

        # subsequent header row found
        if header_found and not data_found and not _is_separator(line):
            line = _snake_case(line)
            line = _fixup_separators(line)
            line_list =  line.split('|')
            line_list = [x.strip() for x in line_list]
            result.append((row_counter, line_list))
            continue

        # table separator found - this is a header separator
        if header_found and not data_found and _is_separator(line):
            data_found = True
            row_counter += 1
            continue

        # data row found
        if header_found and data_found and not _is_separator(line):
            line = _fixup_separators(line)
            line_list =  line.split('|')
            line_list = [x.strip() for x in line_list]
            result.append((row_counter, line_list))
            continue

        # table separator found - this is a data separator
        if header_found and data_found and _is_separator(line):
            row_counter += 1
            continue

    return result


def _get_headers(table: Iterable[Tuple[int, List]]) -> List[List[str]]:
    """
    return a list of all of the header rows (which are lists of strings.
        [                            # headers
            ['str', 'str', 'str'],   # header rows
            ['str', 'str', 'str']
        ]
    """
    result = []
    for row_num, line in table:
        if row_num == 0:
            result.append(line)
    return result


def _get_data(table: Iterable[Tuple[int, List]]) -> List[List[List[str]]]:
    """
    return a list of rows, which are lists made up of lists of strings:
        [                                # data
            [                            # data rows
                ['str', 'str', 'str'],   # data lines
                ['str', 'str', 'str']
            ]
        ]
    """
    result: List[List[List[str]]] = []
    current_row = 1
    this_line: List[List[str]] = []
    for row_num, line in table:
        if row_num != 0:
            if row_num != current_row:
                result.append(this_line)
                current_row = row_num
                this_line = []

            this_line.append(line)

    if this_line:
        result.append(this_line)

    return result


def _collapse_headers(table: List[List[str]]) -> List[str]:
    """append each column string to return the full header list"""
    first = table[0]
    # parts for each column; the width follows the most recent header line
    parts: List[List[str]] = [[h] for h in first]
    changed: List[bool] = [False] * len(first)

    for line in table[1:]:
        if len(line) > len(parts):
            raise IndexError('list index out of range')

        parts = parts[:len(line)]
        changed = changed[:len(line)]
        for i, header in enumerate(line):
            if header:
                parts[i].append(header)
                changed[i] = True

    result: List[str] = []
    for i, col in enumerate(parts):
        if changed[i]:
            # remove consecutive underscores
            result.append(re.sub(r'__+', '_', '_'.join(col)))
        else:
            result.append(col[0])

    return result


def _collapse_data(table: List[List[List[str]]], quiet=False) -> List[List[str]]:
    """combine data rows to return a simple list of lists"""
    result: List[List[str]] = []

    for index, row in enumerate(table):
        first_line = row[0]
        width = len(first_line)
        cols: List[List[str]] = [[item] if item else [] for item in first_line]
        failed = False

        for line in row[1:]:
            for i, item in enumerate(line):
                if i >= width:
                    failed = True
                    break
                if item:
                    cols[i].append(item)
            if failed:
                break

        # empty items are dropped so each cell is joined only once
        new_row = ['\n'.join(c) for c in cols]

        if not failed:
            result.append(new_row)
        else:
            if not quiet:
                row[0] = new_row
                row_string = '\n'.join([' | '.join(l) for l in row])
                jc.utils.warning_message(
                    [f'Possible table separator character found in row {index}:  {row_string}. Skipping.']
                )

    return result


def _create_table_dict(header: List[str], data: List[List[str]]) -> List[Dict[str, Optional[str]]]:
    """
    zip the headers and data to create a list of dictionaries. Also convert
    empty strings to None.
    """
    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data]
    for row in table_list_dict:
        for k, v in row.items():
            if v == '':
                row[k] = None

    return table_list_dict


def _parse_pretty(string: str, quiet: bool =False) -> List[Dict[str, Optional[str]]]:
    string_lines: List[str] = jc.utils.splitlines(string)
    clean: List[Tuple[int, List[str]]] = _normalize_rows(string_lines)
    raw_headers: List[List[str]] = _get_headers(clean)
    raw_data: List[List[List[str]]] = _get_data(clean)

    new_headers: List[str] = _collapse_headers(raw_headers)
    new_data: List[List[str]] = _collapse_data(raw_data, quiet)
    final_table: List[Dict[str, Optional[str]]] = _create_table_dict(new_headers, new_data)

    return final_table


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
    table_type = 'unknown'

    if jc.utils.has_data(data):
        data = _remove_ansi(data)
        data = _strip(data)
        table_type = _table_sniff(data)

        if table_type == 'pretty':
            raw_output = _parse_pretty(data, quiet)
        elif table_type == 'markdown':
            raise ParseError('Only "pretty" tables supported with multiline. "markdown" table detected. Please try the "asciitable" parser.')
        else:
            raise ParseError('Only "pretty" tables supported with multiline. "simple" table detected. Please try the "asciitable" parser.')

    return raw_output if raw else _process(raw_output)
