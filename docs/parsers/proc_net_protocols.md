[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_protocols"></a>

# jc.parsers.proc_net_protocols

jc - JSON Convert `/proc/net/protocols` file parser

Usage (cli):

    $ cat /proc/net/protocols | jc --proc

or

    $ jc /proc/net/protocols

or

    $ cat /proc/net/protocols | jc --proc-net-protocols

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_protocols_file)

or

    import jc
    result = jc.parse('proc_net_protocols', proc_net_protocols_file)

Schema:

    [
      {
        "protocol":                   string,
        "size":                       integer,
        "sockets":                    integer,
        "memory":                     integer,
        "press":                      string,
        "maxhdr":                     integer,
        "slab":                       boolean,
        "module":                     string,
        "cl":                         boolean,
        "co":                         boolean,
        "di":                         boolean,
        "ac":                         boolean,
        "io":                         boolean,
        "in":                         boolean,
        "de":                         boolean,
        "sh":                         boolean,
        "ss":                         boolean,
        "gs":                         boolean,
        "se":                         boolean,
        "re":                         boolean,
        "sp":                         boolean,
        "bi":                         boolean,
        "br":                         boolean,
        "ha":                         boolean,
        "uh":                         boolean,
        "gp":                         boolean,
        "em":                         boolean,
      }
    ]

Examples:

    $ cat /proc/net/protocols | jc --proc -p
    [
      {
        "protocol": "AF_VSOCK",
        "size": 1216,
        "sockets": 0,
        "memory": -1,
        "press": "NI",
        "maxhdr": 0,
        "slab": true,
        "module": "vsock",
        "cl": false,
        "co": false,
        "di": false,
        "ac": false,
        "io": false,
        "in": false,
        "de": false,
        "sh": false,
        "ss": false,
        "gs": false,
        "se": false,
        "re": false,
        "sp": false,
        "bi": false,
        "br": false,
        "ha": false,
        "uh": false,
        "gp": false,
        "em": false
      },
      ...
    ]

    $ cat /proc/net/protocols | jc --proc-net-protocols -p -r
    [
      {
        "protocol": "AF_VSOCK",
        "size": "1216",
        "sockets": "0",
        "memory": "-1",
        "press": "NI",
        "maxhdr": "0",
        "slab": "yes",
        "module": "vsock",
        "cl": "n",
        "co": "n",
        "di": "n",
        "ac": "n",
        "io": "n",
        "in": "n",
        "de": "n",
        "sh": "n",
        "ss": "n",
        "gs": "n",
        "se": "n",
        "re": "n",
        "sp": "n",
        "bi": "n",
        "br": "n",
        "ha": "n",
        "uh": "n",
        "gp": "n",
        "em": "n"
      },
      ...
    ]

<a id="jc.parsers.proc_net_protocols.parse"></a>

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

Source: [`jc/parsers/proc_net_protocols.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_protocols.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
