[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_if_inet6"></a>

# jc.parsers.proc_net_if_inet6

jc - JSON Convert `/proc/net/if_inet6` file parser

Usage (cli):

    $ cat /proc/net/if_inet6 | jc --proc

or

    $ jc /proc/net/if_inet6

or

    $ cat /proc/net/if_inet6 | jc --proc-net-if-inet6

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_if_inet6_file)

or

    import jc
    result = jc.parse('proc_net_if_inet6', proc_net_if_inet6_file)

Schema:

    [
      {
        "address":              string,
        "index":                string,
        "prefix":               string,
        "scope":                string,
        "flags":                string,
        "name":                 string
      }
    ]

Examples:

    $ cat /proc/net/if_inet6 | jc --proc -p
    [
      {
        "address": "fe80000000000000020c29fffea4e315",
        "index": "02",
        "prefix": "40",
        "scope": "20",
        "flags": "80",
        "name": "ens33"
      },
      {
        "address": "00000000000000000000000000000001",
        "index": "01",
        "prefix": "80",
        "scope": "10",
        "flags": "80",
        "name": "lo"
      }
    ]

<a id="jc.parsers.proc_net_if_inet6.parse"></a>

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

Source: [`jc/parsers/proc_net_if_inet6.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_if_inet6.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
