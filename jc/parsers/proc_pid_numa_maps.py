r"""jc - JSON Convert `/proc/<pid>/numa_maps` file parser

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
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/<pid>/numa_maps` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for entry in proc_data:
        for key, val in entry.items():
            try:
                entry[key] = int(val)
            except Exception:
                pass

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List = []

    if jc.utils.has_data(data):

        header = 'address policy details\n'
        data = header + data

        raw_output = simple_table_parse(data.splitlines())

        for row in raw_output:
            if 'details' in row:
                detail_split = row['details'].split()

                options = []
                for item in detail_split:
                    if '=' in item:
                        key, val = item.split('=')
                        row.update({key: val})
                    else:
                        options.append(item)

                if options:
                    row['options'] = options

                del row['details']

    return raw_output if raw else _process(raw_output)
