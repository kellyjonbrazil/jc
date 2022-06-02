"""jc - JSON Convert `postconf -M` command output parser

Usage (cli):

    $ postconf -M | jc --postconf

    or

    $ jc postconf -M

Usage (module):

    import jc
    result = jc.parse('postconf', postconf_command_output)

Schema:

    [
      {
        "postconf":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ postconf | jc --postconf -p
    []

    $ postconf | jc --postconf -p -r
    []
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`postconf -M` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['postconf -M']


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
        table = ['service_name service_type private unprivileged chroot wake_up_time process_limit command']
        data_list = list(filter(None, data.splitlines()))
        table.extend(data_list)
        raw_output = simple_table_parse(table)

    return raw_output if raw else _process(raw_output)
