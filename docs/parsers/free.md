[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.free"></a>

# jc.parsers.free

jc - JSON Convert `free` command output parser

Values are normalized to bytes when using `free -h`.

Usage (cli):

    $ free | jc --free

or

    $ jc free

Usage (module):

    import jc
    result = jc.parse('free', free_command_output)

Schema:

    [
      {
        "type":                 string,
        "total":                integer,
        "used":                 integer,
        "free":                 integer,
        "shared":               integer,
        "buff_cache":           integer,
        "available":            integer
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

<a id="jc.parsers.free.parse"></a>

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

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/free.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/free.py)

Version 1.8 by Kelly Brazil (kellyjonbrazil@gmail.com)
