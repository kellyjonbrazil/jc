[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.datetime_iso"></a>

# jc.parsers.datetime_iso

jc - JSON Convert ISO 8601 Datetime string parser

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

<a id="jc.parsers.datetime_iso.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, aix, freebsd, darwin, win32, cygwin

Source: [`jc/parsers/datetime_iso.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/datetime_iso.py)

This parser can be used with the `--slurp` command-line option.

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
