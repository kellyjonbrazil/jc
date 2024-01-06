"""jc - JSON Convert POSIX path list string parser

Parse a colon-separated POSIX path list, commonly found in environment variables.

Usage (cli):

    $ echo "/Users/admin/.docker/bin:/Users/admin/.asdf/shims" | jc --path-list

Usage (module):

    import jc
    result = jc.parse('path-list', path_string)

Schema:

    [
      {
        "path":                      string or null,
        "parent":                    string or null,
        "filename":                  string or null,
        "stem":                      string or null,
        "extension":                 string or null,
        "path_list": [               array or null
                                     string
        ],
      }
    ]

Examples:

    $ echo "/abc/def/gh.txt:/xyz/uvw/ab.app" | jc --path-list -p

    [
      {
        "path": "/abc/def/gh.txt",
        "parent": "/abc/def",
        "filename": "gh.txt",
        "stem": "gh",
        "extension": "txt",
        "path_list": [
          "/",
          "abc",
          "def",
          "gh.txt"
        ]
      },
      {
        "path": "/xyz/uvw/ab.app",
        "parent": "/xyz/uvw",
        "filename": "ab.app",
        "stem": "ab",
        "extension": "app",
        "path_list": [
          "/",
          "xyz",
          "uvw",
          "ab.app"
        ]
      }
    ]

"""

import jc.parsers.path as path
from typing import Dict, List
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'path list string parser'
    author = 'Michael Nietzold'
    author_email = 'https://github.com/muescha'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'string', 'slurpable']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # no changes
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries representing a Key/Value pair document.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    # This parser is an alias of path.py
    path.info = info  # type: ignore

    delimiter = ":" if "\\" not in data else ";"

    raw_output = [
        path.parse(line, raw=raw, quiet=quiet)
        for line in data.split(delimiter)
        if jc.utils.has_data(data)
    ]

    return raw_output if raw else _process(raw_output)
