"""jc - JSON Convert `/proc/net/route` file parser

Usage (cli):

    $ cat /proc/net/route | jc --proc

or

    $ jc /proc/net/route

or

    $ cat /proc/net/route | jc --proc-net-route

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_route_file)

or

    import jc
    result = jc.parse('proc_net_route', proc_net_route_file)

Schema:

    [
      {
        "Iface":                  string,
        "Destination":            string,
        "Gateway":                string,
        "Flags":                  string,
        "RefCnt":                 integer,
        "Use":                    integer,
        "Metric":                 integer,
        "Mask":                   string,
        "MTU":                    integer,
        "Window":                 integer,
        "IRTT":                   integer
      }
  ]

Examples:

    $ cat /proc/net/route | jc --proc -p
    [
      {
        "Iface": "ens33",
        "Destination": "00000000",
        "Gateway": "0247A8C0",
        "Flags": "0003",
        "RefCnt": 0,
        "Use": 0,
        "Metric": 100,
        "Mask": "00000000",
        "MTU": 0,
        "Window": 0,
        "IRTT": 0
      },
      ...
    ]

    $ cat /proc/net/route | jc --proc-net-route -p -r
    [
      {
        "Iface": "ens33",
        "Destination": "00000000",
        "Gateway": "0247A8C0",
        "Flags": "0003",
        "RefCnt": "0",
        "Use": "0",
        "Metric": "100",
        "Mask": "00000000",
        "MTU": "0",
        "Window": "0",
        "IRTT": "0"
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
    description = '`/proc/net/route` file parser'
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
    # field types documented here: https://github.com/torvalds/linux/blob/v4.19/include/uapi/linux/route.h
    int_list = {'RefCnt', 'Use', 'Metric', 'MTU', 'Window', 'IRTT'}

    for entry in proc_data:
        for key, val in entry.items():
            if key in int_list:
                entry[key] = int(val)

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

        raw_output = simple_table_parse(data.splitlines())

    return raw_output if raw else _process(raw_output)
