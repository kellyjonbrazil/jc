[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_dev_mcast"></a>

# jc.parsers.proc_net_dev_mcast

jc - JSON Convert `/proc/net/dev_mcast` file parser

Usage (cli):

    $ cat /proc/net/dev_mcast | jc --proc

or

    $ jc /proc/net/dev_mcast

or

    $ cat /proc/net/dev_mcast | jc --proc-net-dev-mcast

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_dev_mcast_file)

or

    import jc
    result = jc.parse('proc_net_dev_mcast', proc_net_dev_mcast_file)

Schema:

    [
      {
        "index":                      integer,
        "interface":                  string,
        "dmi_u":                      integer,
        "dmi_g":                      integer,
        "dmi_address":                string
      }
    ]

Examples:

    $ cat /proc/net/dev_mcast | jc --proc -p
    [
      {
        "index": 2,
        "interface": "ens33",
        "dmi_u": 1,
        "dmi_g": 0,
        "dmi_address": "333300000001"
      },
      {
        "index": 2,
        "interface": "ens33",
        "dmi_u": 1,
        "dmi_g": 0,
        "dmi_address": "01005e000001"
      },
      ...
    ]

    $ cat /proc/net/dev_mcast | jc --proc-net-dev-mcast -p -r
    [
      {
        "index": "2",
        "interface": "ens33",
        "dmi_u": "1",
        "dmi_g": "0",
        "dmi_address": "333300000001"
      },
      {
        "index": "2",
        "interface": "ens33",
        "dmi_u": "1",
        "dmi_g": "0",
        "dmi_address": "01005e000001"
      },
      ...
    ]

<a id="jc.parsers.proc_net_dev_mcast.parse"></a>

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

Source: [`jc/parsers/proc_net_dev_mcast.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_dev_mcast.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
