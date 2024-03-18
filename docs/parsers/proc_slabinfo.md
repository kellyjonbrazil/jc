[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_slabinfo"></a>

# jc.parsers.proc_slabinfo

jc - JSON Convert `/proc/slabinfo` file parser

Usage (cli):

    $ cat /proc/slabinfo | jc --proc

or

    $ jc /proc/slabinfo

or

    $ cat /proc/slabinfo | jc --proc-slabinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_slabinfo_file)

or

    import jc
    result = jc.parse('proc_slabinfo', proc_slabinfo_file)

Schema:

    [
      {
        "name":                             string,
        "active_objs":                      integer,
        "num_objs":                         integer,
        "obj_size":                         integer,
        "obj_per_slab":                     integer,
        "pages_per_slab":                   integer,
        "tunables": {
          "limit":                          integer,
          "batch_count":                    integer,
          "shared_factor":                  integer
        },
        "slabdata": {
          "active_slabs":                   integer,
          "num_slabs":                      integer,
          "shared_avail":                   integer
      }
    ]

Examples:

    $ cat /proc/slabinfo | jc --proc -p
    [
      {
        "name": "ext4_groupinfo_4k",
        "active_objs": 224,
        "num_objs": 224,
        "obj_size": 144,
        "obj_per_slab": 56,
        "pages_per_slab": 2,
        "tunables": {
          "limit": 0,
          "batch_count": 0,
          "shared_factor": 0
        },
        "slabdata": {
          "active_slabs": 4,
          "num_slabs": 4,
          "shared_avail": 0
        }
      },
      ...
    ]

<a id="jc.parsers.proc_slabinfo.parse"></a>

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

Source: [`jc/parsers/proc_slabinfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_slabinfo.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
