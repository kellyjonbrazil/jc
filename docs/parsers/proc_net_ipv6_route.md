[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_ipv6_route"></a>

# jc.parsers.proc_net_ipv6_route

jc - JSON Convert `/proc/net/ipv6_route` file parser

Usage (cli):

    $ cat /proc/net/ipv6_route | jc --proc

or

    $ jc /proc/net/ipv6_route

or

    $ cat /proc/net/ipv6_route | jc --proc-net-ipv6-route

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_ipv6_route_file)

or

    import jc
    result = jc.parse('proc_net_ipv6_route', proc_net_ipv6_route_file)

Schema:

    [
      {
        "dest_net":                 string,
        "dest_prefix":              string,
        "source_net":               string,
        "source_prefix":            string,
        "next_hop":                 string,
        "metric":                   string,
        "ref_count":                string,
        "use_count":                string,
        "flags":                    string,
        "device":                   string
      }
    ]

Examples:

    $ cat /proc/net/ipv6_route | jc --proc -p
    [
      {
        "dest_net": "00000000000000000000000000000001",
        "dest_prefix": "80",
        "source_net": "00000000000000000000000000000000",
        "source_prefix": "00",
        "next_hop": "00000000000000000000000000000000",
        "metric": "00000100",
        "ref_count": "00000001",
        "use_count": "00000000",
        "flags": "00000001",
        "device": "lo"
      },
      ...
    ]

<a id="jc.parsers.proc_net_ipv6_route.parse"></a>

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

Source: [`jc/parsers/proc_net_ipv6_route.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_ipv6_route.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
