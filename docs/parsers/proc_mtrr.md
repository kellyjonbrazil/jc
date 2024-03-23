[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_mtrr"></a>

# jc.parsers.proc_mtrr

jc - JSON Convert `/proc/mtrr` file parser

Usage (cli):

    $ cat /proc/mtrr | jc --proc

or

    $ jc /proc/mtrr

or

    $ cat /proc/mtrr | jc --proc-mtrr

Usage (module):

    import jc
    result = jc.parse('proc', proc_mtrr_file)

or

    import jc
    result = jc.parse('proc_mtrr', proc_mtrr_file)

Schema:

    [
      {
        "register":             string,
        "type":                 string,
        "base":                 string,
        "base_mb":              integer,
        "size":                 integer,
        "count":                integer,
        "<key>":                string  # additional key/values are strings
      }
    ]

Examples:

    $ cat /proc/mtrr | jc --proc -p
    [
      {
        "register": "reg00",
        "type": "write-back",
        "base": "0x000000000",
        "base_mb": 0,
        "size": 2048,
        "count": 1
      },
      {
        "register": "reg01",
        "type": "write-back",
        "base": "0x080000000",
        "base_mb": 2048,
        "size": 1024,
        "count": 1
      },
      ...
    ]

    $ cat /proc/mtrr | jc --proc-mtrr -p -r
    [
      {
        "register": "reg00",
        "type": "write-back",
        "base": "0x000000000",
        "base_mb": "0",
        "size": "2048MB",
        "count": "1"
      },
      {
        "register": "reg01",
        "type": "write-back",
        "base": "0x080000000",
        "base_mb": "2048",
        "size": "1024MB",
        "count": "1"
      },
      ...
    ]

<a id="jc.parsers.proc_mtrr.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
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

Source: [`jc/parsers/proc_mtrr.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_mtrr.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
