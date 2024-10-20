[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ifconfig"></a>

# jc.parsers.ifconfig

jc - JSON Convert `ifconfig` command output parser

No `ifconfig` options are supported.

Consider using the `ip` command instead of `ifconfig` as it supports native
JSON output.

Usage (cli):

    $ ifconfig | jc --ifconfig

or

    $ jc ifconfig

Usage (module):

    import jc
    result = jc.parse('ifconfig', ifconfig_command_output)

Schema:

    [
      {
        "name":                     string,
        "type":                     string,
        "metric":                   integer
        "flags":                    integer,
        "state": [
                                    string
        ],
        "mtu":                      integer,
        "mac_addr":                 string,
        "ipv4_addr":                string,    # [0]
        "ipv4_mask":                string,    # [0]
        "ipv4_bcast":               string,    # [0]
        "ipv6_addr":                string,    # [0]
        "ipv6_mask":                integer,   # [0]
        "ipv6_scope":               string,    # [0]
        "ipv6_scope_id":            string,    # [0]
        "ipv6_type":                string,    # [0]
        "rx_packets":               integer,
        "rx_bytes":                 integer,
        "rx_errors":                integer,
        "rx_dropped":               integer,
        "rx_overruns":              integer,
        "rx_frame":                 integer,
        "tx_packets":               integer,
        "tx_bytes":                 integer,
        "tx_errors":                integer,
        "tx_dropped":               integer,
        "tx_overruns":              integer,
        "tx_carrier":               integer,
        "tx_collisions":            integer,
        "options":                  string,
        "options_flags": [
                                    string
        ],
        "status":                   string,
        "hw_address":               string,
        "media":                    string,
        "media_flags": [
                                    string
        ],
        "nd6_options":              integer,
        "nd6_flags": [
                                    string
        ],
        "plugged":                  string,
        "vendor":                   string,
        "vendor_pn":                string,
        "vendor_sn":                string,
        "vendor_date":              string,
        "module_temperature":       string,
        "module_voltage":           string
        "ipv4": [
          {
            "address":              string,
            "mask":                 string,
            "broadcast":            string
          }
        ],
        "ipv6: [
          {
            "address":              string,
            "scope_id":             string,
            "mask":                 integer,
            "scope":                string,
            "type":                 string
          }
        ],
        "lanes": [
          {
            "lane":                 integer,
            "rx_power_mw":          float,
            "rx_power_dbm":         float,
            "tx_bias_ma":           float
          }
        ]
      }
    ]

    [0] these fields only pick up the last IP address in the interface
        output and are here for backwards compatibility. For information on
        all IP addresses, use the `ipv4` and `ipv6` objects which contain an
        array of IP address objects.

Examples:

    $ ifconfig ens33 | jc --ifconfig -p
    [
      {
        "name": "ens33",
        "flags": 4163,
        "state": [
          "UP",
          "BROADCAST",
          "RUNNING",
          "MULTICAST"
        ],
        "mtu": 1500,
        "type": "Ethernet",
        "mac_addr": "00:0c:29:3b:58:0e",
        "ipv4_addr": "192.168.71.137",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": 64,
        "ipv6_scope": "0x20",
        "ipv6_type": "link",
        "metric": null,
        "rx_packets": 8061,
        "rx_errors": 0,
        "rx_dropped": 0,
        "rx_overruns": 0,
        "rx_frame": 0,
        "tx_packets": 4502,
        "tx_errors": 0,
        "tx_dropped": 0,
        "tx_overruns": 0,
        "tx_carrier": 0,
        "tx_collisions": 0,
        "rx_bytes": 1514413,
        "tx_bytes": 866622,
        "ipv4": [
          {
            "address": "192.168.71.137",
            "mask": "255.255.255.0",
            "broadcast": "192.168.71.255"
          }
        ],
        "ipv6": [
          {
            "address": "fe80::c1cb:715d:bc3e:b8a0",
            "scope_id": null,
            "mask": 64,
            "scope": "0x20",
            "type": "link"
          }
        ]
      }
    ]

    $ ifconfig ens33 | jc --ifconfig -p -r
    [
      {
        "name": "ens33",
        "flags": "4163",
        "state": "UP,BROADCAST,RUNNING,MULTICAST",
        "mtu": "1500",
        "type": "Ethernet",
        "mac_addr": "00:0c:29:3b:58:0e",
        "ipv4_addr": "192.168.71.137",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": "64",
        "ipv6_scope": "0x20",
        "ipv6_type": "link",
        "metric": null,
        "rx_packets": "8061",
        "rx_errors": "0",
        "rx_dropped": "0",
        "rx_overruns": "0",
        "rx_frame": "0",
        "tx_packets": "4502",
        "tx_errors": "0",
        "tx_dropped": "0",
        "tx_overruns": "0",
        "tx_carrier": "0",
        "tx_collisions": "0",
        "rx_bytes": "1514413",
        "tx_bytes": "866622",
        "ipv4": [
          {
            "address": "192.168.71.137",
            "mask": "255.255.255.0",
            "broadcast": "192.168.71.255"
          }
        ],
        "ipv6": [
          {
            "address": "fe80::c1cb:715d:bc3e:b8a0",
            "scope_id": null,
            "mask": "64",
            "scope": "0x20",
            "type": "link"
          }
        ]
      }
    ]

<a id="jc.parsers.ifconfig.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, aix, freebsd, darwin

Source: [`jc/parsers/ifconfig.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ifconfig.py)

Version 2.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
