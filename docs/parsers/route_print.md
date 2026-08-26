[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.route_print"></a>

# jc.parsers.route_print

jc - JSON Convert `route print` command output parser

See also: the `route` command parser

Usage (cli):

    $ route print | jc --route-print

Usage (module):

    import jc
    result = jc.parse('route_print', route_print_command_output)

Schema:

    {
        "interface_list": [
            {
                "interface_index":            integer,
                "mac_address":                string,
                "description":                string
            }
        ],
        "ipv4_route_table": {
            "active_routes": [
                {
                    "network_destination":    string,
                    "netmask":                string,
                    "gateway":                string,
                    "interface":              string,
                    "metric":                 integer,  # [0]
                    "metric_set_to_default":  boolean   # [1]
                }
            ],
            "persistent_routes": [
                {
                    "network_address":        string,
                    "netmask":                string,
                    "gateway_address":        string,
                    "metric":                 integer   # [0]
                    "metric_set_to_default":  boolean   # [1]
                }
            ]
        },
        "ipv6_route_table": {
            "active_routes": [
                {
                    "interface":              integer,
                    "metric":                 integer,  # [0]
                    "metric_set_to_default":  boolean,  # [1]
                    "network_destination":    string,
                    "gateway":                string
                }
            ],
            "persistent_routes": [
                {
                    "interface":              integer,
                    "metric":                 integer,  # [0]
                    "metric_set_to_default":  boolean,  # [1]
                    "network_destination":    string,
                    "gateway":                string
                }
            ]
        }
    }

    [0] Null/None if "metric" = "Default"
    [1] True if "metric" = "Default"

Examples:

    $ route print | jc --route-print -p
    {
      "interface_list": [
        {
          "interface_index": 28,
          "mac_address": null,
          "description": "Tailscale Tunnel"
        },
        {
          "interface_index": 12,
          "mac_address": "00:1c:42:da:01:6a",
          "description": "Parallels VirtIO Ethernet Adapter"
        },
        {
          "interface_index": 1,
          "mac_address": null,
          "description": "Software Loopback Interface 1"
        }
      ],
      "ipv4_route_table": {
        "active_routes": [
          {
            "network_destination": "0.0.0.0",
            "netmask": "0.0.0.0",
            "gateway": "10.211.55.1",
            "interface": "10.211.55.3",
            "metric": 15,
            "metric_set_to_default": false
          },
          {
            "network_destination": "10.0.0.0",
            "netmask": "255.0.0.0",
            "gateway": "192.168.22.1",
            "interface": "10.211.55.3",
            "metric": 16,
            "metric_set_to_default": false
          },
          ...
          {
            "network_destination": "255.255.255.255",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "10.211.55.3",
            "metric": null,
            "metric_set_to_default": true
          }
        ],
        "persistent_routes": [
          {
            "network_address": "10.0.1.0",
            "netmask": "255.255.255.0",
            "gateway_address": "192.168.22.1",
            "metric": 1,
            "metric_set_to_default": false
          },
          {
            "network_address": "10.0.3.0",
            "netmask": "255.255.255.0",
            "gateway_address": "192.168.22.1",
            "metric": 1,
            "metric_set_to_default": false
          },
          ...
        ]
      },
      "ipv6_route_table": {
        "active_routes": [
          {
            "interface": 1,
            "metric": 331,
            "network_destination": "::1/128",
            "gateway": "On-link",
            "metric_set_to_default": false
          },
          {
            "interface": 12,
            "metric": 271,
            "network_destination": "2001:db8::/64",
            "gateway": "fe80::1",
            "metric_set_to_default": false
          },
          ...
          {
            "interface": 12,
            "metric": 271,
            "network_destination": "ff00::/8",
            "gateway": "On-link",
            "metric_set_to_default": false
          }
        ],
        "persistent_routes": [
          {
            "interface": 0,
            "metric": 4294967295,
            "network_destination": "2001:db8::/64",
            "gateway": "fe80::1",
            "metric_set_to_default": false
          }
        ]
      }
    }

<a id="jc.parsers.route_print.parse"></a>

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

    Parsed dictionary. The raw and processed data structures are the same.

### Parser Information
Compatibility:  win32

Source: [`jc/parsers/route_print.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/route_print.py)

Version 1.0 by joehacksalot (joehacksalot@gmail.com)
