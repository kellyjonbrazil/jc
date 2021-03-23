
# jc.parsers.date
jc - JSON CLI output utility `date` command output parser

The `epoch` calculated timestamp field is naive (i.e. based on the local time of the system the parser is run on)
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
      "month_num": 3,
      "day": 23,
      "hour": 17,
      "minute": 41,
      "second": 44,
      "period": null,
      "month": "Mar",
      "weekday": "Tue",
      "weekday_num": 2,
      "timezone": "UTC",
      "epoch": 1616546504,
      "epoch_utc": 1616571704
    }

    $ date | jc --date -p -r
    {
      "year": "2021",
      "month": "Mar",
      "day": "23",
      "weekday": "Tue",
      "hour": "17",
      "minute": "41",
      "second": "44",
      "timezone": "UTC"
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
      "year":         integer,
      "month_num":    integer,
      "day":          integer,
      "hour":         integer,
      "minute":       integer,
      "second":       integer,
      "period":       string,
      "month":        string,
      "weekday":      string,
      "weekday_num":  integer,
      "timezone":     string,
      "epoch":        integer,       # naive timestamp
      "epoch_utc":    integer,       # timezone-aware timestamp. Only available if timezone field is UTC
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

