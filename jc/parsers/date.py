"""jc - JSON CLI output utility date Parser

Usage:

    specify --date as the first argument if the piped input is coming from date

Compatibility:

    'linux', 'darwin', 'freebsd'

Examples:

    $ date | jc --date -p
    {
      "year": 2020,
      "month": "Jul",
      "day": 31,
      "weekday": "Fri",
      "hour": 14,
      "minute": 35,
      "second": 55,
      "timezone": "PDT"
    }

    $ date | jc --date -p -r
    {
      "year": "2020",
      "month": "Jul",
      "day": "31",
      "weekday": "Fri",
      "hour": "14",
      "minute": "36",
      "second": "14",
      "timezone": "PDT"
    }
"""
import jc.utils


class info():
    version = '1.0'
    description = 'date command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['date']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        {
          "year":      integer,
          "month":     string,
          "day":       integer,
          "weekday":   string,
          "hour":      integer,
          "minute":    integer,
          "second":    integer,
          "timezone":  string
        }
    """
    return {
        "year": int(proc_data['year']),
        "month": proc_data['month'],
        "day": int(proc_data['day']),
        "weekday": proc_data['weekday'],
        "hour": int(proc_data['hour']),
        "minute": int(proc_data['minute']),
        "second": int(proc_data['second']),
        "timezone": proc_data['timezone']
    }


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

    raw_output = {}

    if jc.utils.has_data(data):
        data = data.replace(':', ' ')
        split_data = data.split()

        raw_output = {
            "year": split_data[7],
            "month": split_data[1],
            "day": split_data[2],
            "weekday": split_data[0],
            "hour": split_data[3],
            "minute": split_data[4],
            "second": split_data[5],
            "timezone": split_data[6]
        }

    if raw:
        return raw_output
    else:
        return process(raw_output)
