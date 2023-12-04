[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.swapon"></a>

# jc.parsers.swapon

jc - JSON Convert `swapon` command output parser

> Note: Must use `swapon`

Usage (cli):

    $ swapon | jc --swapon

or

    $ jc swapon

Usage (module):

    import jc
    result = jc.parse('swapon', uname_command_output)

Schema:

    [
      {
        "name": string,
        "type": string,
        "size": int,
        "used": int,
        "priority": int,
      }
    ]

Example:

    $ swapon | jc --swapon
    [
      {
        "name": "/swapfile",
        "type": "file",
        "size": 1073741824,
        "used": 0,
        "priority": -2
      }
    ]

<a id="jc.parsers.swapon.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[_Entry]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, freebsd

Version 1.0 by Roey Darwish Dror (roey.ghost@gmail.com)
