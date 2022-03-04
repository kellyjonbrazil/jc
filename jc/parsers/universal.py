"""jc - JSON Convert universal parsers"""


import string
from typing import List, Dict


def simple_table_parse(data: List[str]) -> List[Dict]:
    """
    Parse simple tables. The last column may contain data with spaces.

    Parameters:

        data:   (list)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank lines (list items)
                         in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501
    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output


def sparse_table_parse(data: List[str], delim: str = '\u2063') -> List[Dict]:
    """
    Parse tables with missing column data or with spaces in column data.

    Parameters:

        data:   (list)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower(). Do not change the
                         position of header names as the positions are used
                         to find the data.

                         Also, ensure there are no blank lines (list items)
                         in the data.

        delim:  (string) Delimiter to use. By default `u\\2063`
                         (invisible separator) is used since it is unlikely
                         to ever be seen in terminal output. You can change
                         this for troubleshooting purposes or if there is a
                         delimiter conflict with your data.

    Returns:

        List of Dictionaries
    """
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
                        while h_end > 0 and entry[h_end] not in string.whitespace:
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
