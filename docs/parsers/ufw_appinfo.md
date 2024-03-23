[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ufw_appinfo"></a>

# jc.parsers.ufw_appinfo

jc - JSON Convert `ufw app info [application]` command
output parser

Supports individual apps via `ufw app info [application]` and all apps list
via `ufw app info all`.

Because `ufw` application definitions allow overlapping ports and port
ranges, this parser preserves that behavior, but also provides `normalized`
lists and ranges that remove duplicate ports and merge overlapping ranges.

Usage (cli):

    $ ufw app info OpenSSH | jc --ufw-appinfo

or

    $ jc ufw app info OpenSSH

Usage (module):

    import jc
    result = jc.parse('ufw_appinfo', ufw_appinfo_command_output)

Schema:

    [
      {
        "profile":                  string,
        "title":                    string,
        "description":              string,
        "tcp_list": [
                                    integer
        ],
        "tcp_ranges": [
          {
            "start":                integer,      # [0]
            "end":                  integer
          }
        ],
        "udp_list": [
                                    integer
        ],
        "udp_ranges": [
          {
            "start":                integer,      # [0]
            "end":                  integer
          }
        ],
        "normalized_tcp_list": [
                                    integers      # [1]
        ],
        "normalized_tcp_ranges": [
          {
            "start":                integer,      # [0]
            "end":                  integers      # [2]
          }
        ],
        "normalized_udp_list": [
                                    integers      # [1]
        ],
        "normalized_udp_ranges": [
          {
            "start":                integer,      # [0]
            "end":                  integers      # [2]
          }
        ]
      }
    ]

    [0] 'any' is converted to start/end: 0/65535
    [1] duplicates and overlapping are removed
    [2] overlapping are merged

Examples:

    $ ufw app info MSN | jc --ufw-appinfo -p
    [
      {
        "profile": "MSN",
        "title": "MSN Chat",
        "description": "MSN chat protocol (with file transfer and voice)",
        "tcp_list": [
          1863,
          6901
        ],
        "udp_list": [
          1863,
          6901
        ],
        "tcp_ranges": [
          {
            "start": 6891,
            "end": 6900
          }
        ],
        "normalized_tcp_list": [
          1863,
          6901
        ],
        "normalized_tcp_ranges": [
          {
            "start": 6891,
            "end": 6900
          }
        ],
        "normalized_udp_list": [
          1863,
          6901
        ]
      }
    ]

    $ ufw app info MSN | jc --ufw-appinfo -p -r
    [
      {
        "profile": "MSN",
        "title": "MSN Chat",
        "description": "MSN chat protocol (with file transfer and voice)",
        "tcp_list": [
          "1863",
          "6901"
        ],
        "udp_list": [
          "1863",
          "6901"
        ],
        "tcp_ranges": [
          {
            "start": "6891",
            "end": "6900"
          }
        ]
      }
    ]

<a id="jc.parsers.ufw_appinfo.parse"></a>

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

Source: [`jc/parsers/ufw_appinfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ufw_appinfo.py)

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
