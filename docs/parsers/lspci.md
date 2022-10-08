[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.lspci"></a>

# jc.parsers.lspci

jc - JSON Convert `lspci -mmv` command output parser

This parser supports the following `lspci` options:
- `-mmv`
- `-nmmv`
- `-nnmmv`

Usage (cli):

    $ lspci -nnmmv | jc --lspci

or

    $ jc lspci -nnmmv

Usage (module):

    import jc
    result = jc.parse('lspci', lspci_command_output)

Schema:

    [
      {
        "lspci":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ lspci | jc --lspci -p
    []

    $ lspci | jc --lspci -p -r
    []

<a id="jc.parsers.lspci.parse"></a>

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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
