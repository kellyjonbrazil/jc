[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_ioports"></a>

# jc.parsers.proc_ioports

jc - JSON Convert `/proc/ioports` file parser

Usage (cli):

    $ cat /proc/ioports | jc --proc

or

    $ jc /proc/ioports

or

    $ cat /proc/ioports | jc --proc-ioports

Usage (module):

    import jc
    result = jc.parse('proc', proc_ioports_file)

or

    import jc
    result = jc.parse('proc_ioports', proc_ioports_file)

Schema:

    [
      {
        "start":                   string,
        "end":                     string,
        "device":                  string
      }
    ]

Examples:

    $ cat /proc/ioports | jc --proc -p
    [
      {
        "start": "0000",
        "end": "0cf7",
        "device": "PCI Bus 0000:00"
      },
      {
        "start": "0000",
        "end": "001f",
        "device": "dma1"
      },
      {
        "start": "0020",
        "end": "0021",
        "device": "PNP0001:00"
      },
      ...
    ]

<a id="jc.parsers.proc_ioports.parse"></a>

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

Source: [`jc/parsers/proc_ioports.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_ioports.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
