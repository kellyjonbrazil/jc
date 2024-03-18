[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.iwconfig"></a>

# jc.parsers.iwconfig

jc - JSON Convert `iwconfig` command output parser

No `iwconfig` options are supported.

Usage (cli):

    $ iwconfig | jc --iwconfig

or

    $ jc iwconfig

Usage (module):

    import jc
    result = jc.parse('iwconfig', iwconfig_command_output)

Schema:

    [
        {
            "name":                         string,
            "protocol":                     string,
            "essid":                        string,
            "mode":                         string,
            "frequency":                    float,
            "frequency_unit":               string,
            "access_point":                 string,
            "bit_rate":                     float,
            "bit_rate_unit":                string,
            "tx_power":                     integer,
            "tx_power_unit":                string,
            "retry_short_limit":            integer,
            "rts_threshold":                boolean,
            "fragment_threshold":           boolean,
            "power_management":             boolean,
            "link_quality":                 string,
            "signal_level":                 integer,
            "signal_level_unit":            string,
            "rx_invalid_nwid":              integer,
            "rx_invalid_crypt":             integer,
            "rx_invalid_frag":              integer,
            "tx_excessive_retries":         integer,
            "invalid_misc":                 integer,
            "missed_beacon":                integer
        }
    ]

Examples:

    $  iwconfig | jc --iwconfig -p
    [
      {
        "name": "wlp5s0",
        "protocol": "IEEE 802.11",
        "essid": "BLABLABLA",
        "mode": "Managed",
        "frequency": 5.18,
        "frequency_unit": "GHz",
        "access_point": "E6:64:DA:16:51:BF",
        "bit_rate": 6.0,
        "bit_rate_unit": "Mb/s",
        "tx_power": 30,
        "tx_power_unit": "dBm",
        "retry_short_limit": 7,
        "rts_threshold": false,
        "fragment_threshold": false,
        "power_management": true,
        "link_quality": "61/70",
        "signal_level": -49,
        "signal_level_unit": "dBm",
        "rx_invalid_nwid": 0,
        "rx_invalid_crypt": 0,
        "rx_invalid_frag": 0,
        "tx_excessive_retries": 0,
        "invalid_misc": 2095,
        "missed_beacon": 0
      }
    ]

<a id="jc.parsers.iwconfig.parse"></a>

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
Compatibility:  linux

Source: [`jc/parsers/iwconfig.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/iwconfig.py)

Version 1.2 by Thomas Vincent (vrince@gmail.com)
