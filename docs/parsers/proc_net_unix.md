[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_unix"></a>

# jc.parsers.proc_net_unix

jc - JSON Convert `/proc/net/unix` file parser

Usage (cli):

    $ cat /proc/net/unix | jc --proc

or

    $ jc /proc/net/unix

or

    $ cat /proc/net/unix | jc --proc-net-unix

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_unix_file)

or

    import jc
    result = jc.parse('proc_net_unix', proc_net_unix_file)

Schema:

    [
      {
        "Num":                    string,
        "RefCount":               string,
        "Protocol":               string,
        "Flags":                  string,
        "Type":                   string,
        "St":                     string,
        "Inode":                  integer,
        "Path":                   string
      }
  ]

Examples:

    $ cat /proc/net/unix | jc --proc -p
    [
      {
        "Num": "ffff9b61ac49c400:",
        "RefCount": "00000002",
        "Protocol": "00000000",
        "Flags": "00010000",
        "Type": "0001",
        "St": "01",
        "Inode": 42776,
        "Path": "/var/snap/lxd/common/lxd/unix.socket"
      },
      ...
    ]

    $ cat /proc/net/unix | jc --proc-net-unix -p -r
    [
      {
        "Num": "ffff9b61ac49c400:",
        "RefCount": "00000002",
        "Protocol": "00000000",
        "Flags": "00010000",
        "Type": "0001",
        "St": "01",
        "Inode": "42776",
        "Path": "/var/snap/lxd/common/lxd/unix.socket"
      },
      ...
    ]

<a id="jc.parsers.proc_net_unix.parse"></a>

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

Source: [`jc/parsers/proc_net_unix.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_unix.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
