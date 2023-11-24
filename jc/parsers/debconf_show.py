"""jc - JSON Convert `debconf-show` command output parser

Usage (cli):

    $ debconf-show | jc --debconf-show

or

    $ jc debconf-show

Usage (module):

    import jc
    result = jc.parse('debconf_show', debconf_show_command_output)

Schema:

    [
      {
        "debconf-show":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ debconf-show | jc --debconf-show -p
    []

    $ debconf-show | jc --debconf-show -p -r
    []
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`debconf-show` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['debconf-show']


__version__ = info.version


def _process(proc_data: JSONDictType) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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

        for line in filter(None, data.splitlines()):
            output_line: Dict = {}
            splitline = line.split(':', maxsplit=1)

            output_line['asked'] = splitline[0].startswith('*')
            packagename, key = splitline[0].split('/', maxsplit=1)
            packagename = packagename[2:]
            key = key.replace('-', '_')
            val = splitline[1].strip()
            output_line['packagename'] = packagename
            output_line['name'] = key
            output_line['value'] = val

            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
