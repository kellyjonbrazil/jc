# jc.parsers.lsmod
jc - JSON CLI output utility lsmod Parser

Usage:
    specify --lsmod as the first argument if the piped input is coming from lsmod

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

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    dictionary   structured data with the following schema:

    [
      {
        "module": string,
        "size":   integer,
        "used":   integer,
        "by": [
                  string
        ]
      }
    ]

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

    dictionary   raw or processed structured data

