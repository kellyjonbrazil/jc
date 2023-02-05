[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.zpool_status"></a>

# jc.parsers.zpool\_status

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
            "state":                          string,
            "read":                           integer,
            "write":                          integer,
            "checksum":                       integer,
            "errors":                         string,
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
        "status": "One or more devices could not be opened.  Sufficient replicas exist for\nthe pool to continue functioning in a degraded state.",
        "action": "Attach the missing device and online it using 'zpool online'.",
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
        "status": "One or more devices could not be opened.  Sufficient replicas exist for\nthe pool to continue functioning in a degraded state.",
        "action": "Attach the missing device and online it using 'zpool online'.",
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
          quiet: bool = False) -> List[JSONDictType]
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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
