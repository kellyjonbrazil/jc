"""jc - JSON CLI output utility `nmcli` command output parser

<<Short nmcli description and caveats>>

Usage (cli):

    $ nmcli | jc --nmcli

    or

    $ jc nmcli

Usage (module):

    import jc
    result = jc.parse('nmcli', nmcli_command_output)

    or

    import jc.parsers.nmcli
    result = jc.parsers.nmcli.parse(nmcli_command_output)

Schema:

    [
      {
        "nmcli":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ nmcli | jc --nmcli -p
    []

    $ nmcli | jc --nmcli -p -r
    []
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`nmcli` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['nmcli']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

    return proc_data

def _normalize_key(keyname: str) -> str:
    return keyname.replace(' ', '_')\
                  .replace('.', '_')\
                  .replace('[', '_')\
                  .replace(']', '')\
                  .replace('-', '_')\
                  .replace('GENERAL_', '')\
                  .lower()


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
    item: Dict = {}
    current_item = ''

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            key, value = line.split(':', maxsplit=1)
            key = _normalize_key(key)
            value = value.strip()

            if item and 'device' in key and value != current_item:
                raw_output.append(item)
                item = {}
                current_item = value

            item.update({key: value})

    if item:
        raw_output.append(item)

    return raw_output if raw else _process(raw_output)
