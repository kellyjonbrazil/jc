"""jc - JSON CLI output utility csv Parser

Usage:

    specify --csv as the first argument if the piped input is coming from a csv file.
    the csv parser will attempt to automatically detect the delimiter character.
    if the delimiter cannot be detected it will default to comma.
    the first row of the file must be a header row.

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ cat homes.csv
    "Sell", "List", "Living", "Rooms", "Beds", "Baths", "Age", "Acres", "Taxes"
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
import jc.utils
import csv


class info():
    version = '1.0'
    description = 'CSV file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the python standard csv library'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Each dictionary represents a row in the csv file:

        [
          {
            csv file converted to a Dictionary
            https://docs.python.org/3/library/csv.html
          }
        ]
    """

    # No further processing
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if cleandata:
        dialect = None
        try:
            dialect = csv.Sniffer().sniff(data[:1024])
        except Exception:
            pass

        reader = csv.DictReader(cleandata, dialect=dialect)

        for row in reader:
            raw_output.append(row)

    if raw:
        return raw_output
    else:
        return process(raw_output)
