r"""jc - JSON Convert `csv` file parser

The `csv` parser will attempt to automatically detect the delimiter
character. If the delimiter cannot be detected it will default to comma.
The first row of the file must be a header row.

Usage (cli):

    $ cat file.csv | jc --csv

Usage (module):

    import jc
    result = jc.parse('csv', csv_output)

Schema:

CSV file converted to a Dictionary:
https://docs.python.org/3/library/csv.html

    [
      {
        "column_name1":     string,
        "column_name2":     string
      }
    ]

Examples:

    $ cat homes.csv
    "Sell", "List", "Living", "Rooms", "Beds", "Baths", "Age", "Acres"...
    142, 160, 28, 10, 5, 3,  60, 0.28,  3167
    175, 180, 18,  8, 4, 1,  12, 0.43,  4033
    129, 132, 13,  6, 3, 1,  41, 0.33,  1471
    ...

    $ cat homes.csv | jc --csv -p
    [
      {
        "Sell": "142",
        "List": "160",
        "Living": "28",
        "Rooms": "10",
        "Beds": "5",
        "Baths": "3",
        "Age": "60",
        "Acres": "0.28",
        "Taxes": "3167"
      },
      {
        "Sell": "175",
        "List": "180",
        "Living": "18",
        "Rooms": "8",
        "Beds": "4",
        "Baths": "1",
        "Age": "12",
        "Acres": "0.43",
        "Taxes": "4033"
      },
      {
        "Sell": "129",
        "List": "132",
        "Living": "13",
        "Rooms": "6",
        "Beds": "3",
        "Baths": "1",
        "Age": "41",
        "Acres": "0.33",
        "Taxes": "1471"
      },
      ...
    ]
"""
import csv
import itertools
import re
from typing import List, Union, Type
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = 'CSV file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the python standard csv library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Each Dictionary represents a row in the csv
        file.
    """

    # No further processing
    return proc_data


def _sniff(data: str) -> Type[csv.Dialect]:
    """
    Detect the CSV dialect from the start of the text. The quote character
    is always a double quote. The delimiter can only be a punctuation or
    whitespace character that is found in the first row outside of quoted
    fields, and quoted fields and apostrophes are removed from the sample so
    they do not influence the detection. Raises an exception if the dialect
    cannot be detected.
    """
    masked = re.sub(r'"[^"]*("|$)', '""', data[:1024]).replace("'", '')
    rows = [row for row in jc.utils.splitlines(masked, split_cr=True) if row.strip()]

    # the last row is incomplete if the sample was cut off
    if len(data) > 1024 and len(rows) > 1:
        rows.pop()

    delimiters = re.sub(r'[\w"]', '', rows[0])
    dialect = csv.Sniffer().sniff('\n'.join(rows), delimiters)
    dialect.quotechar = '"'
    dialect.doublequote = True
    return dialect


def parse(
    data: Union[str, bytes],
    raw: bool = False,
    quiet: bool = False,
    implicit_header: bool = False,
    tsv: bool = False,
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:               (string)  text data to parse
        raw:                (boolean) unprocessed output if True
        quiet:              (boolean) suppress warning messages if True
        implicit_header:    (boolean) data has no header, generate column names
        tsv:                (boolean) force TSV delimiter

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    # remove BOM bytes, if present
    if isinstance(data, str):
        data = data.encode('utf-8')

    data = data.decode('utf-8-sig')

    raw_output = []
    # keep the line endings so line breaks inside quoted fields are kept
    cleandata = jc.utils.splitlines(data, keepends=True, split_cr=True)

    # Clear any blank lines before the header row. csv.DictReader skips the
    # other blank rows and keeps blank lines inside quoted fields.
    cleandata = itertools.dropwhile(lambda x: not x.strip('\r\n'), cleandata)

    if jc.utils.has_data(data):

        dialect: Union[str, Type[csv.Dialect]] = (
            'excel-tab' if tsv
            else 'excel'  # default in csv module
        )
        try:
            dialect = _sniff(data)
            if tsv:
                dialect.delimiter = '\t'
        except Exception:
            pass

        reader = csv.DictReader(
            cleandata,
            dialect=dialect,
            # In implicit mode Python will skip the header
            # and put all fields in `restkey` (`None`).
            fieldnames=[] if implicit_header else None
        )

        for row in reader:
            if implicit_header:
                row = { f"c{idx}": col for idx, col in enumerate(row[None]) }
            raw_output.append(row)

    return raw_output if raw else _process(raw_output)
