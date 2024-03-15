[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.os_prober"></a>

# jc.parsers.os_prober

jc - JSON Convert `os-prober` command output parser

Usage (cli):

    $ os-prober | jc --os-prober

or

    $ jc os-prober

Usage (module):

    import jc
    result = jc.parse('os_prober', os_prober_command_output)

Schema:

    {
      "partition":              string,
      "efi_bootmgr":            string,  # [0]
      "name":                   string,
      "short_name":             string,
      "type":                   string
    }

    [0] only exists if an EFI boot manager is detected

Examples:

    $ os-prober | jc --os-prober -p
    {
      "partition": "/dev/sda1",
      "name": "Windows 10",
      "short_name": "Windows",
      "type": "chain"
    }

<a id="jc.parsers.os_prober.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]
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

Source: [`jc/parsers/os_prober.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/os_prober.py)

This parser can be used with the `--slurp` command-line option.

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
