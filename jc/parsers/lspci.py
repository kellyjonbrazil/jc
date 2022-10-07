"""jc - JSON Convert `lspci -mmv` command output parser

This parser supports the following `lspci` options:
- `-mmv`
- `-nmmv`
- `-nnmmv`

Usage (cli):

    $ lspci -nnmmv | jc --lspci

or

    $ jc lspci -nnmmv

Usage (module):

    import jc
    result = jc.parse('lspci', lspci_command_output)

Schema:

    [
      {
        "lspci":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ lspci | jc --lspci -p
    []

    $ lspci | jc --lspci -p -r
    []
"""
import re
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`lspci -mmv` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['lspci']


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
    device_output: Dict = {}

    if jc.utils.has_data(data):
        item_id_p = re.compile(r'(?P<id>^[0-9a-f]{4}$)')
        item_id_bracket_p = re.compile(r' \[(?P<id>[0-9a-f]{4})\]$')

        for line in filter(None, data.splitlines()):
            if line.startswith('Slot:'):
                if device_output:
                    raw_output.append(device_output)
                    device_output = {}

                device_output['Slot'] = line.split()[1]
                continue

            key, val = line.split(maxsplit=1)
            key = key[:-1]

            # numeric only (-nmmv)
            if item_id_p.match(val):
                device_output[key + '_id'] = val
                continue

            # string and numeric (-nnmmv)
            if item_id_bracket_p.search(val):
                string, idnum = val.rsplit(maxsplit=1)
                device_output[key] = string
                device_output[key + '_id'] = idnum[1:-1]
                continue

            # string only (-mmv)
            device_output[key] = val
            continue


        if device_output:
            raw_output.append(device_output)

    return raw_output if raw else _process(raw_output)
