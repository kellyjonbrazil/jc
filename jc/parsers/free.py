"""jc - JSON CLI output utility free Parser

Usage:
    specify --free as the first argument if the piped input is coming from free

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


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:

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

        dictionary   raw or processed structured data
    """

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]
    headers.insert(0, "type")

    # clean up 'buff/cache' header
    # even though forward slash in a key is valid json, it can make things difficult
    headers = ['buff_cache' if x == 'buff/cache' else x for x in headers]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    for entry in raw_output:
        entry['type'] = entry['type'].rstrip(':')

    if raw:
        return raw_output
    else:
        return process(raw_output)
