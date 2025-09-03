[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.iw_scan"></a>

# jc.parsers.iw_scan

jc - JSON Convert `iw dev <device> scan` command output parser

This parser is considered beta quality. Not all fields are parsed and there
are not enough samples to test.

Usage (cli):

    $ iw dev wlan0 scan | jc --iw-scan

or

    $ jc iw dev wlan0 scan

Usage (module):

    import jc
    result = jc.parse('iw_scan', iw_scan_command_output)

Schema:

    [
      {
        "foo":     string/integer/float,      # best guess based on value
        "bar":     string/integer/float,
        "baz":     string/integer/float
      }
    ]

Examples:

    $ iw dev wlan0 scan | jc --iw-scan -p
    [
      {
        "bssid": "71:31:72:65:e1:a2",
        "interface": "wlan0",
        "freq": 2462,
        "capability": "ESS Privacy ShortSlotTime (0x0411)",
        "ssid": "WLAN-1234",
        "supported_rates": [
          1.0,
          2.0,
          5.5,
          11.0,
          18.0,
          24.0,
          36.0,
          54.0
        ],
        "erp": "<no flags>",
        "erp_d4.0": "<no flags>",
        "rsn": "Version: 1",
        "group_cipher": "CCMP",
        "pairwise_ciphers": "CCMP",
        "authentication_suites": "PSK",
        "capabilities": "0x186c",
        "extended_supported_rates": [
          6.0,
          9.0,
          12.0,
          48.0
        ],
        "ht_rx_mcs_rate_indexes_supported": "0-15",
        "primary_channel": 11,
        "secondary_channel_offset": "no secondary",
        "rifs": 1,
        "ht_protection": "no",
        "non-gf_present": 1,
        "obss_non-gf_present": 0,
        "dual_beacon": 0,
        "dual_cts_protection": 0,
        "stbc_beacon": 0,
        "l-sig_txop_prot": 0,
        "pco_active": 0,
        "pco_phase": 0,
        "bss_width_channel_transition_delay_factor": 5,
        "extended_capabilities": "HT Information Exchange Supported",
        "wmm": "Parameter version 1",
        "be": "CW 15-1023, AIFSN 3",
        "bk": "CW 15-1023, AIFSN 7",
        "vi": "CW 7-15, AIFSN 2, TXOP 3008 usec",
        "vo": "CW 3-7, AIFSN 2, TXOP 1504 usec",
        "wps": "Version: 1.0",
        "wi-fi_protected_setup_state": "2 (Configured)",
        "selected_registrar": "0x0",
        "response_type": "3 (AP)",
        "uuid": "00000000-0000-0003-0000-75317074f1a2",
        "manufacturer": "Corporation",
        "model": "VGV8539JW",
        "model_number": "1.47.000",
        "serial_number": "J144024542",
        "primary_device_type": "6-0050f204-1",
        "device_name": "Wireless Router(WFA)",
        "config_methods": "Label, PBC",
        "rf_bands": "0x3",
        "tsf_usec": 212098649788,
        "sta_channel_width_mhz": 20,
        "passive_dwell_tus": 20,
        "active_dwell_tus": 10,
        "channel_width_trigger_scan_interval_s": 300,
        "scan_passive_total_per_channel_tus": 200,
        "scan_active_total_per_channel_tus": 20,
        "beacon_interval_tus": 100,
        "signal_dbm": -80.0,
        "last_seen_ms": 11420,
        "selected_rates": [
          1.0,
          2.0,
          5.5,
          11.0
        ],
        "obss_scan_activity_threshold_percent": 0.25,
        "ds_parameter_set_channel": 11,
        "max_amsdu_length_bytes": 7935,
        "minimum_rx_ampdu_time_spacing_usec": 16
      },
      ...
    ]

<a id="jc.parsers.iw_scan.parse"></a>

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

Source: [`jc/parsers/iw_scan.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/iw_scan.py)

Version 0.75 by Kelly Brazil (kellyjonbrazil@gmail.com)
