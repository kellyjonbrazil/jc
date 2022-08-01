"""jc - JSON Convert PLIST file parser

Converts binary and XML PLIST files.

Binary values are converted into an ASCII hex representation.

Datetime objects are converted into Unix epoch timestamps and ISO strings.

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
import binascii
from datetime import datetime
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


def _b2a(byte_string: bytes) -> str:
    """Convert a byte string to a colon-delimited hex ascii string"""
    # need try/except since seperator was only introduced in python 3.8.
    # provides compatibility for python 3.6 and 3.7.
    try:
      return binascii.hexlify(byte_string, ':').decode('utf-8')
    except TypeError:
      hex_string = binascii.hexlify(byte_string).decode('utf-8')
      colon_seperated = ':'.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
      return colon_seperated


def _fix_objects(obj):
    """
    Recursively traverse the nested dictionary or list and convert objects
    into JSON serializable types.
    """
    if isinstance(obj, dict):
        for k, v in obj.copy().items():

            if isinstance(v, datetime):
                iso = v.isoformat()
                v = int(round(v.timestamp()))
                obj.update({k: v, f'{k}_iso': iso})
                continue

            if isinstance(v, bytes):
                v = _b2a(v)
                obj.update({k: v})
                continue

            if isinstance(v, dict):
                obj.update({k: _fix_objects(v)})
                continue

            if isinstance(v, list):
                newlist =[]
                for i in v:
                    newlist.append(_fix_objects(i))
                obj.update({k: newlist})
                continue

    if isinstance(obj, list):
        new_list = []
        for i in obj:
            new_list.append(_fix_objects(i))
        obj = new_list

    return obj


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

        try:
            raw_output = plistlib.loads(data)
        except plistlib.InvalidFileException:
            pass

        raw_output = _fix_objects(raw_output)

    return raw_output if raw else _process(raw_output)
