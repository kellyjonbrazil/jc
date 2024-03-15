[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_vmallocinfo"></a>

# jc.parsers.proc_vmallocinfo

jc - JSON Convert `/proc/vmallocinfo` file parser

This parser will attempt to convert number values to integers. If that is
not desired, please use the `--raw` option (cli) or `raw=True` argument
(module).

Usage (cli):

    $ cat /proc/vmallocinfo | jc --proc

or

    $ jc /proc/vmallocinfo

or

    $ cat /proc/vmallocinfo | jc --proc-vmallocinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_vmallocinfo_file)

or

    import jc
    result = jc.parse('proc_vmallocinfo', proc_vmallocinfo_file)

Schema:

    [
      {
        "start":                  string,
        "end":                    string,
        "size":                   integer,
        "caller":                 string,
        "options": [
                                  string
        ],
        "phys":                   string
        "pages":                  integer,
        "N<id>":                  integer
      }
    ]

Examples:

    $ cat /proc/vmallocinfo | jc --proc -p
    [
      {
        "start": "0xffffb3c1c0000000",
        "end": "0xffffb3c1c0005000",
        "size": 20480,
        "caller": "map_irq_stack+0x93/0xe0",
        "options": [
          "vmap"
        ],
        "phys": "0x00000000bfefe000"
      },
      {
        "start": "0xffffb3c1c0005000",
        "end": "0xffffb3c1c0007000",
        "size": 8192,
        "caller": "acpi_os_map_iomem+0x1ac/0x1c0",
        "options": [
          "ioremap"
        ],
        "phys": "0x00000000bfeff000"
      },
      ...
    ]

    $ cat /proc/vmallocinfo | jc --proc-vmallocinfo -p -r
    [
      {
        "start": "0xffffb3c1c0000000",
        "end": "0xffffb3c1c0005000",
        "size": "20480",
        "caller": "map_irq_stack+0x93/0xe0",
        "options": [
          "vmap"
        ],
        "phys": "0x00000000bfefe000"
      },
      {
        "start": "0xffffb3c1c0005000",
        "end": "0xffffb3c1c0007000",
        "size": "8192",
        "caller": "acpi_os_map_iomem+0x1ac/0x1c0",
        "options": [
          "ioremap"
        ],
        "phys": "0x00000000bfeff000"
      },
      ...
    ]

<a id="jc.parsers.proc_vmallocinfo.parse"></a>

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

Source: [`jc/parsers/proc_vmallocinfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_vmallocinfo.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
