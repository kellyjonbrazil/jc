
# jc.parsers.date
jc - JSON CLI output utility `date` command output parser

Calculated epoch time field is naive (i.e. based on the local time of the system the parser is run on) since there is no unambiguous timezone information in the `date` command output.

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
      "day": 22,
      "hour": 20,
      "minute": 47,
      "second": 3,
      "period": null,
      "month": "Mar",
      "weekday": "Mon",
      "weekday_num": 1,
      "timezone": "PDT",
      "epoch": 1616471223
    }


    $ date | jc --date -p -r
    {
      "year": "2021",
      "month": "Mar",
      "day": "22",
      "weekday": "Mon",
      "hour": "20",
      "minute": "48",
      "second": "12",
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
      "epoch":        integer
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

