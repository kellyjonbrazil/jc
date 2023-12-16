"""jc - JSON Convert `/proc/cmdline` file parser

Usage (cli):

    $ cat /proc/cmdline | jc --proc

or

    $ jc /proc/cmdline

or

    $ cat /proc/cmdline | jc --proc-cmdline

Usage (module):

    import jc
    result = jc.parse('proc_cmdline', proc_cmdline_file)

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
import shlex
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/cmdline` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
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
    options: List = []

    if jc.utils.has_data(data):

        split_line = shlex.split(data)

        for item in split_line:
            if '=' in item:
                key, val = item.split('=', maxsplit=1)
                raw_output[key] = val

            else:
                options.append(item)

    if options:
        raw_output['_options'] = options

    return raw_output if raw else _process(raw_output)
