r"""jc - JSON Convert `/proc/net/igmp6` file parser

Usage (cli):

    $ cat /proc/net/igmp6 | jc --proc

or

    $ jc /proc/net/igmp6

or

    $ cat /proc/net/igmp6 | jc --proc-net-igmp6

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_igmp6_file)

or

    import jc
    result = jc.parse('proc_net_igmp6', proc_net_igmp6_file)

Schema:

    [
      {
        "index":                    integer,
        "name":                     string,
        "address":                  string,
        "users":                    integer,
        "group":                    string,
        "reporters":                integer
      }
    ]

Examples:

    $ cat /proc/net/igmp6 | jc --proc -p
    [
      {
        "index": 1,
        "name": "lo",
        "address": "ff020000000000000000000000000001",
        "users": 1,
        "group": "0000000C",
        "reporters": 0
      },
      {
        "index": 1,
        "name": "lo",
        "address": "ff010000000000000000000000000001",
        "users": 1,
        "group": "00000008",
        "reporters": 0
      },
      {
        "index": 2,
        "name": "ens33",
        "address": "ff0200000000000000000001ffa4e315",
        "users": 1,
        "group": "00000004",
        "reporters": 0
      },
      ...
    ]

    $ cat /proc/net/igmp6 | jc --proc-net-igmp6 -p -r
    [
      {
        "index": "1",
        "name": "lo",
        "address": "ff020000000000000000000000000001",
        "users": "1",
        "group": "0000000C",
        "reporters": "0"
      },
      {
        "index": "1",
        "name": "lo",
        "address": "ff010000000000000000000000000001",
        "users": "1",
        "group": "00000008",
        "reporters": "0"
      },
      {
        "index": "2",
        "name": "ens33",
        "address": "ff0200000000000000000001ffa4e315",
        "users": "1",
        "group": "00000004",
        "reporters": "0"
      }
    ]
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/igmp6` file parser'
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
    int_list = {'index', 'users', 'reporters'}

    for item in proc_data:
        for key, val in item.items():
            if key in int_list:
                item[key] = int(val)

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

        header = 'index name address users group reporters\n'
        data = header + data
        raw_output = simple_table_parse(data.splitlines())

    return raw_output if raw else _process(raw_output)
