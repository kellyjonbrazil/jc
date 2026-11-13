r"""jc - JSON Convert universal parsers"""
import re
import unicodedata
from functools import lru_cache
from typing import Iterable, List, Dict


_NON_ASCII = re.compile('[^\x00-\x7f]')


@lru_cache(maxsize=4096)
def _char_width(char: str) -> int:
    """Number of terminal cells a character fills."""
    if unicodedata.combining(char) or unicodedata.category(char) == 'Cf':
        return 0

    if unicodedata.east_asian_width(char) in ('W', 'F'):
        return 2

    return 1


def _cell_starts(text: str) -> List[int]:
    """Return the display cell at the start of each character of text."""
    cell_at_char: List[int] = []
    cell = 0
    for char in text:
        cell_at_char.append(cell)
        cell += 1 if char < '\x80' else _char_width(char)

    return cell_at_char


def _cell_chars(text: str) -> List[int]:
    """Return the character index at each display cell of text."""
    char_at_cell: List[int] = []
    for i, char in enumerate(text):
        if char < '\x80':
            char_at_cell.append(i)
        else:
            char_at_cell.extend([i] * _char_width(char))

    return char_at_cell


def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via jc.utils.splitlines(). Item 0 must be the
                         header row. Any spaces in header names should be
                         changed to underscore '_'. You should also ensure
                         headers are lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output


def sparse_table_parse(data: Iterable[str], delim: str = '\u2063') -> List[Dict]:
    """
    Parse tables with missing column data or with spaces in column data.
    Blank cells are converted to None in the resulting dictionary. Data
    elements must line up within column boundaries.

    Column positions are measured in display cells: East Asian wide and
    fullwidth characters count as two cells, combining characters and
    zero-width format characters count as zero cells, and all other
    characters count as one cell.

    Example Table:

        col_1        col_2     col_3     col_4         col_5
        apple        orange              fuzzy peach   my favorite fruits
        green beans            celery    spinach       my favorite veggies
        chicken      beef                brown eggs    my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': None, 'col_4':
        'fuzzy peach', 'col_5': 'my favorite fruits'}, {'col_1':
        'green beans', 'col_2': None, 'col_3': 'celery', 'col_4': 'spinach',
        'col_5': 'my favorite veggies'}, {'col_1': 'chicken', 'col_2':
        'beef', 'col_3': None, 'col_4': 'brown eggs', 'col_5':
        'my favorite proteins'}]

    Parameters:

        data:   (iter)   An iterable of string lines (e.g. jc.utils.splitlines())
                         Item 0 must be the header row. Any spaces in header
                         names should be changed to underscore '_'. You
                         should also ensure headers are lowercase by using
                         .lower(). Do not change the position of header
                         names as the positions are used to find the data.

                         Also, ensure there are no blank line items.

        delim:  (string) Not used. Rows are sliced at the column
                         positions, so any character can appear in the
                         data. Kept for compatibility with existing callers.

    Returns:

        List of Dictionaries
    """
    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    # find header
    output: List = []
    header_text: str = data.pop(0)
    header_list: List = header_text.split()

    # find each column end position. Each header name is searched for
    # starting just after the previous one, so repeated names and any kind
    # of whitespace between names are handled. The end of a column is the
    # character just before the start of the next header name.
    header_cells = None
    if _NON_ASCII.search(header_text):
        header_cells = _cell_starts(header_text)

    header_spec_list = []
    col_start = header_text.find(header_list[0])
    for i, column in enumerate(header_list[0:len(header_list) - 1]):
        col_start = header_text.find(header_list[i + 1], col_start + len(column))
        header_spec = {
            'name': column,
            'end': (header_cells[col_start] if header_cells else col_start) - 1
        }

        header_spec_list.append(header_spec)

    # parse lines. The cut positions of each row are found from the right
    # and the row is sliced at those positions. The character at each cut
    # position (a whitespace character) is dropped.
    for entry in data:
        # rows with non-ASCII characters map the column positions from
        # display cells to character indexes
        row_cells = None
        if _NON_ASCII.search(entry):
            row_cells = _cell_chars(entry)
            entry_len = len(row_cells)
        else:
            entry_len = len(entry)

        cuts: List[int] = []

        # positions past the end of the line are treated as whitespace, so
        # short lines do not need to be padded. Cuts that fall there give
        # blank cells at the end of the row.
        trailing_cuts = 0

        for h_spec in reversed(header_spec_list):
            h_end = h_spec['end']

            if h_end >= entry_len:
                trailing_cuts += 1
                continue

            if row_cells:
                h_end = row_cells[h_end]

            # the characters between the previous cut and the end of its
            # column are known to not be whitespace, so start the search
            # just left of the previous cut instead of searching them again.
            # A cut that reaches the start of the line stays there.
            if cuts and h_end >= cuts[-1]:
                h_end = cuts[-1]
                if h_end > 0:
                    h_end -= 1

            # check if the location contains whitespace. if not
            # then move to the left until a space is found
            while h_end > 0 and not entry[h_end].isspace():
                h_end -= 1

            # a value that runs back to the start of the line is kept whole
            # in the next column: the cut goes before the line
            if h_end == 0 and not entry[0].isspace():
                h_end = -1

            if not cuts or h_end != cuts[-1]:
                cuts.append(h_end)

        # slice the row at the cut positions
        entry_list = []
        col_start = 0
        for h_end in reversed(cuts):
            entry_list.append(entry[col_start:h_end] if h_end >= 0 else '')
            col_start = h_end + 1
        entry_list.append(entry[col_start:])
        entry_list.extend([''] * trailing_cuts)

        # clean up leading and trailing spaces in entry
        clean_entry_list = []
        for col in entry_list:
            clean_entry = col.strip()
            if clean_entry == '':
                clean_entry = None

            clean_entry_list.append(clean_entry)

        output_line = dict(zip(header_list, clean_entry_list))
        output.append(output_line)

    return output
