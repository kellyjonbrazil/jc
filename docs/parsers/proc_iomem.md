[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_iomem"></a>

# jc.parsers.proc_iomem

jc - JSON Convert `/proc/iomem` file parser

Usage (cli):

    $ cat /proc/iomem | jc --proc

or

    $ jc /proc/iomem

or

    $ cat /proc/iomem | jc --proc-iomem

Usage (module):

    import jc
    result = jc.parse('proc', proc_iomem_file)

or

    import jc
    result = jc.parse('proc_iomem', proc_iomem_file)

Schema:

    [
      {
        "start":                   string,
        "end":                     string,
        "device":                  string
      }
    ]

Examples:

    $ cat /proc/iomem | jc --proc -p
    [
      {
        "start": "00000000",
        "end": "00000fff",
        "device": "Reserved"
      },
      {
        "start": "00001000",
        "end": "0009e7ff",
        "device": "System RAM"
      },
      {
        "start": "0009e800",
        "end": "0009ffff",
        "device": "Reserved"
      },
      ...
    ]

<a id="jc.parsers.proc_iomem.parse"></a>

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

Source: [`jc/parsers/proc_iomem.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_iomem.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
