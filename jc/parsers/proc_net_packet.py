"""jc - JSON Convert `/proc/net/packet` file parser

Usage (cli):

    $ cat /proc/net/packet | jc --proc

or

    $ jc /proc/net/packet

or

    $ cat /proc/net/packet | jc --proc-net-packet

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_packet_file)

or

    import jc
    result = jc.parse('proc_net_packet', proc_net_packet_file)

Schema:

    {
      "sk":                     string,
      "RefCnt":                 integer,
      "Type":                   integer,
      "Proto":                  string,
      "Iface":                  integer,
      "R":                      integer,
      "Rmem":                   integer,
      "User":                   integer,
      "Inode":                  integer
    }

Examples:

    $ cat /proc/net/packet | jc --proc -p
    {
      "sk": "ffff9b61b56c1800",
      "RefCnt": 3,
      "Type": 3,
      "Proto": "88cc",
      "Iface": 2,
      "R": 1,
      "Rmem": 0,
      "User": 101,
      "Inode": 34754
    }

    $ cat /proc/net/packet | jc --proc-net-packet -p -r
    {
      "sk": "ffff9b61b56c1800",
      "RefCnt": "3",
      "Type": "3",
      "Proto": "88cc",
      "Iface": "2",
      "R": "1",
      "Rmem": "0",
      "User": "101",
      "Inode": "34754"
    }
"""
from typing import Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/packet` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list = {'RefCnt', 'Type', 'Iface', 'R', 'Rmem', 'User', 'Inode'}

    for key, val in proc_data.items():
        if key in int_list:
            proc_data[key] = int(val)

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}

    if jc.utils.has_data(data):

        raw_output_list = simple_table_parse(data.splitlines())
        raw_output = raw_output_list[0]

    return raw_output if raw else _process(raw_output)
