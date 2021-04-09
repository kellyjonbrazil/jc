[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.free
jc - JSON CLI output utility `free` command output parser

Usage (cli):

    $ free | jc --free

    or

    $ jc free

Usage (module):

    import jc.parsers.free
    result = jc.parsers.free.parse(free_command_output)

Schema:

    [
      {
        "type":         string,
        "total":        integer,
        "used":         integer,
        "free":         integer,
        "shared":       integer,
        "buff_cache":   integer,
        "available":    integer
      }
    ]

Examples:

    $ free | jc --free -p
    [
      {
        "type": "Mem",
        "total": 3861340,
        "used": 220508,
        "free": 3381972,
        "shared": 11800,
        "buff_cache": 258860,
        "available": 3397784
      },
      {
        "type": "Swap",
        "total": 2097148,
        "used": 0,
        "free": 2097148
      }
    ]

    $ free | jc --free -p -r
    [
      {
        "type": "Mem",
        "total": "2017300",
        "used": "213104",
        "free": "1148452",
        "shared": "1176",
        "buff_cache": "655744",
        "available": "1622204"
      },
      {
        "type": "Swap",
        "total": "2097148",
        "used": "0",
        "free": "2097148"
      }
    ]


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

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

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
