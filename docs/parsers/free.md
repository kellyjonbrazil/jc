# jc.parsers.free
jc - JSON CLI output utility free Parser

Usage:
    specify --free as the first argument if the piped input is coming from free

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

## process
```python
process(proc_data)
```

schema:

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

## parse
```python
parse(data, raw=False, quiet=False)
```

Main parsing function

Arguments:

    raw:    (boolean) output preprocessed JSON if True
    quiet:  (boolean) suppress warning messages if True

