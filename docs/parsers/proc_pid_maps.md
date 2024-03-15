[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pid_maps"></a>

# jc.parsers.proc_pid_maps

jc - JSON Convert `/proc/<pid>/maps` file parser

Usage (cli):

    $ cat /proc/1/maps | jc --proc

or

    $ jc /proc/1/maps

or

    $ cat /proc/1/maps | jc --proc-pid-maps

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_maps_file)

or

    import jc
    result = jc.parse('proc_pid_maps', proc_pid_maps_file)

Schema:

    [
      {
        "start":                          string,
        "end":                            string,
        "perms": [
                                          string
        ],
        "offset":                         string,
        "inode":                          integer,
        "pathname":                       string,
        "maj":                            string,
        "min":                            string
      }
    ]

Examples:

    $ cat /proc/1/maps | jc --proc -p
    [
      {
        "perms": [
          "read",
          "private"
        ],
        "offset": "00000000",
        "inode": 798126,
        "pathname": "/usr/lib/systemd/systemd",
        "start": "55a9e753c000",
        "end": "55a9e7570000",
        "maj": "fd",
        "min": "00"
      },
      {
        "perms": [
          "read",
          "execute",
          "private"
        ],
        "offset": "00034000",
        "inode": 798126,
        "pathname": "/usr/lib/systemd/systemd",
        "start": "55a9e7570000",
        "end": "55a9e763a000",
        "maj": "fd",
        "min": "00"
      },
      ...
    ]

    $ cat /proc/1/maps | jc --proc-pid-maps -p -r
    [
      {
        "address": "55a9e753c000-55a9e7570000",
        "perms": "r--p",
        "offset": "00000000",
        "dev": "fd:00",
        "inode": "798126",
        "pathname": "/usr/lib/systemd/systemd"
      },
      {
        "address": "55a9e7570000-55a9e763a000",
        "perms": "r-xp",
        "offset": "00034000",
        "dev": "fd:00",
        "inode": "798126",
        "pathname": "/usr/lib/systemd/systemd"
      },
      ...
    ]

<a id="jc.parsers.proc_pid_maps.parse"></a>

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

Source: [`jc/parsers/proc_pid_maps.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pid_maps.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
