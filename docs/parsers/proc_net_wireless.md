[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_wireless"></a>

# jc.parsers.proc_net_wireless

jc - JSON Convert `/proc/net/wireless` file parser

Usage (cli):

    $ cat /proc/net/wireless | jc --proc

or

    $ jc /proc/net/wireless

or

    $ cat /proc/net/wireless | jc --proc-net-wireless

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_wireless_file)

or

    import jc
    result = jc.parse('proc_net_wireless', proc_net_wireless_file)

Schema:

    [
      {
        "interface":                  string,
        "status":                     integer,
        "quality_link":               integer,
        "quality_link_updated":       boolean,
        "quality_level":              integer,
        "quality_level_updated":      boolean,
        "quality_noise":              integer,
        "quality_noise_updated":      boolean,
        "discarded_nwid":             integer,
        "discarded_crypt":            integer,
        "discarded_frag":             integer,
        "discarded_retry":            integer,
        "discarded_misc":             integer,
        "missed_beacon":              integer
      }
    ]

Examples:

    $ cat /proc/net/wireless | jc --proc -p
    [
      {
        "interface": "wlp0s20f3",
        "status": 0,
        "quality_link": 58,
        "quality_link_updated": true,
        "quality_level": -52,
        "quality_level_updated": true,
        "quality_noise": -256,
        "quality_noise_updated": false,
        "discarded_nwid": 0,
        "discarded_crypt": 0,
        "discarded_frag": 0,
        "discarded_retry": 12,
        "discarded_misc": 7,
        "missed_beacon": 0
      },
      {
        "interface": "wlan1",
        "status": 10,
        "quality_link": 70,
        "quality_link_updated": true,
        "quality_level": -40,
        "quality_level_updated": true,
        "quality_noise": -95,
        "quality_noise_updated": true,
        "discarded_nwid": 3,
        "discarded_crypt": 1,
        "discarded_frag": 0,
        "discarded_retry": 1543,
        "discarded_misc": 210,
        "missed_beacon": 18
      }
    ]

    $ cat /proc/net/wireless | jc --proc-net-wireless -p -r
    [
      {
        "interface": "wlp0s20f3",
        "status": "0000",
        "quality_link": "58.",
        "quality_level": "-52.",
        "quality_noise": "-256",
        "discarded_nwid": "0",
        "discarded_crypt": "0",
        "discarded_frag": "0",
        "discarded_retry": "12",
        "discarded_misc": "7",
        "missed_beacon": "0"
      },
      {
        "interface": "wlan1",
        "status": "000a",
        "quality_link": "70.",
        "quality_level": "-40.",
        "quality_noise": "-95.",
        "discarded_nwid": "3",
        "discarded_crypt": "1",
        "discarded_frag": "0",
        "discarded_retry": "1543",
        "discarded_misc": "210",
        "missed_beacon": "18"
      }
    ]

<a id="jc.parsers.proc_net_wireless.parse"></a>

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

Source: [`jc/parsers/proc_net_wireless.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_wireless.py)

Version 1.0 by Michael Klemm (MichaelKlemm@users.noreply.github.com)
