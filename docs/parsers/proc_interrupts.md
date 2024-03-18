[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_interrupts"></a>

# jc.parsers.proc_interrupts

jc - JSON Convert `/proc/interrupts` file parser

Usage (cli):

    $ cat /proc/interrupts | jc --proc

or

    $ jc /proc/interrupts

or

    $ cat /proc/interrupts | jc --proc-interrupts

Usage (module):

    import jc
    result = jc.parse('proc', proc_interrupts_file)

or

    import jc
    result = jc.parse('proc_interrupts', proc_interrupts_file)

Schema:

    [
      {
        "irq":                      string,
        "cpu_num":                  integer,
        "interrupts": [
                                    integer
        ],
        "type":                     string,
        "device": [
                                    string
        ]
      }
    ]

Examples:

    $ cat /proc/interrupts | jc --proc -p
    [
      {
        "irq": "0",
        "cpu_num": 2,
        "interrupts": [
          18,
          0
        ],
        "type": "IO-APIC",
        "device": [
          "2-edge",
          "timer"
        ]
      },
      {
        "irq": "1",
        "cpu_num": 2,
        "interrupts": [
          0,
          73
        ],
        "type": "IO-APIC",
        "device": [
          "1-edge",
          "i8042"
        ]
      },
      ...
    ]

    $ cat /proc/interrupts | jc --proc-interrupts -p -r
    [
      {
        "irq": "0",
        "cpu_num": 2,
        "interrupts": [
          "18",
          "0"
        ],
        "type": "IO-APIC",
        "device": [
          "2-edge",
          "timer"
        ]
      },
      {
        "irq": "1",
        "cpu_num": 2,
        "interrupts": [
          "0",
          "73"
        ],
        "type": "IO-APIC",
        "device": [
          "1-edge",
          "i8042"
        ]
      },
      ...
    ]

<a id="jc.parsers.proc_interrupts.parse"></a>

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

Source: [`jc/parsers/proc_interrupts.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_interrupts.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
