[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.hciconfig"></a>

# jc.parsers.hciconfig

jc - JSON Convert `hciconfig` command output parser

Usage (cli):

    $ hciconfig | jc --hciconfig

or

    $ jc hciconfig

Usage (module):

    import jc
    result = jc.parse('hciconfig', hciconfig_command_output)

Schema:

    [
      {
        "device":               string,
        "type":                 string,
        "bus":                  string,
        "bd_address":           string,
        "acl_mtu":              integer,
        "acl_mtu_packets":      integer,
        "sco_mtu":              integer,
        "sco_mtu_packets":      integer,
        "state": [
                                string
        ],
        "rx_bytes":             integer,
        "rx_acl":               integer,
        "rx_sco":               integer,
        "rx_events":            integer,
        "rx_errors":            integer,
        "tx_bytes":             integer,
        "tx_acl":               integer,
        "tx_sco":               integer,
        "tx_commands":          integer,
        "tx_errors":            integer,
        "features": [
                                string
        ],
        "packet_type": [
                                string
        ],
        "link_policy": [
                                string
        ],
        "link_mode": [
                                string
        ],
        "name":                 string,
        "class":                string,
        "service_classes": [
                                string       # 'Unspecified' is null
        ],
        "device_class":         string,
        "hci_version":          string,
        "hci_revision":         string,
        "lmp_version":          string,
        "lmp_subversion":       string,
        "manufacturer":         string
      }
    ]

Examples:

    $ hciconfig -a | jc --hciconfig -p
    [
      {
        "device": "hci0",
        "type": "Primary",
        "bus": "USB",
        "bd_address": "00:1A:7D:DA:71:13",
        "acl_mtu": 310,
        "acl_mtu_packets": 10,
        "sco_mtu": 64,
        "sco_mtu_packets": 8,
        "state": [
          "UP",
          "RUNNING"
        ],
        "rx_bytes": 13905869,
        "rx_acl": 0,
        "rx_sco": 0,
        "rx_events": 393300,
        "rx_errors": 0,
        "tx_bytes": 62629,
        "tx_acl": 0,
        "tx_sco": 0,
        "tx_commands": 3893,
        "tx_errors": 0,
        "features": [
          "0xff",
          "0xff",
          "0x8f",
          "0xfe",
          "0xdb",
          "0xff",
          "0x5b",
          "0x87"
        ],
        "packet_type": [
          "DM1",
          "DM3",
          "DM5",
          "DH1",
          "DH3",
          "DH5",
          "HV1",
          "HV2",
          "HV3"
        ],
        "link_policy": [
          "RSWITCH",
          "HOLD",
          "SNIFF",
          "PARK"
        ],
        "link_mode": [
          "SLAVE",
          "ACCEPT"
        ],
        "name": "CSR8510 A10",
        "class": "0x000000",
        "service_classes": null,
        "device_class": "Miscellaneous",
        "hci_version": "4.0 (0x6)",
        "hci_revision": "0x22bb",
        "lmp_version": "4.0 (0x6)",
        "lmp_subversion": "0x22bb",
        "manufacturer": "Cambridge Silicon Radio (10)"
      },
      {
        "device": "hci1",
        "type": "Primary",
        "bus": "USB",
        "bd_address": "00:1A:7D:DA:71:13",
        "acl_mtu": 310,
        "acl_mtu_packets": 10,
        "sco_mtu": 64,
        "sco_mtu_packets": 8,
        "state": [
          "DOWN"
        ],
        "rx_bytes": 4388363,
        "rx_acl": 0,
        "rx_sco": 0,
        "rx_events": 122021,
        "rx_errors": 0,
        "tx_bytes": 52350,
        "tx_acl": 0,
        "tx_sco": 0,
        "tx_commands": 3480,
        "tx_errors": 2,
        "features": [
          "0xff",
          "0xff",
          "0x8f",
          "0xfe",
          "0xdb",
          "0xff",
          "0x5b",
          "0x87"
        ],
        "packet_type": [
          "DM1",
          "DM3",
          "DM5",
          "DH1",
          "DH3",
          "DH5",
          "HV1",
          "HV2",
          "HV3"
        ],
        "link_policy": [
          "RSWITCH",
          "HOLD",
          "SNIFF",
          "PARK"
        ],
        "link_mode": [
          "SLAVE",
          "ACCEPT"
        ]
      }
    ]

    $ hciconfig -a | jc --hciconfig -p -r
    [
      {
        "device": "hci0",
        "type": "Primary",
        "bus": "USB",
        "bd_address": "00:1A:7D:DA:71:13",
        "acl_mtu": "310",
        "acl_mtu_packets": "10",
        "sco_mtu": "64",
        "sco_mtu_packets": "8",
        "state": [
          "UP",
          "RUNNING"
        ],
        "rx_bytes": "13905869",
        "rx_acl": "0",
        "rx_sco": "0",
        "rx_events": "393300",
        "rx_errors": "0",
        "tx_bytes": "62629",
        "tx_acl": "0",
        "tx_sco": "0",
        "tx_commands": "3893",
        "tx_errors": "0",
        "features": [
          "0xff",
          "0xff",
          "0x8f",
          "0xfe",
          "0xdb",
          "0xff",
          "0x5b",
          "0x87"
        ],
        "packet_type": [
          "DM1",
          "DM3",
          "DM5",
          "DH1",
          "DH3",
          "DH5",
          "HV1",
          "HV2",
          "HV3"
        ],
        "link_policy": [
          "RSWITCH",
          "HOLD",
          "SNIFF",
          "PARK"
        ],
        "link_mode": [
          "SLAVE",
          "ACCEPT"
        ],
        "name": "CSR8510 A10",
        "class": "0x000000",
        "service_classes": [
          "Unspecified"
        ],
        "device_class": "Miscellaneous",
        "hci_version": "4.0 (0x6)",
        "hci_revision": "0x22bb",
        "lmp_version": "4.0 (0x6)",
        "lmp_subversion": "0x22bb",
        "manufacturer": "Cambridge Silicon Radio (10)"
      },
      {
        "device": "hci1",
        "type": "Primary",
        "bus": "USB",
        "bd_address": "00:1A:7D:DA:71:13",
        "acl_mtu": "310",
        "acl_mtu_packets": "10",
        "sco_mtu": "64",
        "sco_mtu_packets": "8",
        "state": [
          "DOWN"
        ],
        "rx_bytes": "4388363",
        "rx_acl": "0",
        "rx_sco": "0",
        "rx_events": "122021",
        "rx_errors": "0",
        "tx_bytes": "52350",
        "tx_acl": "0",
        "tx_sco": "0",
        "tx_commands": "3480",
        "tx_errors": "2",
        "features": [
          "0xff",
          "0xff",
          "0x8f",
          "0xfe",
          "0xdb",
          "0xff",
          "0x5b",
          "0x87"
        ],
        "packet_type": [
          "DM1",
          "DM3",
          "DM5",
          "DH1",
          "DH3",
          "DH5",
          "HV1",
          "HV2",
          "HV3"
        ],
        "link_policy": [
          "RSWITCH",
          "HOLD",
          "SNIFF",
          "PARK"
        ],
        "link_mode": [
          "SLAVE",
          "ACCEPT"
        ]
      }
    ]

<a id="jc.parsers.hciconfig.parse"></a>

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
Compatibility:  linux

Source: [`jc/parsers/hciconfig.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/hciconfig.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
