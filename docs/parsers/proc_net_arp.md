[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_arp"></a>

# jc.parsers.proc_net_arp

jc - JSON Convert `/proc/net/arp` file parser

Usage (cli):

    $ cat /proc/net/arp | jc --proc

or

    $ jc /proc/net/arp

or

    $ cat /proc/net/arp | jc --proc-net-arp

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_arp_file)

or

    import jc
    result = jc.parse('proc_net_arp', proc_net_arp_file)

Schema:

    [
      {
        "IP_address":           string,
        "HW_type":              string,
        "Flags":                string,
        "HW_address":           string,
        "Mask":                 string,
        "Device":               string
      }
    ]

Examples:

    $ cat /proc/net/arp | jc --proc -p
    [
      {
        "IP_address": "192.168.71.254",
        "HW_type": "0x1",
        "Flags": "0x2",
        "HW_address": "00:50:56:f3:2f:ae",
        "Mask": "*",
        "Device": "ens33"
      },
      ...
    ]

<a id="jc.parsers.proc_net_arp.parse"></a>

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

Source: [`jc/parsers/proc_net_arp.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_arp.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
