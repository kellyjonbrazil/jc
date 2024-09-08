[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ethtool"></a>

# jc.parsers.ethtool

jc - JSON Convert `ethtool` command output parser

Supports standard `ethtool` output and the `--module-info` option.

Usage (cli):

    $ ethtool <interface> | jc --ethtool
    $ ethtool --module-info <interface> | jc --ethtool

or

    $ jc ethtool <interface>
    $ jc ethtool --module-info <interface>

Usage (module):

    import jc
    result = jc.parse('ethtool', ethtool_command_output)

Schema:

Note: many units fields are converted to integers and floats
when detected. Use raw output for the original string values.

    {
      "name":                               string,
      "supported_ports": [
                                            string
      ],
      "supported_link_modes": [
                                            string
      ],
      "supported_pause_frame_use":          string,
      "supports_auto_negotiation":          boolean,
      "supported_fec_modes": [
                                            string
      ],
      "advertised_link_modes": [
                                            string
      ],
      "advertised_pause_frame_use":         boolean,
      "advertised_auto_negotiation":        boolean,
      "advertised_fec_modes": [
                                            string
      ],
      "speed":                              string,
      "speed_bps":                          integer,
      "duplex":                             string,
      "auto_negotiation":                   boolean,
      "port":                               string,
      "phyad":                              string,
      "mdi_x":                              string,
      "transceiver":                        string,
      "supports_wake_on":                   string,
      "wake_on":                            string,
      "current_message_level": [
                                            string
      ],
      "link_detected":                      boolean,
      "identifier":                         string,
      "extended_identifier":                string,
      "connector":                          string,
      "transceiver_codes":                  string,
      "transceiver_type": [
                                            string
      ],
      "encoding":                           string,
      "br_nominal":                         string,
      "rate_identifier":                    string,
      "length_smf_km":                      string,
      "length_smf":                         string,
      "length_50um":                        string,
      "length_62_5um":                      string,
      "length_copper":                      string,
      "length_om3":                         string,
      "passive_cu_cmplnce":                 string,
      "vendor_name":                        string,
      "vendor_oui":                         string,
      "vendor_pn":                          string,
      "vendor_rev":                         string,
      "option_values":                      string,
      "br_margin_max":                      string,
      "br_margin_min":                      string
    }

Examples:

    $ ethtool enp0s3 | jc --ethtool -p
    {
      "name": "enp0s3",
      "supported_pause_frame_use": "No",
      "supports_auto_negotiation": true,
      "supported_fec_modes": "Not reported",
      "advertised_pause_frame_use": false,
      "advertised_auto_negotiation": true,
      "advertised_fec_modes": "Not reported",
      "speed": "1000Mb/s",
      "duplex": "Full",
      "port": "Twisted Pair",
      "phyad": "0",
      "transceiver": "internal",
      "auto_negotiation": false,
      "mdi_x": "off (auto)",
      "supports_wake_on": "umbg",
      "wake_on": "d",
      "link_detected": true,
      "supported_ports": [
        "TP"
      ],
      "supported_link_modes": [
        "10baseT/Half",
        "10baseT/Full",
        "100baseT/Half",
        "100baseT/Full",
        "1000baseT/Full"
      ],
      "advertised_link_modes": [
        "10baseT/Half",
        "10baseT/Full",
        "100baseT/Half",
        "100baseT/Full",
        "1000baseT/Full"
      ],
      "current_message_level": [
        "0x00000007 (7)",
        "drv probe link"
      ],
      "speed_bps": 1000000000
    }

    $ ethtool --module-info enp0s3 | jc --ethtool -p
    {
      "identifier": "0x03 (SFP)",
      "extended_identifier": "0x04 (GBIC/SFP defined by 2-wire interface ID)",
      "connector": "0x21 (Copper pigtail)",
      "transceiver_codes": "0x01 0x00 0x00 0x04 0x00 0x04 0x80 0xd5 0x00",
      "transceiver_type": [
        "Infiniband: 1X Copper Passive",
        "Ethernet: 1000BASE-CX",
        "Passive Cable",
        "FC: Twin Axial Pair (TW)",
        "FC: 1200 MBytes/sec",
        "FC: 800 MBytes/sec",
        "FC: 400 MBytes/sec",
        "FC: 200 MBytes/sec",
        "FC: 100 MBytes/sec"
      ],
      "encoding": "0x00 (unspecified)",
      "br_nominal": "10300MBd",
      "rate_identifier": "0x00 (unspecified)",
      "length_smf_km": "0km",
      "length_smf": "0m",
      "length_50um": "0m",
      "length_62_5um": "0m",
      "length_copper": "2m",
      "length_om3": "0m",
      "passive_cu_cmplnce": "0x01 (SFF-8431 appendix E) [SFF-8472 rev10.4 only]",
      "vendor_name": "UbiquitiNetworks",
      "vendor_oui": "00:40:20",
      "vendor_pn": "UDC-2",
      "vendor_rev": "",
      "option_values": "0x00 0x00",
      "br_margin_max": "0%",
      "br_margin_min": "0%"
    }

<a id="jc.parsers.ethtool.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]
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

Source: [`jc/parsers/ethtool.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ethtool.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
