[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.uptime"></a>

# jc.parsers.uptime

jc - JSON Convert `uptime` command output parser

Usage (cli):

    $ uptime | jc --uptime

or

    $ jc uptime

Usage (module):

    import jc
    result = jc.parse('uptime', uptime_command_output)

Schema:

    {
      "time":                   string,
      "time_hour":              integer,
      "time_minute":            integer,
      "time_second":            integer,        # null if not displayed
      "uptime":                 string,
      "uptime_days":            integer,
      "uptime_hours":           integer,
      "uptime_minutes":         integer,
      "uptime_total_seconds":   integer,
      "users":                  integer,
      "load_1m":                float,
      "load_5m":                float,
      "load_15m":               float
    }

Example:

    $ uptime | jc --uptime -p
    {
      "time": "11:35",
      "uptime": "3 days, 4:03",
      "users": 5,
      "load_1m": 1.88,
      "load_5m": 2.0,
      "load_15m": 1.94,
      "time_hour": 11,
      "time_minute": 35,
      "time_second": null,
      "uptime_days": 3,
      "uptime_hours": 4,
      "uptime_minutes": 3,
      "uptime_total_seconds": 273780
    }

    $ uptime | jc --uptime -p -r
    {
      "time": "11:36",
      "uptime": "3 days, 4:04",
      "users": "5",
      "load_1m": "1.88",
      "load_5m": "1.99",
      "load_15m": "1.94"
    }

<a id="jc.parsers.uptime.parse"></a>

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

    Dictionary. Raw or processed structured data

### Parser Information
Compatibility:  linux, darwin, cygwin, aix, freebsd

Source: [`jc/parsers/uptime.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/uptime.py)

This parser can be used with the `--slurp` command-line option.

Version 1.10 by Kelly Brazil (kellyjonbrazil@gmail.com)
