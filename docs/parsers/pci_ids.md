[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pci_ids"></a>

# jc.parsers.pci\_ids

jc - JSON Convert `pci.ids` file parser

This parser converts the pci.ids database file.

https://raw.githubusercontent.com/pciutils/pciids/master/pci.ids

Usage (cli):

    $ cat pci.ids | jc --pci-ids

Usage (module):

    import jc
    result = jc.parse('pci_ids', pci_ids_file_output)

Schema:

    [
      {
        "pci-id":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ cat pci.ids | jc --pci-id -p
    []

    $ cat pci.ids | jc --pci-id -p -r
    []

<a id="jc.parsers.pci_ids.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
