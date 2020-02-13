"""jc - JSON CLI output utility free Parser

Usage:

    specify --free as the first argument if the piped input is coming from free

Compatibility:

    'linux'

Examples:

    $ free | jc --free -p
    [
      {
        "type": "Mem",
        "total": 3861340,
        "used": 220508,
        "free": 3381972,
        "shared": 11800,
        "buff_cache": 258860,
        "available": 3397784
      },
      {
        "type": "Swap",
        "total": 2097148,
        "used": 0,
        "free": 2097148
      }
    ]

    $ free | jc --free -p -r
    [
      {
        "type": "Mem",
        "total": "2017300",
        "used": "213104",
        "free": "1148452",
        "shared": "1176",
        "buff_cache": "655744",
        "available": "1622204"
      },
      {
        "type": "Swap",
        "total": "2097148",
        "used": "0",
        "free": "2097148"
      }
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    version = '1.0'
    description = 'free command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['free']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "type":         string,
            "total":        integer,
            "used":         integer,
            "free":         integer,
            "shared":       integer,
            "buff_cache":   integer,
            "available":    integer
          }
        ]
    """

    for entry in proc_data:
        int_list = ['total', 'used', 'free', 'shared', 'buff_cache', 'available']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

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

    cleandata = data.splitlines()
    cleandata[0] = cleandata[0].lower()
    cleandata[0] = cleandata[0].replace('buff/cache', 'buff_cache')
    cleandata[0] = 'type ' + cleandata[0]

    raw_output = jc.parsers.universal.simple_table_parse(cleandata)

    for entry in raw_output:
        entry['type'] = entry['type'].rstrip(':')

    if raw:
        return raw_output
    else:
        return process(raw_output)
