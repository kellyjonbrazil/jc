[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.timestamp"></a>

# jc.parsers.timestamp

jc - JSON Convert Unix Epoch Timestamp string parser

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

<a id="jc.parsers.timestamp.parse"></a>

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

Source: [`jc/parsers/timestamp.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/timestamp.py)

This parser can be used with the `--slurp` command-line option.

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
