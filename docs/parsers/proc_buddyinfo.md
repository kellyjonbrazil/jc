[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_buddyinfo"></a>

# jc.parsers.proc_buddyinfo

jc - JSON Convert `/proc/buddyinfo` file parser

Usage (cli):

    $ cat /proc/buddyinfo | jc --proc

or

    $ jc /proc/buddyinfo

or

    $ cat /proc/buddyinfo | jc --proc-buddyinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_buddyinfo_file)

or

    import jc
    result = jc.parse('proc_buddyinfo', proc_buddyinfo_file)

Schema:

All values are integers.

    [
      {
        "node":               integer,
        "zone":               string,
        "free_chunks": [
                              integer  # [0]
        ]
      }
    ]

    [0] array index correlates to the Order number.
        E.g. free_chunks[0] is the value for Order 0


Examples:

    $ cat /proc/buddyinfo | jc --proc -p
    [
      {
        "node": 0,
        "zone": "DMA",
        "free_chunks": [
          0,
          0,
          0,
          1,
          1,
          1,
          1,
          1,
          0,
          1,
          3
        ]
      },
      {
        "node": 0,
        "zone": "DMA32",
        "free_chunks": [
          78,
          114,
          82,
          52,
          38,
          25,
          13,
          9,
          3,
          4,
          629
        ]
      },
      {
        "node": 0,
        "zone": "Normal",
        "free_chunks": [
          0,
          22,
          8,
          10,
          1,
          1,
          2,
          11,
          13,
          0,
          0
        ]
      }
    ]

<a id="jc.parsers.proc_buddyinfo.parse"></a>

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

Source: [`jc/parsers/proc_buddyinfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_buddyinfo.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
