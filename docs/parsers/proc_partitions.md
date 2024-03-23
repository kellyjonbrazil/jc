[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_partitions"></a>

# jc.parsers.proc_partitions

jc - JSON Convert `/proc/partitions` file parser

Usage (cli):

    $ cat /proc/partitions | jc --proc

or

    $ jc /proc/partitions

or

    $ cat /proc/partitions | jc --proc-partitions

Usage (module):

    import jc
    result = jc.parse('proc', proc_partitions_file)

or

    import jc
    result = jc.parse('proc_partitions', proc_partitions_file)

Schema:

    [
      {
        "major":                  integer,
        "minor":                  integer,
        "num_blocks":             integer,
        "name":                   string
      }
    ]

Examples:

    $ cat /proc/partitions | jc --proc -p
    [
      {
        "major": 7,
        "minor": 0,
        "num_blocks": 56896,
        "name": "loop0"
      },
      {
        "major": 7,
        "minor": 1,
        "num_blocks": 56868,
        "name": "loop1"
      },
      ...
    ]

    $ cat /proc/partitions | jc --proc-partitions -p -r
    [
      {
        "major": "7",
        "minor": "0",
        "num_blocks": "56896",
        "name": "loop0"
      },
      {
        "major": "7",
        "minor": "1",
        "num_blocks": "56868",
        "name": "loop1"
      },
      ...
    ]

<a id="jc.parsers.proc_partitions.parse"></a>

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

Source: [`jc/parsers/proc_partitions.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_partitions.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
