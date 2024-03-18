[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pagetypeinfo"></a>

# jc.parsers.proc_pagetypeinfo

jc - JSON Convert `/proc/pagetypeinfo` file parser

Usage (cli):

    $ cat /proc/pagetypeinfo | jc --proc

or

    $ jc /proc/pagetypeinfo

or

    $ cat /proc/pagetypeinfo | jc --proc-pagetypeinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_pagetypeinfo_file)

or

    import jc
    result = jc.parse('proc_pagetypeinfo', proc_pagetypeinfo_file)

Schema:

    {
      "page_block_order":             integer,
      "pages_per_block":              integer,
      "free_pages": [
        {
          "node":                     integer,
          "zone":                     string,
          "type":                     string,
          "free": [
                                      integer  # [0]
          ]
      ],
      "num_blocks_type": [
        {
          "node":                     integer,
          "zone":                     string,
          "unmovable":                integer,
          "movable":                  integer,
          "reclaimable":              integer,
          "high_atomic":              integer,
          "isolate":                  integer
        }
      ]
    }

    [0] array index correlates to the Order number.
        E.g. free[0] is the value for Order 0

Examples:

    $ cat /proc/pagetypeinfo | jc --proc -p
    {
      "page_block_order": 9,
      "pages_per_block": 512,
      "free_pages": [
        {
          "node": 0,
          "zone": "DMA",
          "type": "Unmovable",
          "free": [
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0
          ]
        },
        ...
      ],
      "num_blocks_type": [
        {
          "node": 0,
          "zone": "DMA",
          "unmovable": 1,
          "movable": 7,
          "reclaimable": 0,
          "high_atomic": 0,
          "isolate": 0
        },
        {
          "node": 0,
          "zone": "DMA32",
          "unmovable": 8,
          "movable": 1472,
          "reclaimable": 48,
          "high_atomic": 0,
          "isolate": 0
        },
        {
          "node": 0,
          "zone": "Normal",
          "unmovable": 120,
          "movable": 345,
          "reclaimable": 47,
          "high_atomic": 0,
          "isolate": 0
        }
      ]
    }

<a id="jc.parsers.proc_pagetypeinfo.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_pagetypeinfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pagetypeinfo.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
