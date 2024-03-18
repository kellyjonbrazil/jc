r"""jc - JSON Convert `/proc/buddyinfo` file parser

Usage (cli):

    $ cat /proc/buddyinfo | jc --proc

or

    $ jc /proc/buddyinfo

or

    $ cat /proc/buddyinfo | jc --proc-buddyinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_buddyinfo_file)

or

    import jc
    result = jc.parse('proc_buddyinfo', proc_buddyinfo_file)

Schema:

All values are integers.

    [
      {
        "node":               integer,
        "zone":               string,
        "free_chunks": [
                              integer  # [0]
        ]
      }
    ]

    [0] array index correlates to the Order number.
        E.g. free_chunks[0] is the value for Order 0


Examples:

    $ cat /proc/buddyinfo | jc --proc -p
    [
      {
        "node": 0,
        "zone": "DMA",
        "free_chunks": [
          0,
          0,
          0,
          1,
          1,
          1,
          1,
          1,
          0,
          1,
          3
        ]
      },
      {
        "node": 0,
        "zone": "DMA32",
        "free_chunks": [
          78,
          114,
          82,
          52,
          38,
          25,
          13,
          9,
          3,
          4,
          629
        ]
      },
      {
        "node": 0,
        "zone": "Normal",
        "free_chunks": [
          0,
          22,
          8,
          10,
          1,
          1,
          2,
          11,
          13,
          0,
          0
        ]
      }
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/buddyinfo` file parser'
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
    int_list = {'node'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        if 'free_chunks' in entry:
            entry['free_chunks'] = [int(x) for x in entry['free_chunks']]

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

        for line in filter(None, data.splitlines()):

            buddy_list = line.split()

            raw_output.append(
                {
                    'node': buddy_list[1][:-1],
                    'zone': buddy_list[3],
                    'free_chunks': buddy_list[4:]
                }
            )

    return raw_output if raw else _process(raw_output)
