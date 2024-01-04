"""jc - JSON Convert path string parser

Parse a path.

Usage (cli):

    $ echo "/Users/admin/.docker/bin" | jc --path

Usage (module):

    import jc
    result = jc.parse('path', path_string)

Schema:

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

Examples:

    $ echo "/abc/def/gh.txt" | jc --path -p

    {
      "path": "/abc/def/gh.txt",
      "parent": "/abc/def",
      "filename": "gh.txt",
      "stem": "gh",
      "extension": "txt",
      "path_list": [
        "abc",
        "def",
        "gh.txt"
      ]
    }

"""

from typing import Dict

import jc.parsers.url as url
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'path string parser'
    author = 'Michael Nietzold'
    author_email = 'https://github.com/muescha'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'string', 'slurpable']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    hold_list = [
        'path',
        'parent',
        'filename',
        'stem',
        'extension',
        'path_list'
    ]

    return {key: proc_data.get(key) for key in hold_list}


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary representing a Key/Value pair document.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    # This parser is an alias of url.py
    url.info = info  # type: ignore

    raw_output = url.parse(data, raw=raw, quiet=quiet) if jc.utils.has_data(data) else {}

    return raw_output if raw else _process(raw_output)
