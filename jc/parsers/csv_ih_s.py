r"""jc - JSON Convert `csv` implicit header file streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

The `csv` implicit header parser will attempt to automatically detect the
delimiter character. If the delimiter cannot be detected it will default to
comma. The file must have no header, and the field names will be generated
as "c0", "c1", etc.

> Note: The first 100 rows are read into memory to enable delimiter
> detection, then the rest of the rows are loaded lazily.

Usage (cli):

    $ cat file.csv | jc --csv-ih

Usage (module):

    import jc
    result = jc.parse('csv_ih', csv_output.splitlines())

Schema:

CSV file converted to a Dictionary:
https://docs.python.org/3/library/csv.html

    {
      "c0":     string,
      "c1":     string,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":        boolean,     # false if error parsing
        "error":          string,      # exists if "success" is false
        "line":           string       # exists if "success" is false
      }
    }

Examples:

    $ cat homes.csv
    142, 160, 28, 10, 5, 3,  60, 0.28,  3167
    175, 180, 18,  8, 4, 1,  12, 0.43,  4033
    129, 132, 13,  6, 3, 1,  41, 0.33,  1471
    ...

    $ cat homes.csv | jc --csv-ih-s
    {"c0":"142","c1":"160","c2":"28","c3":"10","c4":"5"...}
    {"c0":"175","c1":"180","c2":"18","c3":"8","c4":"4"...}
    {"c0":"129","c1":"132","c2":"13","c3":"6","c4":"3"...}
    ...
"""
from typing import List, Union
from jc.jc_types import JSONDictType
import jc.parsers.csv_s as jc_csv_s
from jc.streaming import streaming_input_type_check
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'CSV implicit header file streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the python standard csv library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']
    streaming = True


__version__ = info.version

def parse(
    data: Union[str, bytes],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False,
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
    return jc_csv_s.parse(data, raw, quiet, ignore_exceptions, implicit_header=True)