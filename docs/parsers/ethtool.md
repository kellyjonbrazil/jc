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

    $ ethtool | jc --ethtool -p
    []

    $ ethtool | jc --ethtool -p -r
    []

<a id="jc.parsers.ethtool.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> JSONDictType
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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
