"""jc - JSON Convert `/proc/meminfo` file parser

Usage (cli):

    $ cat /proc/meminfo | jc --proc

Usage (module):

    import jc
    result = jc.parse('proc_meminfo', proc_meminfo_file)

Schema:

    [
      {
        "foo":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ foo | jc --foo -p
    []

    $ foo | jc --foo -p -r
    []
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/meminfo` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
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

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            split_line = line.split(':', maxsplit=1)
            key = split_line[0]
            val = int(split_line[1].rsplit(maxsplit=1)[0])
            raw_output[key] = val

    return raw_output if raw else _process(raw_output)
