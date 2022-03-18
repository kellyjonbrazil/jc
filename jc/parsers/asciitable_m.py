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
from os import sep
import re
from typing import Iterable, List, Dict, Tuple, Optional, Union, Generator
import jc.utils
from jc.exceptions import ParseError
from jc.parsers.universal import sparse_table_parse


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
    # remove newlines from values
    # for item in proc_data:
    #     for k, v in item.items():
    #         item[k] = v.replace('\n', '')

    return proc_data


def _remove_ansi(string: str) -> str:
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', string)


def _lstrip(string: str) -> str:
    """find the leftmost non-whitespace character and lstrip to that index"""
    lstrip_list = [x for x in string.splitlines() if not len(x.strip()) == 0]
    start_points = (len(x) - len(x.lstrip()) for x in lstrip_list)
    min_point = min(start_points)
    new_lstrip_list = (x[min_point:] for x in lstrip_list)
    return '\n'.join(new_lstrip_list)


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


def _pretty_set_separators(table_lines: Iterable, separator: str) -> Generator[str, None, None]:
    """Return a generator that yields rows standardized separators"""
    for line in table_lines:
        strip_line = line.strip()

        # skip any blanks
        if not strip_line:
            continue

        # yield row separators as a sentinel string
        if   strip_line.startswith('╒═') and strip_line.endswith('═╕')\
          or strip_line.startswith('╞═') and strip_line.endswith('═╡')\
          or strip_line.startswith('╘═') and strip_line.endswith('═╛')\
          or strip_line.startswith('┌─') and strip_line.endswith('─┐')\
          or strip_line.startswith('├─') and strip_line.endswith('─┤')\
          or strip_line.startswith('└─') and strip_line.endswith('─┘')\
          or strip_line.startswith('+=') and strip_line.endswith('=+')\
          or strip_line.startswith('+-') and strip_line.endswith('-+'):
            yield separator
            continue

        # remove the table column separator characters and yield the line
        line = line.replace('|', ' ').replace('│', ' ')
        yield line


def _pretty_normalize_rows(table_lines: Iterable,
                           separator: str,
                           data_separator: str) -> Generator[str, None, None]:
    """
    Return a generator that yields header and data rows with different separators.
    Also removes spaces from headers.
    """
    header_found = False
    data_found = False

    # Removes initial table lines, finds the header row(s) and separates
    # the header from the data rows with different separator characters.
    for i in table_lines:
        if separator in i and not header_found and not data_found:
            # top table frame
            continue
        if not separator in i and not header_found and not data_found:
            header_found = True
            # first header data found
            # remove spaces from header
            i = re.sub(r'\b \b', '_', i)
            yield i
            continue
        if not separator in i and header_found and not data_found:
            # subsequent header data found
            # remove spaces from header
            i = re.sub(r'\b \b', '_', i)
            yield i
            continue
        if separator in i and header_found and not data_found:
            data_found = True
            # table separator found - this is a header separator
            yield separator
            continue
        if not separator in i and header_found and data_found:
            # subsequent data row found
            yield i
            continue
        if separator in i and header_found and data_found:
            # table separator found - this is a data separator
            yield data_separator
            continue


def _pretty_remove_header_rows(table: List[Dict], sep: str, data_sep: str) -> List[Optional[Dict]]:
    """return a table with only data rows."""
    # create a new list of row objects with new key names
    data_obj_list: List[Optional[Dict]] = []
    sep_found = False
    data_sep_found = False
    for obj in table:
        #skip to data
        for v in obj.values():
            if not sep_found and not str(v).strip() == sep:
                continue
            if not sep_found and str(v).strip() == sep:
                sep_found = True
                continue
        # append data row objects or None for separators
        if sep_found:
            for k, v in obj.items():
                if str(v).strip() == data_sep:
                    data_sep_found = True
                    break
                else:
                    data_sep_found = False
            if data_sep_found:
                data_obj_list.append(None)
            else:
                data_obj_list.append(obj)

    # remove first item, which is a separator
    return data_obj_list[1:]


def _pretty_map_new_keynames(table: List[Dict], sep: str) -> Dict:
    """
    returns a dict of old keyname to new keyname mappings by consolidating
    multiline keynames from the input list of dictionaries.
    """
    # first get all header objects to find full keynames. Stop when data rows are found.
    header_obj_list = []
    sep_found = False
    for obj in table:
        for v in obj.values():
            if str(v).strip() == sep:
                sep_found = True
                break
        if sep_found:
            break
        header_obj_list.append(obj)

    if not header_obj_list:
        header_obj_list = [{key: None for key in table[0]}]

    # create an old-key to new-key name mapping dict
    new_keynames_dict = dict.fromkeys([key for key in header_obj_list[0]], '')
    for item in new_keynames_dict:
        new_keynames_dict[item] = item
    for obj in header_obj_list:
        for k, v in obj.items():
            if v:
                new_keynames_dict[k] = new_keynames_dict[k] + '_' + v

    # normalize keynames so they are lowercase, no spaces, and no redundat '_'s
    for k, v in new_keynames_dict.items():
        new_keynames_dict[k] = v.replace(' ', '_').lower()
        new_keynames_dict[k] = re.sub(r'__+', '_', v)

    return new_keynames_dict


def _pretty_rename_keys(table: List, new_keynames: Dict) -> List[Optional[Dict]]:
    """rename all of the keys in the table based on the new_keynames mapping"""
    renamed_key_table: List[Optional[Dict]] = []
    for item in table:
        if item:
            renamed_key_table.append({new_keynames[k]:v for k, v in item.items()})
        else:
            renamed_key_table.append(None)

    return renamed_key_table


def _pretty_consolidate_rows(table: List) -> List[Dict]:
    """go through all data objects and combine values between data separators"""
    consolidated_rows = []
    current_obj = dict.fromkeys([key for key in table[0]], '')
    for item in table:
        if not item:
            consolidated_rows.append(current_obj)
            current_obj = dict.fromkeys([key for key in table[0]], '')
            continue
        else:
            for k, v in item.items():
                if v:
                    if not current_obj[k]:
                        current_obj[k] = v
                    else:
                        current_obj[k] = current_obj[k] + '\n' + v

    return consolidated_rows


def _parse_pretty(string: str) -> List:
    string_lines = string.splitlines()
    sep = '~~~'
    data_sep = '==='
    separator = '  ' + sep + ' '
    data_separator = '  ' + data_sep + ' '

    clean_gen = _pretty_set_separators(string_lines, separator)
    normalized_gen = _pretty_normalize_rows(clean_gen, separator, data_separator)
    raw_table = sparse_table_parse(normalized_gen)
    new_keynames_dict = _pretty_map_new_keynames(raw_table, sep)
    data_table = _pretty_remove_header_rows(raw_table, sep, data_sep)
    table_with_renamed_keys = _pretty_rename_keys(data_table, new_keynames_dict)
    final_table = _pretty_consolidate_rows(table_with_renamed_keys)

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
        data = _lstrip(data)
        table_type = _table_sniff(data)

        if table_type == 'pretty':
            raw_output = _parse_pretty(data)
        elif table_type == 'markdown':
            raise ParseError('Only "pretty" tables supported with multiline. "markdown" table detected. Please try the "asciitable" parser.')
        else:
            raise ParseError('Only "pretty" tables supported with multiline. "simple" table detected. Please try the "asciitable" parser.')

    return raw_output if raw else _process(raw_output)
