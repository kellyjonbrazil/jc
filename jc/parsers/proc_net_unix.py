"""jc - JSON Convert `/proc/net/unix` file parser

Usage (cli):

    $ cat /proc/net/unix | jc --proc

or

    $ jc /proc/net/unix

or

    $ cat /proc/net/unix | jc --proc-net-unix

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_unix_file)

or

    import jc
    result = jc.parse('proc_net_unix', proc_net_unix_file)

Schema:

    [
      {
        "Num":                    string,
        "RefCount":               string,
        "Protocol":               string,
        "Flags":                  string,
        "Type":                   string,
        "St":                     string,
        "Inode":                  integer,
        "Path":                   string
      }
  ]

Examples:

    $ cat /proc/net/unix | jc --proc -p
    [
      {
        "Num": "ffff9b61ac49c400:",
        "RefCount": "00000002",
        "Protocol": "00000000",
        "Flags": "00010000",
        "Type": "0001",
        "St": "01",
        "Inode": 42776,
        "Path": "/var/snap/lxd/common/lxd/unix.socket"
      },
      ...
    ]

    $ cat /proc/net/unix | jc --proc-net-unix -p -r
    [
      {
        "Num": "ffff9b61ac49c400:",
        "RefCount": "00000002",
        "Protocol": "00000000",
        "Flags": "00010000",
        "Type": "0001",
        "St": "01",
        "Inode": "42776",
        "Path": "/var/snap/lxd/common/lxd/unix.socket"
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
    description = '`/proc/net/unix` file parser'
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
    int_list = {'Inode'}

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
