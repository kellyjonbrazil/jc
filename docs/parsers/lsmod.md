[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.lsmod
jc - JSON CLI output utility `lsmod` command output parser

Usage (cli):

    $ lsmod | jc --lsmod

    or

    $ jc lsmod

Usage (module):

    import jc
    result = jc.parse('lsmod', lsmod_command_output)

    or

    import jc.parsers.lsmod
    result = jc.parsers.lsmod.parse(lsmod_command_output)

Schema:

    [
      {
        "module":     string,
        "size":       integer,
        "used":       integer,
        "by": [
                      string
        ]
      }
    ]

Examples:

    $ lsmod | jc --lsmod -p
    [
      ...
      {
        "module": "nf_nat",
        "size": 26583,
        "used": 3,
        "by": [
          "nf_nat_ipv4",
          "nf_nat_ipv6",
          "nf_nat_masquerade_ipv4"
        ]
      },
      {
        "module": "iptable_mangle",
        "size": 12695,
        "used": 1
      },
      {
        "module": "iptable_security",
        "size": 12705,
        "used": 1
      },
      {
        "module": "iptable_raw",
        "size": 12678,
        "used": 1
      },
      {
        "module": "nf_conntrack",
        "size": 139224,
        "used": 7,
        "by": [
          "nf_nat",
          "nf_nat_ipv4",
          "nf_nat_ipv6",
          "xt_conntrack",
          "nf_nat_masquerade_ipv4",
          "nf_conntrack_ipv4",
          "nf_conntrack_ipv6"
        ]
      },
      ...
    ]

    $ lsmod | jc --lsmod -p -r
    [
      ...
      {
        "module": "nf_conntrack",
        "size": "139224",
        "used": "7",
        "by": [
          "nf_nat",
          "nf_nat_ipv4",
          "nf_nat_ipv6",
          "xt_conntrack",
          "nf_nat_masquerade_ipv4",
          "nf_conntrack_ipv4",
          "nf_conntrack_ipv6"
        ]
      },
      {
        "module": "ip_set",
        "size": "45799",
        "used": "0"
      },
      {
        "module": "nfnetlink",
        "size": "14519",
        "used": "1",
        "by": [
          "ip_set"
        ]
      },
      {
        "module": "ebtable_filter",
        "size": "12827",
        "used": "1"
      },
      {
        "module": "ebtables",
        "size": "35009",
        "used": "2",
        "by": [
          "ebtable_nat",
          "ebtable_filter"
        ]
      },
      ...
    ]


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux

Version 1.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
