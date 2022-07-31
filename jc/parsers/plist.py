"""jc - JSON Convert PLIST file parser

Converts binary and XML PLIST files.

Usage (cli):

    $ cat file.plist | jc --plist

Usage (module):

    import jc
    result = jc.parse('plist', plist_command_output)

Schema:

    [
      {
        "plist":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ plist | jc --plist -p
    []

    $ plist | jc --plist -p -r
    []
"""
from typing import List, Dict, Union
import plistlib
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'PLIST file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


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
    data: Union[str, bytes],
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

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)

    if isinstance(data, str):
        data = bytes(data, 'utf-8')

    raw_output: Dict = {}

    if jc.utils.has_data(data):

        raw_output = plistlib.loads(data)

    return raw_output if raw else _process(raw_output)
