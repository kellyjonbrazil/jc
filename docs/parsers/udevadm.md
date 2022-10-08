[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.udevadm"></a>

# jc.parsers.udevadm

jc - JSON Convert `udevadm info` command output parser

Usage (cli):

    $ udevadm info --query=all /dev/sda | jc --udevadm

or

    $ jc udevadm info --query=all /dev/sda

Usage (module):

    import jc
    result = jc.parse('udevadm', udevadm_command_output)

Schema:

    [
      {
        "udevadm":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ udevadm info --query=all /dev/sda | jc --udevadm -p
    []

    $ udevadm info --query=all /dev/sda | jc --udevadm -p -r
    []

<a id="jc.parsers.udevadm.parse"></a>

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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
