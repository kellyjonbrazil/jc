[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.zpool_status"></a>

# jc.parsers.zpool_status

jc - JSON Convert `zpool status` command output parser

Works with or without the `-v` option.

Usage (cli):

    $ zpool status | jc --zpool-status

or

    $ jc zpool status

Usage (module):

    import jc
    result = jc.parse('zpool_status', zpool_status_command_output)

Schema:

    [
      {
        "pool":                               string,
        "state":                              string,
        "status":                             string,
        "action":                             string,
        "see":                                string,
        "scan":                               string,
        "scrub":                              string,
        "config": [
          {
            "name":                           string,
            "state":                          string/null,
            "read":                           integer/null,
            "write":                          integer/null,
            "checksum":                       integer/null,
            "errors":                         string/null,
          }
        ],
        "errors":                             string
      }
    ]

Examples:

    $ zpool status -v | jc --zpool-status -p
    [
      {
        "pool": "tank",
        "state": "DEGRADED",
        "status": "One or more devices could not be opened.  Suffic...",
        "action": "Attach the missing device and online it using 'zpool...",
        "see": "http://www.sun.com/msg/ZFS-8000-2Q",
        "scrub": "none requested",
        "config": [
          {
            "name": "tank",
            "state": "DEGRADED",
            "read": 0,
            "write": 0,
            "checksum": 0
          },
          {
            "name": "mirror-0",
            "state": "DEGRADED",
            "read": 0,
            "write": 0,
            "checksum": 0
          },
          {
            "name": "c1t0d0",
            "state": "ONLINE",
            "read": 0,
            "write": 0,
            "checksum": 0
          },
          {
            "name": "c1t1d0",
            "state": "UNAVAIL",
            "read": 0,
            "write": 0,
            "checksum": 0,
            "errors": "cannot open"
          }
        ],
        "errors": "No known data errors"
      }
    ]

    $ zpool status -v | jc --zpool-status -p -r
    [
      {
        "pool": "tank",
        "state": "DEGRADED",
        "status": "One or more devices could not be opened.  Sufficient...",
        "action": "Attach the missing device and online it using 'zpool...",
        "see": "http://www.sun.com/msg/ZFS-8000-2Q",
        "scrub": "none requested",
        "config": [
          {
            "name": "tank",
            "state": "DEGRADED",
            "read": "0",
            "write": "0",
            "checksum": "0"
          },
          {
            "name": "mirror-0",
            "state": "DEGRADED",
            "read": "0",
            "write": "0",
            "checksum": "0"
          },
          {
            "name": "c1t0d0",
            "state": "ONLINE",
            "read": "0",
            "write": "0",
            "checksum": "0"
          },
          {
            "name": "c1t1d0",
            "state": "UNAVAIL",
            "read": "0",
            "write": "0",
            "checksum": "0",
            "errors": "cannot open"
          }
        ],
        "errors": "No known data errors"
      }
    ]

<a id="jc.parsers.zpool_status.parse"></a>

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
Compatibility:  linux, darwin, freebsd

Source: [`jc/parsers/zpool_status.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/zpool_status.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
