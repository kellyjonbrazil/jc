[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_netlink"></a>

# jc.parsers.proc_net_netlink

jc - JSON Convert `/proc/net/netlink` file parser

Usage (cli):

    $ cat /proc/net/netlink | jc --proc

or

    $ jc /proc/net/netlink

or

    $ cat /proc/net/netlink | jc --proc-net-netlink

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_netlink_file)

or

    import jc
    result = jc.parse('proc_net_netlink', proc_net_netlink_file)

Schema:

    [
      {
        "sk":                       string,
        "Eth":                      integer,
        "Pid":                      integer,
        "Groups":                   string,
        "Rmem":                     integer,
        "Wmem":                     integer,
        "Dump":                     integer,
        "Locks":                    integer,
        "Drops":                    integer,
        "Inode":                    integer
      }
    ]

Examples:

    $ cat /proc/net/netlink | jc --proc -p
    [
      {
        "sk": "ffff9b61adaff000",
        "Eth": 0,
        "Pid": 1,
        "Groups": "800405d5",
        "Rmem": 0,
        "Wmem": 0,
        "Dump": 0,
        "Locks": 2,
        "Drops": 0,
        "Inode": 29791
      },
      {
        "sk": "ffff9b61a792a000",
        "Eth": 0,
        "Pid": 837,
        "Groups": "00000111",
        "Rmem": 0,
        "Wmem": 0,
        "Dump": 0,
        "Locks": 2,
        "Drops": 0,
        "Inode": 35337
      },
      ...
    ]

    $ cat /proc/net/netlink | jc --proc-net-netlink -p -r
    [
      {
        "sk": "ffff9b61adaff000",
        "Eth": "0",
        "Pid": "1",
        "Groups": "800405d5",
        "Rmem": "0",
        "Wmem": "0",
        "Dump": "0",
        "Locks": "2",
        "Drops": "0",
        "Inode": "29791"
      },
      {
        "sk": "ffff9b61a792a000",
        "Eth": "0",
        "Pid": "837",
        "Groups": "00000111",
        "Rmem": "0",
        "Wmem": "0",
        "Dump": "0",
        "Locks": "2",
        "Drops": "0",
        "Inode": "35337"
      },
      ...
    ]

<a id="jc.parsers.proc_net_netlink.parse"></a>

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

Source: [`jc/parsers/proc_net_netlink.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_netlink.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
