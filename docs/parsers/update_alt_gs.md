[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.update_alt_gs"></a>

# jc.parsers.update_alt_gs

jc - JSON Convert `update-alternatives --get-selections` command output parser

Usage (cli):

    $ update-alternatives --get-selections | jc --update-alt-gs

or

    $ jc update-alternatives --get-selections

Usage (module):

    import jc
    result = jc.parse('update-alt-gs',
                      update_alternatives_get_selections_command_output)

Schema:

    [
      {
        "name":     string,
        "status":   string,
        "current":  string
      }
    ]

Examples:

    $ update-alternatives --get-selections | jc --update-alt-gs -p
    [
      {
        "name": "arptables",
        "status": "auto",
        "current": "/usr/sbin/arptables-nft"
      },
      {
        "name": "awk",
        "status": "auto",
        "current": "/usr/bin/gawk"
      }
    ]

<a id="jc.parsers.update_alt_gs.parse"></a>

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

Source: [`jc/parsers/update_alt_gs.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/update_alt_gs.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
