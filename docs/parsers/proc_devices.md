[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_devices"></a>

# jc.parsers.proc_devices

jc - JSON Convert `/proc/devices` file parser

Usage (cli):

    $ cat /proc/devices | jc --proc

or

    $ jc /proc/devices

or

    $ cat /proc/devices | jc --proc-devices

Usage (module):

    import jc
    result = jc.parse('proc', proc_devices_file)

or

    import jc
    result = jc.parse('proc_devices', proc_devices_file)

Schema:

Since devices can be members of multiple groups, the value for each device
is a list.

    {
      "character": {
        "<device number>": [
                                    string
        ]
      },
      "block": {
        "<device number>": [
                                    string
        ]
      }
    }

Examples:

    $ cat /proc/devices | jc --proc -p
    {
      "character": {
        "1": [
          "mem"
        ],
        "4": [
          "/dev/vc/0",
          "tty",
          "ttyS"
        ],
        "5": [
          "/dev/tty",
          "/dev/console",
          "/dev/ptmx",
          "ttyprintk"
        ],
      "block": {
        "7": [
          "loop"
        ],
        "8": [
          "sd"
        ],
        "9": [
          "md"
        ]
      }
    }

<a id="jc.parsers.proc_devices.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_devices.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_devices.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
