[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ifconfig"></a>

# jc.parsers.ifconfig

jc - JSON Convert `ifconfig` command output parser

> Note: No `ifconfig` options are supported.

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
        "name":             string,
        "flags":            integer,
        "state": [
                            string
        ],
        "mtu":              integer,
        "ipv4_addr":        string,
        "ipv4_mask":        string,
        "ipv4_bcast":       string,
        "ipv6_addr":        string,
        "ipv6_mask":        integer,
        "ipv6_scope":       string,
        "mac_addr":         string,
        "type":             string,
        "rx_packets":       integer,
        "rx_bytes":         integer,
        "rx_errors":        integer,
        "rx_dropped":       integer,
        "rx_overruns":      integer,
        "rx_frame":         integer,
        "tx_packets":       integer,
        "tx_bytes":         integer,
        "tx_errors":        integer,
        "tx_dropped":       integer,
        "tx_overruns":      integer,
        "tx_carrier":       integer,
        "tx_collisions":    integer,
        "metric":           integer
      }
    ]

Examples:

    $ ifconfig | jc --ifconfig -p
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
        "ipv4_addr": "192.168.71.137",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": 64,
        "ipv6_scope": "0x20",
        "mac_addr": "00:0c:29:3b:58:0e",
        "type": "Ethernet",
        "rx_packets": 8061,
        "rx_bytes": 1514413,
        "rx_errors": 0,
        "rx_dropped": 0,
        "rx_overruns": 0,
        "rx_frame": 0,
        "tx_packets": 4502,
        "tx_bytes": 866622,
        "tx_errors": 0,
        "tx_dropped": 0,
        "tx_overruns": 0,
        "tx_carrier": 0,
        "tx_collisions": 0,
        "metric": null
      },
      {
        "name": "lo",
        "flags": 73,
        "state": [
          "UP",
          "LOOPBACK",
          "RUNNING"
        ],
        "mtu": 65536,
        "ipv4_addr": "127.0.0.1",
        "ipv4_mask": "255.0.0.0",
        "ipv4_bcast": null,
        "ipv6_addr": "::1",
        "ipv6_mask": 128,
        "ipv6_scope": "0x10",
        "mac_addr": null,
        "type": "Local Loopback",
        "rx_packets": 73,
        "rx_bytes": 6009,
        "rx_errors": 0,
        "rx_dropped": 0,
        "rx_overruns": 0,
        "rx_frame": 0,
        "tx_packets": 73,
        "tx_bytes": 6009,
        "tx_errors": 0,
        "tx_dropped": 0,
        "tx_overruns": 0,
        "tx_carrier": 0,
        "tx_collisions": 0,
        "metric": null
      }
    ]

    $ ifconfig | jc --ifconfig -p -r
    [
      {
        "name": "ens33",
        "flags": "4163",
        "state": "UP,BROADCAST,RUNNING,MULTICAST",
        "mtu": "1500",
        "ipv4_addr": "192.168.71.137",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": "64",
        "ipv6_scope": "0x20",
        "mac_addr": "00:0c:29:3b:58:0e",
        "type": "Ethernet",
        "rx_packets": "8061",
        "rx_bytes": "1514413",
        "rx_errors": "0",
        "rx_dropped": "0",
        "rx_overruns": "0",
        "rx_frame": "0",
        "tx_packets": "4502",
        "tx_bytes": "866622",
        "tx_errors": "0",
        "tx_dropped": "0",
        "tx_overruns": "0",
        "tx_carrier": "0",
        "tx_collisions": "0",
        "metric": null
      },
      {
        "name": "lo",
        "flags": "73",
        "state": "UP,LOOPBACK,RUNNING",
        "mtu": "65536",
        "ipv4_addr": "127.0.0.1",
        "ipv4_mask": "255.0.0.0",
        "ipv4_bcast": null,
        "ipv6_addr": "::1",
        "ipv6_mask": "128",
        "ipv6_scope": "0x10",
        "mac_addr": null,
        "type": "Local Loopback",
        "rx_packets": "73",
        "rx_bytes": "6009",
        "rx_errors": "0",
        "rx_dropped": "0",
        "rx_overruns": "0",
        "rx_frame": "0",
        "tx_packets": "73",
        "tx_bytes": "6009",
        "tx_errors": "0",
        "tx_dropped": "0",
        "tx_overruns": "0",
        "tx_carrier": "0",
        "tx_collisions": "0",
        "metric": null
      }
    ]

<a id="jc.parsers.ifconfig.parse"></a>

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

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, aix, freebsd, darwin

Version 1.12 by Kelly Brazil (kellyjonbrazil@gmail.com)
