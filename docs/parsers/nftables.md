[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.nftables"></a>

# jc.parsers.nftables

jc - JSON Convert `nftables` command output parser

Parses `nft list ruleset`, `nft list tables`, and `nft list table <family>
<name>`, with or without `-a`.

Rules and set/map `elements` are kept as `nft` prints them, minus the
`# handle N` comment. Inline rule counters are also copied into
`counter_packets` and `counter_bytes`. Named `counter`, `quota`,
`flowtable`, `limit`, `secmark`, `synproxy`, and `ct` blocks are skipped.
`nft -j` and `nft monitor` output are not supported.

Usage (cli):

    $ nft list ruleset | jc --nftables

or

    $ jc nft list ruleset

Usage (module):

    import jc
    result = jc.parse('nftables', nft_command_output)

Schema:

    [
      {
        "family":                   string,
        "name":                     string,
        "handle":                   integer,    # [0]
        "comment":                  string,     # [1]
        "flags": [
                                    string
        ],
        "chains": [
          {
            "name":                 string,
            "handle":               integer,    # [0]
            "type":                 string,     # [2]
            "hook":                 string,     # [1]
            "devices": [
                                    string
            ],
            "priority":             string,     # [1]
            "policy":               string,     # [1]
            "comment":              string,     # [1]
            "rules": [
              {
                "rule":             string,
                "handle":           integer,    # [0]
                "counter_packets":  integer,    # [1]
                "counter_bytes":    integer     # [1]
              }
            ]
          }
        ],
        "sets": [
          {
            "name":                 string,
            "handle":               integer,    # [0]
            "type":                 string,     # [3]
            "flags": [
                                    string
            ],
            "timeout":              string,     # [1]
            "gc_interval":          string,     # [1]
            "size":                 integer,    # [1]
            "policy":               string,     # [1]
            "auto_merge":           boolean,
            "counter":              boolean,
            "comment":              string,     # [1]
            "elements": [
                                    string
            ]
          }
        ],
        "maps": [
          {
            # same fields as sets, plus:
            "value_type":           string      # [3]
          }
        ]
      }
    ]

    [0] null unless `-a` was used
    [1] null if not set
    [2] null for a regular chain
    [3] the `typeof` expression when the set or map is declared with
        `typeof` instead of `type`

Examples:

    $ nft -a list ruleset | jc --nftables -p
    [
      {
        "family": "inet",
        "name": "filter",
        "handle": 1,
        "comment": null,
        "flags": [],
        "chains": [
          {
            "name": "input",
            "handle": 1,
            "type": "filter",
            "hook": "input",
            "devices": [],
            "priority": "filter",
            "policy": "drop",
            "comment": null,
            "rules": [
              {
                "rule": "tcp dport 8080 counter packets 12 bytes 720 accept",
                "handle": 8,
                "counter_packets": 12,
                "counter_bytes": 720
              }
            ]
          }
        ],
        "sets": [],
        "maps": []
      }
    ]

    $ nft -a list ruleset | jc --nftables -p -r
    [
      {
        "family": "inet",
        "name": "filter",
        "handle": "1",
        "comment": null,
        "flags": [],
        "chains": [
          {
            "name": "input",
            "handle": "1",
            "type": "filter",
            "hook": "input",
            "devices": [],
            "priority": "filter",
            "policy": "drop",
            "comment": null,
            "rules": [
              {
                "rule": "tcp dport 8080 counter packets 12 bytes 720 accept",
                "handle": "8",
                "counter_packets": "12",
                "counter_bytes": "720"
              }
            ]
          }
        ],
        "sets": [],
        "maps": []
      }
    ]

<a id="jc.parsers.nftables.parse"></a>

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
Compatibility:  linux

Source: [`jc/parsers/nftables.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/nftables.py)

Version 1.1 by Tung Lam (53996158+tunglambk@users.noreply.github.com)
