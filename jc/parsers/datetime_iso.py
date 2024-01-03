"""jc - JSON Convert ISO 8601 Datetime string parser

This parser supports standard ISO 8601 strings that include both date and
time. If no timezone or offset information is available in the string, then
UTC timezone is used.

Usage (cli):

    $ echo "2022-07-20T14:52:45Z" | jc --iso-datetime

Usage (module):

    import jc
    result = jc.parse('iso_datetime', iso_8601_string)

Schema:

    {
      "year":               integer,
      "month":              string,
      "month_num":          integer,
      "day":                integer,
      "weekday":            string,
      "weekday_num":        integer,
      "hour":               integer,
      "hour_24":            integer,
      "minute":             integer,
      "second":             integer,
      "microsecond":        integer,
      "period":             string,
      "utc_offset":         string,
      "day_of_year":        integer,
      "week_of_year":       integer,
      "iso":                string,
      "timestamp":          integer  # [0]
    }

    [0] timezone aware UNIX timestamp expressed in UTC

Examples:

    $ echo "2022-07-20T14:52:45Z" | jc --iso-datetime -p
    {
      "year": 2022,
      "month": "Jul",
      "month_num": 7,
      "day": 20,
      "weekday": "Wed",
      "weekday_num": 3,
      "hour": 2,
      "hour_24": 14,
      "minute": 52,
      "second": 45,
      "microsecond": 0,
      "period": "PM",
      "utc_offset": "+0000",
      "day_of_year": 201,
      "week_of_year": 29,
      "iso": "2022-07-20T14:52:45+00:00",
      "timestamp": 1658328765
    }
"""
import datetime
import re
import typing
from decimal import Decimal
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'ISO 8601 Datetime string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the pyiso8601 library from https://github.com/micktwomey/pyiso8601/releases/tag/1.0.2'
    compatible = ['linux', 'aix', 'freebsd', 'darwin', 'win32', 'cygwin']
    tags = ['standard', 'string', 'slurpable']


__version__ = info.version


####################################################
"""
pyiso8601 library from https://github.com/micktwomey/pyiso8601/releases/tag/1.0.2
"""

"""
Copyright (c) 2007 - 2022 Michael Twomey

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""ISO 8601 date time string parsing
Basic usage:
>>> import iso8601
>>> iso8601._parse_date("2007-01-25T12:00:00Z")
datetime.datetime(2007, 1, 25, 12, 0, tzinfo=<iso8601.Utc ...>)
>>>
"""

# __all__ = ["_parse_date", "_ParseError", "UTC", "_FixedOffset"]

# Adapted from http://delete.me.uk/2005/03/iso8601.html
ISO8601_REGEX = re.compile(
    r"""
    (?P<year>[0-9]{4})
    (
        (
            (-(?P<monthdash>[0-9]{1,2}))
            |
            (?P<month>[0-9]{2})
            (?!$)  # Don't allow YYYYMM
        )
        (
            (
                (-(?P<daydash>[0-9]{1,2}))
                |
                (?P<day>[0-9]{2})
            )
            (
                (
                    (?P<separator>[ T])
                    (?P<hour>[0-9]{2})
                    (:{0,1}(?P<minute>[0-9]{2})){0,1}
                    (
                        :{0,1}(?P<second>[0-9]{1,2})
                        ([.,](?P<second_fraction>[0-9]+)){0,1}
                    ){0,1}
                    (?P<timezone>
                        Z
                        |
                        (
                            (?P<tz_sign>[-+])
                            (?P<tz_hour>[0-9]{2})
                            :{0,1}
                            (?P<tz_minute>[0-9]{2}){0,1}
                        )
                    ){0,1}
                ){0,1}
            )
        ){0,1}  # YYYY-MM
    ){0,1}  # YYYY only
    $
    """,
    re.VERBOSE,
)


class _ParseError(ValueError):
    """Raised when there is a problem parsing a date string"""


UTC = datetime.timezone.utc


def _FixedOffset(
    offset_hours: float, offset_minutes: float, name: str
) -> datetime.timezone:
    return datetime.timezone(
        datetime.timedelta(hours=offset_hours, minutes=offset_minutes), name
    )


def _parse_timezone(
    matches: typing.Dict[str, str],
    default_timezone: typing.Optional[datetime.timezone] = UTC,
) -> typing.Optional[datetime.timezone]:
    """Parses ISO 8601 time zone specs into tzinfo offsets"""
    tz = matches.get("timezone", None)
    if tz == "Z":
        return UTC
    # This isn't strictly correct, but it's common to encounter dates without
    # timezones so I'll assume the default (which defaults to UTC).
    # Addresses issue 4.
    if tz is None:
        return default_timezone
    sign = matches.get("tz_sign", None)
    hours = int(matches.get("tz_hour", 0))
    minutes = int(matches.get("tz_minute", 0))
    description = f"{sign}{hours:02d}:{minutes:02d}"
    if sign == "-":
        hours = -hours
        minutes = -minutes
    return _FixedOffset(hours, minutes, description)


def _parse_date(
    datestring: str, default_timezone: typing.Optional[datetime.timezone] = UTC
) -> datetime.datetime:
    """Parses ISO 8601 dates into datetime objects
    The timezone is parsed from the date string. However it is quite common to
    have dates without a timezone (not strictly correct). In this case the
    default timezone specified in default_timezone is used. This is UTC by
    default.
    :param datestring: The date to parse as a string
    :param default_timezone: A datetime tzinfo instance to use when no timezone
                             is specified in the datestring. If this is set to
                             None then a naive datetime object is returned.
    :returns: A datetime.datetime instance
    :raises: _ParseError when there is a problem parsing the date or
             constructing the datetime instance.
    """
    try:
        m = ISO8601_REGEX.match(datestring)
    except Exception as e:
        raise _ParseError(e)

    if not m:
        raise _ParseError(f"Unable to parse date string {datestring!r}")

    # Drop any Nones from the regex matches
    # TODO: check if there's a way to omit results in regexes
    groups: typing.Dict[str, str] = {
        k: v for k, v in m.groupdict().items() if v is not None
    }

    try:
        return datetime.datetime(
            year=int(groups.get("year", 0)),
            month=int(groups.get("month", groups.get("monthdash", 1))),
            day=int(groups.get("day", groups.get("daydash", 1))),
            hour=int(groups.get("hour", 0)),
            minute=int(groups.get("minute", 0)),
            second=int(groups.get("second", 0)),
            microsecond=int(
                Decimal(f"0.{groups.get('second_fraction', 0)}") * Decimal("1000000.0")
            ),
            tzinfo=_parse_timezone(groups, default_timezone=default_timezone),
        )
    except Exception as e:
        raise _ParseError(e)

####################################################


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

        dt = _parse_date(data)

        raw_output = {
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
            'microsecond': dt.microsecond,
            'period': dt.strftime('%p').upper(),
            'utc_offset': dt.strftime('%z') or None,
            'day_of_year': int(dt.strftime('%j')),
            'week_of_year': int(dt.strftime('%W')),
            'iso': dt.isoformat(),
            'timestamp': int(dt.timestamp())
        }

    return raw_output if raw else _process(raw_output)
