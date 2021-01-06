
# jc.parsers.uptime
jc - JSON CLI output utility `uptime` command output parser

Usage (cli):

    $ uptime | jc --uptime

    or

    $ jc uptime

Usage (module):

    import jc.parsers.uptime
    result = jc.parsers.uptime.parse(uptime_command_output)

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Example:

    $ uptime | jc --uptime -p
    {
      "time": "11:30:44",
      "uptime": "1 day, 21:17",
      "users": 1,
      "load_1m": 0.01,
      "load_5m": 0.04,
      "load_15m": 0.05
    }

    $ uptime | jc --uptime -p -r
    {
      "time": "11:31:09",
      "uptime": "1 day, 21:17",
      "users": "1",
      "load_1m": "0.00",
      "load_5m": "0.04",
      "load_15m": "0.05"
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
      "time":     string,
      "uptime":   string,
      "users":    integer,
      "load_1m":  float,
      "load_5m":  float,
      "load_15m": float
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

    Dictionary. Raw or processed structured data

