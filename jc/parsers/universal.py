r"""jc - JSON Convert universal parsers"""
from typing import Iterable, List, Dict


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
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

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

        data:   (iter)   An iterable of string lines (e.g. str.splitlines())
                         Item 0 must be the header row. Any spaces in header
                         names should be changed to underscore '_'. You
                         should also ensure headers are lowercase by using
                         .lower(). Do not change the position of header
                         names as the positions are used to find the data.

                         Also, ensure there are no blank line items.

        delim:  (string) Delimiter to use. By default `u\\2063`
                         (invisible separator) is used since it is unlikely
                         to ever be seen in terminal output. You can change
                         this for troubleshooting purposes or if there is a
                         delimiter conflict with your data.

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
    header_spec_list = []
    col_start = header_text.find(header_list[0])
    for i, column in enumerate(header_list[0:len(header_list) - 1]):
        col_start = header_text.find(header_list[i + 1], col_start + len(column))
        header_spec = {
            'name': column,
            'end': col_start - 1
        }

        header_spec_list.append(header_spec)

    # parse lines
    for entry in data:
        entry_len = len(entry)
        delim_in_data = delim in entry
        entry_chars = list(entry)

        # positions past the end of the line are treated as whitespace, so
        # short lines do not need to be padded. Delimiters that fall there
        # are appended to the end of the line.
        trailing_delims: List[int] = []

        # insert new separator since data can contain spaces
        last_end = None
        for h_spec in reversed(header_spec_list):
            h_end = h_spec['end']

            # the characters between the previous delimiter and the end of
            # its column are known to not be whitespace, so start the
            # search at the previous delimiter instead of searching them
            # again
            if last_end is not None and h_end > last_end:
                h_end = last_end

            if h_end >= entry_len:
                trailing_delims.append(h_end)
                last_end = h_end
                continue

            # check if the location contains whitespace. if not
            # then move to the left until a space is found
            while h_end > 0 and not entry_chars[h_end].isspace():
                h_end -= 1

            # insert custom delimiter
            entry_chars[h_end] = delim
            last_end = h_end

        # create the entry list from the new custom delimiter
        entry = ''.join(entry_chars)
        if trailing_delims:
            if delim_in_data:
                # the delimiter is part of the data, so the spaces between
                # the delimiters can end up inside a value. Pad the same as
                # a full-width line would be padded.
                for h_end in reversed(trailing_delims):
                    entry = entry + ' ' * (h_end - len(entry)) + delim
            else:
                entry = entry + delim * len(trailing_delims)
        entry_list = entry.split(delim, maxsplit=len(header_list) - 1)

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
