r"""jc - JSON Convert `/proc/partitions` file parser

Usage (cli):

    $ cat /proc/partitions | jc --proc

or

    $ jc /proc/partitions

or

    $ cat /proc/partitions | jc --proc-partitions

Usage (module):

    import jc
    result = jc.parse('proc', proc_partitions_file)

or

    import jc
    result = jc.parse('proc_partitions', proc_partitions_file)

Schema:

    [
      {
        "major":                  integer,
        "minor":                  integer,
        "num_blocks":             integer,
        "name":                   string
      }
    ]

Examples:

    $ cat /proc/partitions | jc --proc -p
    [
      {
        "major": 7,
        "minor": 0,
        "num_blocks": 56896,
        "name": "loop0"
      },
      {
        "major": 7,
        "minor": 1,
        "num_blocks": 56868,
        "name": "loop1"
      },
      ...
    ]

    $ cat /proc/partitions | jc --proc-partitions -p -r
    [
      {
        "major": "7",
        "minor": "0",
        "num_blocks": "56896",
        "name": "loop0"
      },
      {
        "major": "7",
        "minor": "1",
        "num_blocks": "56868",
        "name": "loop1"
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
    description = '`/proc/partitions` file parser'
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
        for key in entry:
            try:
                entry[key] = int(entry[key])
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

        cleandata = list(filter(None, data.splitlines()))
        cleandata[0] = cleandata[0].replace('#', 'num_')
        raw_output = simple_table_parse(cleandata)

    return raw_output if raw else _process(raw_output)
