[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_consoles"></a>

# jc.parsers.proc_consoles

jc - JSON Convert `/proc/consoles` file parser

Usage (cli):

    $ cat /proc/consoles | jc --proc

or

    $ jc /proc/consoles

or

    $ cat /proc/consoles | jc --proc-consoles

Usage (module):

    import jc
    result = jc.parse('proc', proc_consoles_file)

or

    import jc
    result = jc.parse('proc_consoles', proc_consoles_file)

Schema:

    [
      {
        "device":                     string,
        "operations":                 string,
        "operations_list": [
                                      string  # [0]
        ],
        "flags":                      string,
        "flags_list": [
                                      string  # [1]
        ],
        "major":                      integer,
        "minor":                      integer
      }
    ]

    [0] Values: read, write, unblank
    [1] Values: enabled, preferred, primary boot, prink buffer,
                braille device, safe when CPU offline

Examples:

    $ cat /proc/consoles | jc --proc -p
    [
      {
        "device": "tty0",
        "operations": "-WU",
        "operations_list": [
          "write",
          "unblank"
        ],
        "flags": "ECp",
        "flags_list": [
          "enabled",
          "preferred",
          "printk buffer"
        ],
        "major": 4,
        "minor": 7
      },
      {
        "device": "ttyS0",
        "operations": "-W-",
        "operations_list": [
          "write"
        ],
        "flags": "Ep",
        "flags_list": [
          "enabled",
          "printk buffer"
        ],
        "major": 4,
        "minor": 64
      }
    ]

<a id="jc.parsers.proc_consoles.parse"></a>

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

Source: [`jc/parsers/proc_consoles.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_consoles.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
