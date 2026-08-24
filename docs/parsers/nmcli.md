[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.nmcli"></a>

# jc.parsers.nmcli

jc - JSON Convert `nmcli` command output parser

Supports the following `nmcli` subcommands:
- `nmcli general`
- `nmcli general permissions`
- `nmcli connection`
- `nmcli connection show <device_name>`
- `nmcli device`
- `nmcli device show`
- `nmcli device show <device_name>`

Usage (cli):

    $ nmcli device show lo | jc --nmcli

or

    $ jc nmcli device show lo

Usage (module):

    import jc
    result = jc.parse('nmcli', nmcli_command_output)

Schema:

Because there are so many options, the schema is not strictly defined.
Integer and Float value conversions are attempted and the original
values are kept if they fail. If you don't want automatic conversion,
then use the `-r` or `raw=True` option to disable it.

The structure is flat, for the most part, but there are a couple of
"well-known" keys that are further parsed into objects for convenience.
These are documented below.

    [
      {
        "<key>":                  string/integer/float,   # [0]
        "team_config":            object/null,
        "team_port_config":       object/null,
        "dhcp4_option_x": {
          "name":                 string,
          "value":                string/integer/float,
        },
        "dhcp6_option_x": {
          "name":                 string,
          "value":                string/integer/float,
        },
        "ip4_route_x": {
          "dst":                  string,
          "nh":                   string,
          "mt":                   integer
        },
        "ip6_route_x": {
          "dst":                  string,
          "nh":                   string,
          "mt":                   integer,
          "table":                integer
        }
      }
    ]

    [0] all values of `---` are converted to null

Examples:

    $ nmcli connection show ens33 | jc --nmcli -p
    [
      {
        "connection_id": "ens33",
        "connection_uuid": "d92ece08-9e02-47d5-b2d2-92c80e155744",
        "connection_stable_id": null,
        "connection_type": "802-3-ethernet",
        "connection_interface_name": "ens33",
        "connection_autoconnect": "yes",
        ...
        "ip4_address_1": "192.168.71.180/24",
        "ip4_gateway": "192.168.71.2",
        "ip4_route_1": {
          "dst": "0.0.0.0/0",
          "nh": "192.168.71.2",
          "mt": 100
        },
        "ip4_route_2": {
          "dst": "192.168.71.0/24",
          "nh": "0.0.0.0",
          "mt": 100
        },
        "ip4_dns_1": "192.168.71.2",
        "ip4_domain_1": "localdomain",
        "dhcp4_option_1": {
          "name": "broadcast_address",
          "value": "192.168.71.255"
        },
        ...
        "ip6_address_1": "fe80::c1cb:715d:bc3e:b8a0/64",
        "ip6_gateway": null,
        "ip6_route_1": {
          "dst": "fe80::/64",
          "nh": "::",
          "mt": 100
        }
      }
    ]

    $ nmcli connection show ens33 | jc --nmcli -p -r
    [
      {
        "connection_id": "ens33",
        "connection_uuid": "d92ece08-9e02-47d5-b2d2-92c80e155744",
        "connection_stable_id": null,
        "connection_type": "802-3-ethernet",
        "connection_interface_name": "ens33",
        "connection_autoconnect": "yes",
        ...
        "ip4_address_1": "192.168.71.180/24",
        "ip4_gateway": "192.168.71.2",
        "ip4_route_1": {
          "dst": "0.0.0.0/0",
          "nh": "192.168.71.2",
          "mt": "100"
        },
        "ip4_route_2": {
          "dst": "192.168.71.0/24",
          "nh": "0.0.0.0",
          "mt": "100"
        },
        "ip4_dns_1": "192.168.71.2",
        "ip4_domain_1": "localdomain",
        "dhcp4_option_1": {
          "name": "broadcast_address",
          "value": "192.168.71.255"
        },
        ...
        "ip6_address_1": "fe80::c1cb:715d:bc3e:b8a0/64",
        "ip6_gateway": null,
        "ip6_route_1": {
          "dst": "fe80::/64",
          "nh": "::",
          "mt": "100"
        }
      }
    ]

<a id="jc.parsers.nmcli.parse"></a>

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

Source: [`jc/parsers/nmcli.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/nmcli.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
