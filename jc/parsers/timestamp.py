"""jc - JSON Convert Unix Epoch Timestamp string parser

The naive fields are based on the local time of the system the parser is
run on.

The utc fields are timezone-aware, based on the UTC timezone.

Usage (cli):

    $ echo 1658599410 | jc --timestamp

Usage (module):

    import jc
    result = jc.parse('timestamp', timestamp_string)

Schema:

    {
      "naive": {
        "year":                 integer,
        "month":                string,
        "month_num":            integer,
        "day":                  integer,
        "weekday":              string,
        "weekday_num":          integer,
        "hour":                 integer,
        "hour_24":              integer,
        "minute":               integer,
        "second":               integer,
        "period":               string,
        "day_of_year":          integer,
        "week_of_year":         integer,
        "iso":                  string
      },
      "utc": {
        "year":                 integer,
        "month":                string,
        "month_num":            integer,
        "day":                  integer,
        "weekday":              string,
        "weekday_num":          integer,
        "hour":                 integer,
        "hour_24":              integer,
        "minute":               integer,
        "second":               integer,
        "period":               string,
        "utc_offset":           string,
        "day_of_year":          integer,
        "week_of_year":         integer,
        "iso":                  string
      }
    }

Examples:

    $ echo 1658599410 | jc --timestamp -p
    {
      "naive": {
        "year": 2022,
        "month": "Jul",
        "month_num": 7,
        "day": 23,
        "weekday": "Sat",
        "weekday_num": 6,
        "hour": 11,
        "hour_24": 11,
        "minute": 3,
        "second": 30,
        "period": "AM",
        "day_of_year": 204,
        "week_of_year": 29,
        "iso": "2022-07-23T11:03:30"
      },
      "utc": {
        "year": 2022,
        "month": "Jul",
        "month_num": 7,
        "day": 23,
        "weekday": "Sat",
        "weekday_num": 6,
        "hour": 6,
        "hour_24": 18,
        "minute": 3,
        "second": 30,
        "period": "PM",
        "utc_offset": "+0000",
        "day_of_year": 204,
        "week_of_year": 29,
        "iso": "2022-07-23T18:03:30+00:00"
      }
    }
"""
from datetime import datetime, timezone
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'Unix Epoch Timestamp string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'aix', 'freebsd', 'darwin', 'win32', 'cygwin']
    tags = ['standard', 'string', 'slurpable']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    # no further processing
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):

        data = data[0:10]
        dt = datetime.fromtimestamp(int(data))
        dt_utc = datetime.fromtimestamp(int(data), tz=timezone.utc)

        raw_output = {
            'naive': {
                'year': dt.year,
                'month': dt.strftime('%b'),
                'month_num': dt.month,
                'day': dt.day,
                'weekday': dt.strftime('%a'),
                'weekday_num': dt.isoweekday(),
                'hour': int(dt.strftime('%I')),
                'hour_24': dt.hour,
                'minute': dt.minute,
                'second': dt.second,
                'period': dt.strftime('%p').upper(),
                'day_of_year': int(dt.strftime('%j')),
                'week_of_year': int(dt.strftime('%W')),
                'iso': dt.isoformat()
            },
            'utc': {
                'year': dt_utc.year,
                'month': dt_utc.strftime('%b'),
                'month_num': dt_utc.month,
                'day': dt_utc.day,
                'weekday': dt_utc.strftime('%a'),
                'weekday_num': dt_utc.isoweekday(),
                'hour': int(dt_utc.strftime('%I')),
                'hour_24': dt_utc.hour,
                'minute': dt_utc.minute,
                'second': dt_utc.second,
                'period': dt_utc.strftime('%p').upper(),
                'utc_offset': dt_utc.strftime('%z') or None,
                'day_of_year': int(dt_utc.strftime('%j')),
                'week_of_year': int(dt_utc.strftime('%W')),
                'iso': dt_utc.isoformat()
            }
        }

    return raw_output if raw else _process(raw_output)
