"""jc - JSON Convert `udevadm info` command output parser

Usage (cli):

    $ udevadm info --query=all /dev/sda | jc --udevadm

or

    $ jc udevadm info --query=all /dev/sda

Usage (module):

    import jc
    result = jc.parse('udevadm', udevadm_command_output)

Schema:

    [
      {
        "udevadm":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ udevadm info --query=all /dev/sda | jc --udevadm -p
    []

    $ udevadm info --query=all /dev/sda | jc --udevadm -p -r
    []
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`udevadm info` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['udevadm info']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
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
    s_list: List = []
    e_list: List = []

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            prefix, value = line.split(maxsplit=1)

            if prefix == 'P:':
                raw_output['P'] = value
                continue

            if prefix == 'S:':
                s_list.append(value)
                continue

            if prefix == 'E:':
                e_list.append(value)
                continue

            raw_output[prefix[:-1]] = value

    if s_list:
        raw_output['S'] = s_list

    if e_list:
        raw_output['E'] = {}
        for item in e_list:
            k, v = item.split('=')
            raw_output['E'][k] = v

    return raw_output if raw else _process(raw_output)
