[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_modules"></a>

# jc.parsers.proc_modules

jc - JSON Convert `/proc/modules` file parser

Usage (cli):

    $ cat /proc/modules | jc --proc

or

    $ jc /proc/modules

or

    $ cat /proc/modules | jc --proc-modules

Usage (module):

    import jc
    result = jc.parse('proc', proc_modules_file)

or

    import jc
    result = jc.parse('proc_modules', proc_modules_file)

Schema:

    [
      {
        "module":                   string,
        "size":                     integer,
        "used":                     integer,
        "used_by": [
                                    string
        ],
        "status":                   string,
        "location":                 string,
        "taint_state": [
                                    string
        ],
        "taint_state_verbose": [
                                    string
        ]
      }
    ]

Examples:

    $ cat /proc/modules | jc --proc -p
    [
      {
        "module": "i2c_piix4",
        "size": 28672,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0222000"
      },
      {
        "module": "pata_acpi",
        "size": 16384,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc021a000"
      },
      {
        "module": "falcon_lsm_serviceable",
        "size": 87169,
        "used": 1,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc056f000",
        "taint_state": [
          "P",
          "E"
        ],
        "taint_state_verbose": [
          "Proprietary or non-GPL-compatible module loaded",
          "Unsigned module loaded"
        ]
      },
      {
        "module": "nic_driver",
        "size": 16384,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc011a000",
        "taint_state": [
          "O"
        ],
        "taint_state_verbose": [
          "Out-of-tree (externally built) module loaded"
        ]
      }
    ]

    $ cat /proc/modules | jc --proc-modules -p -r
    [
      {
        "module": "i2c_piix4",
        "size": "28672",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0222000"
      },
      {
        "module": "pata_acpi",
        "size": "16384",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc021a000"
      },
      {
        "module": "falcon_lsm_serviceable",
        "size": "87169",
        "used": "1",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc056f000",
        "taint_state": "(PE)"
      },
      {
        "module": "nic_driver",
        "size": "16384",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc011a000",
        "taint_state": "(O)"
      }
    ]

<a id="jc.parsers.proc_modules.parse"></a>

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

Source: [`jc/parsers/proc_modules.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_modules.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
