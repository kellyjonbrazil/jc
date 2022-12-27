"""jc - JSON Convert `/proc/swaps` file parser

Usage (cli):

    $ cat /proc/swaps | jc --proc

or

    $ jc /proc/swaps

or

    $ cat /proc/swaps | jc --proc-swaps

Usage (module):

    import jc
    result = jc.parse('proc', proc_swaps_file)

or

    import jc
    result = jc.parse('proc_swaps', proc_swaps_file)

Schema:

    [
      {
        "filename":                 string,
        "type":                     string,
        "size":                     integer,
        "used":                     integer,
        "priority":                 integer
      }
    ]

Examples:

    $ cat /proc/swaps | jc --proc -p
    [
      {
        "filename": "/swap.img",
        "type": "file",
        "size": 3996668,
        "used": 0,
        "priority": -2
      },
      ...
    ]

    $ cat /proc/swaps | jc --proc-swaps -p -r
    [
      {
        "filename": "/swap.img",
        "type": "file",
        "size": "3996668",
        "used": "0",
        "priority": "-2"
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
    description = '`/proc/swaps` file parser'
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
    int_list = {'size', 'used', 'priority'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

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
        cleandata[0] = cleandata[0].lower()
        raw_output = simple_table_parse(cleandata)

    return raw_output if raw else _process(raw_output)
