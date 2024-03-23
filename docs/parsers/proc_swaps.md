[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_swaps"></a>

# jc.parsers.proc_swaps

jc - JSON Convert `/proc/swaps` file parser

Usage (cli):

    $ cat /proc/swaps | jc --proc

or

    $ jc /proc/swaps

or

    $ cat /proc/swaps | jc --proc-swaps

Usage (module):

    import jc
    result = jc.parse('proc', proc_swaps_file)

or

    import jc
    result = jc.parse('proc_swaps', proc_swaps_file)

Schema:

    [
      {
        "filename":                 string,
        "type":                     string,
        "size":                     integer,
        "used":                     integer,
        "priority":                 integer
      }
    ]

Examples:

    $ cat /proc/swaps | jc --proc -p
    [
      {
        "filename": "/swap.img",
        "type": "file",
        "size": 3996668,
        "used": 0,
        "priority": -2
      },
      ...
    ]

    $ cat /proc/swaps | jc --proc-swaps -p -r
    [
      {
        "filename": "/swap.img",
        "type": "file",
        "size": "3996668",
        "used": "0",
        "priority": "-2"
      },
      ...
    ]

<a id="jc.parsers.proc_swaps.parse"></a>

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

Source: [`jc/parsers/proc_swaps.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_swaps.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
