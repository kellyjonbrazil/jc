[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.mdadm"></a>

# jc.parsers.mdadm

jc - JSON Convert `mdadm` command output parser

<<Short mdadm description and caveats>>

Usage (cli):

    $ mdadm | jc --mdadm

    or

    $ jc mdadm

Usage (module):

    import jc
    result = jc.parse('mdadm', mdadm_command_output)

Schema:

    [
      {
        "mdadm":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ mdadm | jc --mdadm -p
    []

    $ mdadm | jc --mdadm -p -r
    []

<a id="jc.parsers.mdadm.parse"></a>

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

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
