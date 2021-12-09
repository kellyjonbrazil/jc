"""jc - JSON CLI output utility `csv` file streaming parser

> This streaming parser outputs JSON Lines

The `csv` streaming parser will attempt to automatically detect the delimiter character. If the delimiter cannot be detected it will default to comma. The first row of the file must be a header row.

Note: The first 100 rows are read into memory to enable delimiter detection, then the rest of the rows are loaded lazily.

Usage (cli):

    $ cat file.csv | jc --csv-s

Usage (module):

    import jc.parsers.csv_s
    result = jc.parsers.csv_s.parse(csv_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

Schema:

    csv file converted to a Dictionary: https://docs.python.org/3/library/csv.html

    {
      "column_name1":     string,
      "column_name2":     string,
      "_jc_meta":                      # This object only exists if using -qq or ignore_exceptions=True
        {
          "success":      boolean,     # true if successfully parsed, false if error
          "error":        string,      # exists if "success" is false
          "line":         string       # exists if "success" is false
        }
    }

Examples:

    $ cat homes.csv
    "Sell", "List", "Living", "Rooms", "Beds", "Baths", "Age", "Acres", "Taxes"
    142, 160, 28, 10, 5, 3,  60, 0.28,  3167
    175, 180, 18,  8, 4, 1,  12, 0.43,  4033
    129, 132, 13,  6, 3, 1,  41, 0.33,  1471
    ...

    $ cat homes.csv | jc --csv-s
    {"Sell":"142","List":"160","Living":"28","Rooms":"10","Beds":"5","Baths":"3","Age":"60","Acres":"0.28","Taxes":"3167"}
    {"Sell":"175","List":"180","Living":"18","Rooms":"8","Beds":"4","Baths":"1","Age":"12","Acres":"0.43","Taxes":"4033"}
    {"Sell":"129","List":"132","Living":"13","Rooms":"6","Beds":"3","Baths":"1","Age":"41","Acres":"0.33","Taxes":"1471"}
    ...
"""
import itertools
import csv
import jc.utils
from jc.utils import stream_success, stream_error
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'CSV file streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the python standard csv library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    streaming = True


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Each Dictionary represents a row in the csv file.
    """
    # No further processing
    return proc_data


def parse(data, raw=False, quiet=False, ignore_exceptions=False):
    """
    Main text parsing generator function. Returns an iterator object.

    Parameters:

        data:              (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
        raw:               (boolean)   output preprocessed JSON if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Yields:

        Dictionary. Raw or processed structured data.

    Returns:

        Iterator object
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.streaming_input_type_check(data)

    # convert data to an iterable in case a sequence like a list is used as input.
    # this allows the exhaustion of the input so we don't double-process later.
    data = iter(data)
    temp_list = []

    # first, load the first 100 lines into a list to detect the CSV dialect
    for line in itertools.islice(data, 100):
        temp_list.append(line)

    # check for Python bug that does not split on `\r` newlines from sys.stdin correctly
    # https://bugs.python.org/issue45617
    if len(temp_list) == 1:
        raise ParseError('Unable to detect line endings. Please try the non-streaming CSV parser instead.')

    sniffdata = '\n'.join(temp_list)

    dialect = None
    try:
        dialect = csv.Sniffer().sniff(sniffdata)
    except Exception:
        pass

    # chain `temp_list` and `data` together to lazy load the rest of the CSV data
    new_data = itertools.chain(temp_list, data)
    reader = csv.DictReader(new_data, dialect=dialect)

    for row in reader:
        try:
            yield stream_success(row, ignore_exceptions) if raw else stream_success(_process(row), ignore_exceptions)
        except Exception as e:
            yield stream_error(e, ignore_exceptions, row)
