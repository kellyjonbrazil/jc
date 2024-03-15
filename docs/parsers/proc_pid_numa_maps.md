[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pid_numa_maps"></a>

# jc.parsers.proc_pid_numa_maps

jc - JSON Convert `/proc/<pid>/numa_maps` file parser

This parser will attempt to convert number values to integers. If that is
not desired, please use the `--raw` option (cli) or `raw=True` argument
(module).

Usage (cli):

    $ cat /proc/1/numa_maps | jc --proc

or

    $ jc /proc/1/numa_maps

or

    $ cat /proc/1/numa_maps | jc --proc-pid-numa-maps

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_numa_maps_file)

or

    import jc
    result = jc.parse('proc_pid_numa_maps', proc_pid_numa_maps_file)

Schema:

Integer conversion for Key/value pairs will be attempted.

    [
      {
        "address":                    string,
        "policy":                     string,
        "<key>":                      string/integer,
        "options": [
                                      string  # [0]
        ]
      }
    ]

    [0] remaining individual words that are not part of a key/value pair

Examples:

    $ cat /proc/1/numa_maps | jc --proc -p
    [
      {
        "address": "7f53b5083000",
        "policy": "default",
        "file": "/usr/lib/x86_64-linux-gnu/ld-2.32.so",
        "anon": 2,
        "dirty": 2,
        "N0": 2,
        "kernelpagesize_kB": 4
      },
      {
        "address": "7ffd1b23e000",
        "policy": "default",
        "anon": 258,
        "dirty": 258,
        "N0": 258,
        "kernelpagesize_kB": 4,
        "options": [
          "stack"
        ]
      },
      ...
    ]

    $ cat /proc/1/numa_maps | jc --proc-pid-numa-maps -p -r
    [
      {
        "address": "7f53b5083000",
        "policy": "default",
        "file": "/usr/lib/x86_64-linux-gnu/ld-2.32.so",
        "anon": "2",
        "dirty": "2",
        "N0": "2",
        "kernelpagesize_kB": "4"
      },
      {
        "address": "7ffd1b23e000",
        "policy": "default",
        "anon": "258",
        "dirty": "258",
        "N0": "258",
        "kernelpagesize_kB": "4",
        "options": [
          "stack"
        ]
      },
      ...
    ]

<a id="jc.parsers.proc_pid_numa_maps.parse"></a>

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

Source: [`jc/parsers/proc_pid_numa_maps.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pid_numa_maps.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
