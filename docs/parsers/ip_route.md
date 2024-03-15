[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ip_route"></a>

# jc.parsers.ip_route

jc - JSON Convert `ip route` command output parser

Usage (cli):

    $ ip route | jc --ip-route

or

    $ jc ip-route

Usage (module):

    import jc
    result = jc.parse('ip_route', ip_route_command_output)

Schema:

    [
      {
        "ip":        string,
        "via":       string,
        "dev":       string,
        "metric":    integer,
        "proto":     string,
        "scope":     string,
        "src":       string,
        "via":       string,
        "status":    string
      }
    ]

Examples:

    $ ip route  | jc --ip-route -p
    [
      {
        "ip": "10.0.2.0/24",
        "dev": "enp0s3",
        "proto": "kernel",
        "scope": "link",
        "src": "10.0.2.15",
        "metric": 100
      }
    ]

<a id="jc.parsers.ip_route.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Json objects if data is processed and Raw data if raw = true.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/ip_route.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ip_route.py)

Version 1.0 by Julian Jackson (jackson.julian55@yahoo.com)
