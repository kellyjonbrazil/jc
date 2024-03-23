[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_route"></a>

# jc.parsers.proc_net_route

jc - JSON Convert `/proc/net/route` file parser

Usage (cli):

    $ cat /proc/net/route | jc --proc

or

    $ jc /proc/net/route

or

    $ cat /proc/net/route | jc --proc-net-route

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_route_file)

or

    import jc
    result = jc.parse('proc_net_route', proc_net_route_file)

Schema:

    [
      {
        "Iface":                  string,
        "Destination":            string,
        "Gateway":                string,
        "Flags":                  string,
        "RefCnt":                 integer,
        "Use":                    integer,
        "Metric":                 integer,
        "Mask":                   string,
        "MTU":                    integer,
        "Window":                 integer,
        "IRTT":                   integer
      }
  ]

Examples:

    $ cat /proc/net/route | jc --proc -p
    [
      {
        "Iface": "ens33",
        "Destination": "00000000",
        "Gateway": "0247A8C0",
        "Flags": "0003",
        "RefCnt": 0,
        "Use": 0,
        "Metric": 100,
        "Mask": "00000000",
        "MTU": 0,
        "Window": 0,
        "IRTT": 0
      },
      ...
    ]

    $ cat /proc/net/route | jc --proc-net-route -p -r
    [
      {
        "Iface": "ens33",
        "Destination": "00000000",
        "Gateway": "0247A8C0",
        "Flags": "0003",
        "RefCnt": "0",
        "Use": "0",
        "Metric": "100",
        "Mask": "00000000",
        "MTU": "0",
        "Window": "0",
        "IRTT": "0"
      },
      ...
    ]

<a id="jc.parsers.proc_net_route.parse"></a>

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

Source: [`jc/parsers/proc_net_route.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_route.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
