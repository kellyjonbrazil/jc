[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.zpool_iostat"></a>

# jc.parsers.zpool_iostat

jc - JSON Convert `zpool iostat` command output parser

Supports with or without the `-v` flag.

Usage (cli):

    $ zpool iostat | jc --zpool-iostat

or

    $ jc zpool iostat

Usage (module):

    import jc
    result = jc.parse('zpool_iostat', zpool_iostat_command_output)

Schema:

    [
      {
        "pool":                     string,
        "parent":                   string,
        "cap_alloc":                float,
        "cap_alloc_unit":           string,
        "cap_free":                 float,
        "cap_free_unit":            string,
        "ops_read":                 integer,
        "ops_write":                integer,
        "bw_read":                  float,
        "bw_read_unit":             string,
        "bw_write":                 float,
        "bw_write_unit":            string
      }
    ]

Examples:

    $ zpool iostat -v | jc --zpool-iostat -p
    [
      {
        "pool": "zhgstera6",
        "cap_alloc": 2.89,
        "cap_free": 2.2,
        "ops_read": 0,
        "ops_write": 2,
        "bw_read": 349.0,
        "bw_write": 448.0,
        "cap_alloc_unit": "T",
        "cap_free_unit": "T",
        "bw_read_unit": "K",
        "bw_write_unit": "K"
      },
      {
        "pool": "726060ALE614-K8JAPRGN:10",
        "parent": "zhgstera6",
        "cap_alloc": 2.89,
        "cap_free": 2.2,
        "ops_read": 0,
        "ops_write": 2,
        "bw_read": 349.0,
        "bw_write": 448.0,
        "cap_alloc_unit": "T",
        "cap_free_unit": "T",
        "bw_read_unit": "K",
        "bw_write_unit": "K"
      },
      ...
    ]

    $ zpool iostat -v | jc --zpool-iostat -p -r
    [
      {
        "pool": "zhgstera6",
        "cap_alloc": "2.89T",
        "cap_free": "2.20T",
        "ops_read": "0",
        "ops_write": "2",
        "bw_read": "349K",
        "bw_write": "448K"
      },
      {
        "pool": "726060ALE614-K8JAPRGN:10",
        "parent": "zhgstera6",
        "cap_alloc": "2.89T",
        "cap_free": "2.20T",
        "ops_read": "0",
        "ops_write": "2",
        "bw_read": "349K",
        "bw_write": "448K"
      },
      ...
    ]

<a id="jc.parsers.zpool_iostat.parse"></a>

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

Source: [`jc/parsers/zpool_iostat.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/zpool_iostat.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
