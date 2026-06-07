r"""jc - JSON Convert `tsv` file parser

The `tsv` parser is a clone of the `csv` parser that uses '\t'
as the delimiter character. The first row of the file must be a header row.

Usage (cli):

    $ cat file.tsv | jc --tsv

Usage (module):

    import jc
    result = jc.parse('tsv', tsv_output)

Schema:

TSV file converted to a Dictionary:
https://docs.python.org/3/library/csv.html

    [
      {
        "column_name1":     string,
        "column_name2":     string
      }
    ]

Examples:

    $ cat homes.tsv
    "Sell"	"List"	"Living"	"Rooms"	"Beds"	"Baths"	"Age"	"Acres"...
    142	160	28	10	5	3	60	0.28	3167
    175	180	18	8	4	1	12	0.43	4033
    129	132	13	6	3	1	41	0.33	1471
    ...

    $ cat homes.tsv | jc --tsv -p
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
from typing import List, Union
from jc.jc_types import JSONDictType
import jc.parsers.csv as jc_csv
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = 'TSV file parser'
    author = 'N/A'
    author_email = 'N/A'
    details = 'Using the python standard csv library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


def parse(
    data: Union[str, bytes],
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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
    return jc_csv.parse(data, raw, quiet, implicit_header=False, tsv=True)