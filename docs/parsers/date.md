
# jc.parsers.date
jc - JSON CLI output utility date Parser

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

    proc_data:   (dictionary) raw structured data to process

Returns:

    Dictionary. Structured data with the following schema:

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

