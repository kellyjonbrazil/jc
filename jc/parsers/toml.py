"""jc - JSON Convert TOML file parser

Usage (cli):

    $ cat file.toml | jc --toml

Usage (module):

    import jc
    result = jc.parse('toml', toml_file_output)

Schema:

TOML Document converted to a Dictionary.
See https://toml.io/en/ for details.

    {
      "key1":     string/int/float/boolean/null/array/object,
      "key2":     string/int/float/boolean/null/array/object
    }

Examples:

    $ cat file.toml
    title = "TOML Example"

    [owner]
    name = "Tom Preston-Werner"
    dob = 1979-05-27T07:32:00-08:00

    [database]
    enabled = true
    ports = [ 8000, 8001, 8002 ]

    $ cat file.toml | jc --toml -p
    {
      "title": "TOML Example",
      "owner": {
        "name": "Tom Preston-Werner",
        "dob": 296667120,
        "dob_iso": "1979-05-27T07:32:00-08:00"
      },
      "database": {
        "enabled": true,
        "ports": [
          8000,
          8001,
          8002
        ]
      }
    }
"""
from typing import Any
from jc.jc_types import JSONDictType
import jc.utils
from jc.parsers import tomli
from datetime import datetime


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'TOML file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the tomli library at https://github.com/hukkin/tomli.'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


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


def _fix_objects(obj: Any) -> JSONDictType:
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

            if isinstance(v, dict):
                obj.update({k: _fix_objects(v)})
                continue

            if isinstance(v, list):
                newlist = []
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

    raw_output: JSONDictType = {}

    if jc.utils.has_data(data):
        raw_output = _fix_objects(tomli.loads(data))

    return raw_output if raw else _process(raw_output)
