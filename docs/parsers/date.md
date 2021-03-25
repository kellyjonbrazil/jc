
# jc.parsers.date
jc - JSON CLI output utility `date` command output parser

The `epoch` calculated timestamp field is naive. (i.e. based on the local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only available if the timezone field is UTC.

Usage (cli):

    $ date | jc --date

    or

    $ jc date

Usage (module):

    import jc.parsers.date
    result = jc.parsers.date.parse(date_command_output)

Compatibility:

    'linux', 'darwin', 'freebsd'

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


## info
```python
info()
```


## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (Dictionary) raw structured data to process

Returns:

    Dictionary. Structured data with the following schema:
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
      "utc_offset":         string,       # null if timezone field is not UTC
      "day_of_year":        integer,
      "week_of_year":       integer,
      "iso":                string,
      "epoch":              integer,      # naive timestamp
      "epoch_utc":          integer,      # timezone-aware timestamp. Only available if timezone field is UTC
      "timezone_aware":     boolean       # if true, all fields are correctly based on UTC
    }


## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

