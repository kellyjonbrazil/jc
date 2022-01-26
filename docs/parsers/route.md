[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.route"></a>

# jc.parsers.route

jc - JSON CLI output utility `route` command output parser

Usage (cli):

    $ route | jc --route

    or

    $ jc route

Usage (module):

    import jc
    result = jc.parse('route', route_command_output)

    or

    import jc.parsers.route
    result = jc.parsers.route.parse(route_command_output)

Schema:

    [
      {
        "destination":     string,
        "gateway":         string,
        "genmask":         string,
        "flags":           string,
        "flags_pretty": [
                           string
        ]
        "metric":          integer,
        "ref":             integer,
        "use":             integer,
        "mss":             integer,
        "window":          integer,
        "irtt":            integer,
        "iface":           string
      }
    ]

Examples:

    $ route -ee | jc --route -p
    [
      {
        "destination": "default",
        "gateway": "_gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": 202,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "flags_pretty": [
          "UP",
          "GATEWAY"
        ]
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": 202,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "flags_pretty": [
          "UP"
        ]
      }
    ]

    $ route -ee | jc --route -p -r
    [
      {
        "destination": "default",
        "gateway": "_gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": "202",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": "202",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      }
    ]

<a id="jc.parsers.route.parse"></a>

#### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

#### Parser Information
Compatibility:  linux

Version 1.7 by Kelly Brazil (kellyjonbrazil@gmail.com)
