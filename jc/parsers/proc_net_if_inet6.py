"""jc - JSON Convert `/proc/net/if_inet6` file parser

Usage (cli):

    $ cat /proc/net/if_inet6 | jc --proc

or

    $ jc /proc/net/if_inet6

or

    $ cat /proc/net/if_inet6 | jc --proc-net-if-inet6

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_if_inet6_file)

or

    import jc
    result = jc.parse('proc_net_if_inet6', proc_net_if_inet6_file)

Schema:

    [
      {
        "address":              string,
        "index":                string,
        "prefix":               string,
        "scope":                string,
        "flags":                string,
        "name":                 string
      }
    ]

Examples:

    $ cat /proc/net/if_inet6 | jc --proc -p
    [
      {
        "address": "fe80000000000000020c29fffea4e315",
        "index": "02",
        "prefix": "40",
        "scope": "20",
        "flags": "80",
        "name": "ens33"
      },
      {
        "address": "00000000000000000000000000000001",
        "index": "01",
        "prefix": "80",
        "scope": "10",
        "flags": "80",
        "name": "lo"
      }
    ]
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/if_inet6` file parser'
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

        header = 'address index prefix scope flags name\n'
        data = header + data
        raw_output = simple_table_parse(data.splitlines())

    return raw_output if raw else _process(raw_output)
