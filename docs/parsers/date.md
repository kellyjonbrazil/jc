[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.date"></a>

# jc.parsers.date

jc - JSON Convert `date` command output parser

The `epoch` calculated timestamp field is naive. (i.e. based on the local
time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the timezone field is UTC.

Usage (cli):

    $ date | jc --date

or

    $ jc date

Usage (module):

    import jc
    result = jc.parse('date', date_command_output)

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
      "period":             string,
      "timezone":           string,
      "utc_offset":         string,      # null if timezone field is not UTC
      "day_of_year":        integer,
      "week_of_year":       integer,
      "iso":                string,
      "epoch":              integer,     # [0]
      "epoch_utc":          integer,     # [1]
      "timezone_aware":     boolean      # [2]
    }

    [0] naive timestamp
    [1] timezone-aware timestamp. Only available if timezone field is UTC
    [2] if true, all fields are correctly based on UTC

Examples:

    $ date | jc --date -p
    {
      "year": 2021,
      "month": "Mar",
      "month_num": 3,
      "day": 25,
      "weekday": "Thu",
      "weekday_num": 4,
      "hour": 2,
      "hour_24": 2,
      "minute": 2,
      "second": 26,
      "period": "AM",
      "timezone": "UTC",
      "utc_offset": "+0000",
      "day_of_year": 84,
      "week_of_year": 12,
      "iso": "2021-03-25T02:02:26+00:00",
      "epoch": 1616662946,
      "epoch_utc": 1616637746,
      "timezone_aware": true
    }

<a id="jc.parsers.date.parse"></a>

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
Compatibility:  linux, darwin, freebsd

Source: [`jc/parsers/date.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/date.py)

This parser can be used with the `--slurp` command-line option.

Version 2.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
