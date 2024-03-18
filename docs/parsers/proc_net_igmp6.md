[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_igmp6"></a>

# jc.parsers.proc_net_igmp6

jc - JSON Convert `/proc/net/igmp6` file parser

Usage (cli):

    $ cat /proc/net/igmp6 | jc --proc

or

    $ jc /proc/net/igmp6

or

    $ cat /proc/net/igmp6 | jc --proc-net-igmp6

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_igmp6_file)

or

    import jc
    result = jc.parse('proc_net_igmp6', proc_net_igmp6_file)

Schema:

    [
      {
        "index":                    integer,
        "name":                     string,
        "address":                  string,
        "users":                    integer,
        "group":                    string,
        "reporters":                integer
      }
    ]

Examples:

    $ cat /proc/net/igmp6 | jc --proc -p
    [
      {
        "index": 1,
        "name": "lo",
        "address": "ff020000000000000000000000000001",
        "users": 1,
        "group": "0000000C",
        "reporters": 0
      },
      {
        "index": 1,
        "name": "lo",
        "address": "ff010000000000000000000000000001",
        "users": 1,
        "group": "00000008",
        "reporters": 0
      },
      {
        "index": 2,
        "name": "ens33",
        "address": "ff0200000000000000000001ffa4e315",
        "users": 1,
        "group": "00000004",
        "reporters": 0
      },
      ...
    ]

    $ cat /proc/net/igmp6 | jc --proc-net-igmp6 -p -r
    [
      {
        "index": "1",
        "name": "lo",
        "address": "ff020000000000000000000000000001",
        "users": "1",
        "group": "0000000C",
        "reporters": "0"
      },
      {
        "index": "1",
        "name": "lo",
        "address": "ff010000000000000000000000000001",
        "users": "1",
        "group": "00000008",
        "reporters": "0"
      },
      {
        "index": "2",
        "name": "ens33",
        "address": "ff0200000000000000000001ffa4e315",
        "users": "1",
        "group": "00000004",
        "reporters": "0"
      }
    ]

<a id="jc.parsers.proc_net_igmp6.parse"></a>

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

Source: [`jc/parsers/proc_net_igmp6.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_igmp6.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
