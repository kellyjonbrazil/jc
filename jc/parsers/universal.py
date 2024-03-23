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

    # find the longest line and pad all lines with spaces to match
    max_len = max([len(x) for x in data])

    new_data = []
    for line in data:
        new_data.append(line + ' ' * (max_len - len(line)))

    data = new_data

    # find header
    output: List = []
    header_text: str = data.pop(0)
    header_text = header_text + ' '
    header_list: List = header_text.split()

    # find each column index and end position
    header_search = [header_list[0]]
    for h in header_list[1:]:
        header_search.append(' ' + h + ' ')

    header_spec_list = []
    for i, column in enumerate(header_list[0:len(header_list) - 1]):
        header_spec = {
            'name': column,
            'end': header_text.find(header_search[i + 1])
        }

        header_spec_list.append(header_spec)

    # parse lines
    if data:
        for entry in data:
            output_line = {}

            # insert new separator since data can contain spaces
            for col in reversed(header_list):
                # find the right header_spec
                for h_spec in header_spec_list:
                    if h_spec['name'] == col:
                        h_end = h_spec['end']
                        # check if the location contains whitespace. if not
                        # then move to the left until a space is found
                        while h_end > 0 and not entry[h_end].isspace():
                            h_end -= 1

                        # insert custom delimiter
                        entry = entry[:h_end] + delim + entry[h_end + 1:]

            # create the entry list from the new custom delimiter
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
