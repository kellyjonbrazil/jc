[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.lsb_release"></a>

# jc.parsers.lsb_release

jc - JSON Convert `lsb_release` command parser

This parser is an alias to the Key/Value parser (`--kv`).

Usage (cli):

    $ lsb_release -a | jc --lsb-release

or
    $ jc lsb_release -a

Usage (module):

    import jc
    result = jc.parse('lsb_release', lsb_release_command_output)

Schema:

    {
        "<key>":     string
    }

Examples:

    $ lsb_release -a | jc --lsb-release -p
    {
      "Distributor ID": "Ubuntu",
      "Description": "Ubuntu 16.04.6 LTS",
      "Release": "16.04",
      "Codename": "xenial"
    }

<a id="jc.parsers.lsb_release.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/lsb_release.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/lsb_release.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
