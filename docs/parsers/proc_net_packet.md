[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_packet"></a>

# jc.parsers.proc_net_packet

jc - JSON Convert `/proc/net/packet` file parser

Usage (cli):

    $ cat /proc/net/packet | jc --proc

or

    $ jc /proc/net/packet

or

    $ cat /proc/net/packet | jc --proc-net-packet

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_packet_file)

or

    import jc
    result = jc.parse('proc_net_packet', proc_net_packet_file)

Schema:

    {
      "sk":                     string,
      "RefCnt":                 integer,
      "Type":                   integer,
      "Proto":                  string,
      "Iface":                  integer,
      "R":                      integer,
      "Rmem":                   integer,
      "User":                   integer,
      "Inode":                  integer
    }

Examples:

    $ cat /proc/net/packet | jc --proc -p
    {
      "sk": "ffff9b61b56c1800",
      "RefCnt": 3,
      "Type": 3,
      "Proto": "88cc",
      "Iface": 2,
      "R": 1,
      "Rmem": 0,
      "User": 101,
      "Inode": 34754
    }

    $ cat /proc/net/packet | jc --proc-net-packet -p -r
    {
      "sk": "ffff9b61b56c1800",
      "RefCnt": "3",
      "Type": "3",
      "Proto": "88cc",
      "Iface": "2",
      "R": "1",
      "Rmem": "0",
      "User": "101",
      "Inode": "34754"
    }

<a id="jc.parsers.proc_net_packet.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_net_packet.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_packet.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
