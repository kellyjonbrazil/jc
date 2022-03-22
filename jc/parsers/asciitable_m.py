"""jc - JSON Convert `asciitable-m` parser

This parser converts ASCII and Unicode text tables with multi-line rows.
Tables must have some sort of separator line between rows.

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

Usage (cli):

    $ cat table.txt | jc --asciitable-m

Usage (module):

    import jc
    result = jc.parse('asciitable_m', asciitable-string)

Schema:

    [
      {
        "asciitable-m":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ asciitable-m | jc --asciitable-m -p
    []

    $ asciitable-m | jc --asciitable-m -p -r
    []
"""
import re
from typing import Iterable, Tuple, List, Dict
import jc.utils
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'multi-line ASCII and Unicode table parser'
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
    """find the rightmost non-whitespace character and rstrip to that index"""
    rstrip_list = [x for x in string.splitlines() if not len(x.strip()) == 0]
    end_points = (len(x.rstrip()) for x in rstrip_list)
    max_point = max(end_points)
    new_rstrip_list = ((x + ' ' * max_point)[:max_point] for x in rstrip_list)
    return '\n'.join(new_rstrip_list)


def _strip(string: str) -> str:
    string = _lstrip(string)
    string = _rstrip(string)
    return string

def _table_sniff(string: str) -> str:
    """Find the table-type via heuristics"""
    # pretty tables
    for line in string.splitlines():
        line = line.strip()
        if   line.startswith('╞═') and line.endswith('═╡')\
          or line.startswith('├─') and line.endswith('─┤')\
          or line.startswith('+=') and line.endswith('=+')\
          or line.startswith('+-') and line.endswith('-+'):
            return 'pretty'

    # markdown tables
    second_line = string.splitlines()[1]
    if second_line.startswith('|-') and second_line.endswith('-|'):
        return 'markdown'

    # simple tables
    return 'simple'


def _is_separator(line: str) -> bool:
    """Returns true if a table separator line is found"""
    strip_line = line.strip()
    if   strip_line.startswith('╒═') and strip_line.endswith('═╕')\
        or strip_line.startswith('╞═') and strip_line.endswith('═╡')\
        or strip_line.startswith('╘═') and strip_line.endswith('═╛')\
        or strip_line.startswith('┌─') and strip_line.endswith('─┐')\
        or strip_line.startswith('├─') and strip_line.endswith('─┤')\
        or strip_line.startswith('└─') and strip_line.endswith('─┘')\
        or strip_line.startswith('+=') and strip_line.endswith('=+')\
        or strip_line.startswith('+-') and strip_line.endswith('-+'):
        return True
    return False


def _snake_case(line: str) -> str:
    """replace spaces between words with an underscore and set to lowercase"""
    return re.sub(r'\b \b', '_', line).lower()


def _fixup_separators(line: str) -> str:
    """Normalize separators, and remove first and last separators"""
    # normalize separator
    line = line.replace('│', '|')

    # remove first separator if it is the first char in the line
    if line[0] == '|':
        line = line.replace('|', ' ', 1)

    # remove last separator if it is the last char in the line
    if line[-1] == '|':
        line = line[::-1].replace('|', ' ', 1)[::-1]

    return line


def _normalize_rows(table_lines: Iterable[str]) -> List[Tuple[int, List[str]]]:
    """
    Return a List of tuples of a row counters and data lines.
    """
    result = []
    header_found = False
    data_found = False
    row_counter = 0

    for line in table_lines:
        # skip blank lines
        if not line.strip():
            continue

        # skip top table frame
        if _is_separator(line) and not header_found and not data_found:
            continue

        # first header row found
        if not _is_separator(line) and not header_found and not data_found:
            header_found = True
            line = _snake_case(line)
            line = _fixup_separators(line)
            line_list =  line.split('|')
            line_list = [x.strip() for x in line_list]
            result.append((row_counter, line_list))
            continue

        # subsequent header row found
        if not _is_separator(line) and header_found and not data_found:
            line = _snake_case(line)
            line = _fixup_separators(line)
            line_list =  line.split('|')
            line_list = [x.strip() for x in line_list]
            result.append((row_counter, line_list))
            continue

        # table separator found - this is a header separator
        if _is_separator(line) and header_found and not data_found:
            data_found = True
            row_counter += 1
            continue

        # subsequent data row found
        if not _is_separator(line) and header_found and data_found:
            line = _fixup_separators(line)
            line_list =  line.split('|')
            line_list = [x.strip() for x in line_list]
            result.append((row_counter, line_list))
            continue

        # table separator found - this is a data separator
        if _is_separator(line) and header_found and data_found:
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
    result = table[0]
    for line in table[1:]:
        new_line: List[str] = []
        for i, header in enumerate(line):
            if header:
                new_header = result[i] + '_' + header
                new_header = re.sub(r'__+', '_', new_header)
                new_line.append(new_header)
            else:
                new_line.append(result[i])
        result = new_line

    return result


def _collapse_data(table: List[List[List[str]]]) -> List[List[str]]:
    """combine data rows to return a simple list of lists"""
    result: List[List[str]] = []

    for row in table:
        new_row: List[str] = []
        for line in row:
            if new_row:
                for i, item in enumerate(line):
                    new_row[i] = (new_row[i] + '\n' + item).strip()
            else:
                new_row = line

        result.append(new_row)

    return result


def _create_table_dict(header: List[str], data: List[List[str]]) -> List[Dict[str, str]]:
    return [dict(zip(header, r)) for r in data]


def _parse_pretty(string: str) -> List[Dict[str, str]]:
    string_lines: List[str] = string.splitlines()
    clean: List[Tuple[int, List[str]]] = _normalize_rows(string_lines)
    raw_headers: List[List[str]] = _get_headers(clean)
    raw_data: List[List[List[str]]] = _get_data(clean)

    new_headers: List[str] = _collapse_headers(raw_headers)
    new_data: List[List[str]] = _collapse_data(raw_data)
    final_table: List[Dict[str, str]] = _create_table_dict(new_headers, new_data)

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
        print(data.replace(' ', '~'))
        table_type = _table_sniff(data)

        if table_type == 'pretty':
            raw_output = _parse_pretty(data)
        elif table_type == 'markdown':
            raise ParseError('Only "pretty" tables supported with multiline. "markdown" table detected. Please try the "asciitable" parser.')
        else:
            raise ParseError('Only "pretty" tables supported with multiline. "simple" table detected. Please try the "asciitable" parser.')

    return raw_output if raw else _process(raw_output)
