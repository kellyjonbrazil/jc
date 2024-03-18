[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_igmp"></a>

# jc.parsers.proc_net_igmp

jc - JSON Convert `/proc/net/igmp` file parser

Usage (cli):

    $ cat /proc/net/igmp | jc --proc

or

    $ jc /proc/net/igmp

or

    $ cat /proc/net/igmp | jc --proc-net-igmp

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_igmp_file)

or

    import jc
    result = jc.parse('proc_net_igmp', proc_net_igmp_file)

Schema:

    [
      {
        "index":                      integer,
        "device":                     string,
        "count":                      integer,
        "querier":                    string,
        "groups": [
          {
            "address":                string,
            "users":                  integer,
            "timer":                  string,
            "reporter":               integer
          }
        ]
      }
    ]

Examples:

    $ cat /proc/net/igmp | jc --proc -p
    [
      {
        "index": 0,
        "device": "lo",
        "count": 0,
        "querier": "V3",
        "groups": [
          {
            "address": "010000E0",
            "users": 1,
            "timer": "0:00000000",
            "reporter": 0
          }
        ]
      },
      {
        "index": 2,
        "device": "eth0",
        "count": 26,
        "querier": "V2",
        "groups": [
          {
            "address": "260301E0",
            "users": 1,
            "timer": "0:00000000",
            "reporter": 1
          },
          {
            "address": "9B0101E0",
            "users": 1,
            "timer": "0:00000000",
            "reporter": 1
          },
        ]
      }
      ...
    ]

    $ cat /proc/net/igmp | jc --proc-net-igmp -p -r
    [
      {
        "index": "0",
        "device": "lo",
        "count": "0",
        "querier": "V3",
        "groups": [
          {
            "address": "010000E0",
            "users": "1",
            "timer": "0:00000000",
            "reporter": "0"
          }
        ]
      },
      {
        "index": "2",
        "device": "eth0",
        "count": "26",
        "querier": "V2",
        "groups": [
          {
            "address": "260301E0",
            "users": "1",
            "timer": "0:00000000",
            "reporter": "1"
          },
          {
            "address": "9B0101E0",
            "users": "1",
            "timer": "0:00000000",
            "reporter": "1"
          },
        ]
      }
      ...
    }

<a id="jc.parsers.proc_net_igmp.parse"></a>

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

Source: [`jc/parsers/proc_net_igmp.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_igmp.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
