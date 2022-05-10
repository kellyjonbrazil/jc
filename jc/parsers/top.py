"""jc - JSON Convert `top -b` command output parser

<<Short top description and caveats>>

Usage (cli):

    $ top -b -n 3 | jc --top

    or

    $ jc top -b -n 3

Usage (module):

    import jc
    result = jc.parse('top', top_command_output)

Schema:

    [
      {
        "top":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ top | jc --top -p
    []

    $ top | jc --top -p -r
    []
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`top -b` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['top -b']


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

        for line in filter(None, data.splitlines()):

            # parse the content here
            # check out helper functions in jc.utils
            # and jc.parsers.universal

            pass

    return raw_output if raw else _process(raw_output)
