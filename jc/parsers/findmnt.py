"""jc - JSON Convert `findmnt` command output parser

<<Short findmnt description and caveats>>

Usage (cli):

    $ findmnt | jc --findmnt

or

    $ jc findmnt

Usage (module):

    import jc
    result = jc.parse('findmnt', findmnt_command_output)

Schema:

    [
      {
        "findmnt":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ findmnt | jc --findmnt -p
    []

    $ findmnt | jc --findmnt -p -r
    []
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
from jc.parsers.universal import simple_table_parse
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`findmnt` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['findmnt']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    # split normal options and k/v options
    for item in proc_data:
        reg_options = []
        kv_options = {}

        if 'options' in item:
            opt_list = item['options'].split(',')  # type: ignore

            for option in opt_list:
                if '=' in option:
                    k, v = option.split('=', maxsplit=1)
                    kv_options[k] = v

                else:
                    reg_options.append(option)

            if reg_options:
                item['options'] = reg_options
            if kv_options:
                item['kv_options'] = kv_options

    return proc_data


def _replace(matchobj):
    if matchobj:
        matchlen = len(matchobj.group(1))
        return ' ' * matchlen + '/'


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

    raw_output: List[Dict] = []
    table: List[str] = []

    if jc.utils.has_data(data):



        for line in filter(None, data.splitlines()):

            # remove initial drawing characters
            line = re.sub(r'^([│ ├─└─|`-]+)/', _replace, line, count=1)
            table.append(line)

        table[0] = table[0].lower()
        raw_output = simple_table_parse(table)

    return raw_output if raw else _process(raw_output)
