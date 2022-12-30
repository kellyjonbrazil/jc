"""jc - JSON Convert `/proc/net/ipv6_route` file parser

Usage (cli):

    $ cat /proc/net/ipv6_route | jc --proc

or

    $ jc /proc/net/ipv6_route

or

    $ cat /proc/net/ipv6_route | jc --proc-net-ipv6-route

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_ipv6_route_file)

or

    import jc
    result = jc.parse('proc_net_ipv6_route', proc_net_ipv6_route_file)

Schema:

    [
      {
        "dest_net":                 string,
        "dest_prefix":              string,
        "source_net":               string,
        "source_prefix":            string,
        "next_hop":                 string,
        "metric":                   string,
        "ref_count":                string,
        "use_count":                string,
        "flags":                    string,
        "device":                   string
      }
    ]

Examples:

    $ cat /proc/net/ipv6_route | jc --proc -p
    [
      {
        "dest_net": "00000000000000000000000000000001",
        "dest_prefix": "80",
        "source_net": "00000000000000000000000000000000",
        "source_prefix": "00",
        "next_hop": "00000000000000000000000000000000",
        "metric": "00000100",
        "ref_count": "00000001",
        "use_count": "00000000",
        "flags": "00000001",
        "device": "lo"
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
    description = '`/proc/net/ipv6_route` file parser'
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

        header = 'dest_net dest_prefix source_net source_prefix next_hop metric ref_count use_count flags device\n'
        data = header + data
        raw_output = simple_table_parse(data.splitlines())

    return raw_output if raw else _process(raw_output)
