r"""jc - JSON Convert POSIX path list string parser

Parse a colon-separated POSIX path list, commonly found in environment
variables.

> Note: An empty entry (for example `/usr/bin::/bin`) means the current
> directory and is reported as `.`. An entry that only contains spaces
> is kept as a path.

Usage (cli):

    $ echo "/Users/admin/.docker/bin:/Users/admin/.asdf/shims" | jc --path-list

Usage (module):

    import jc
    result = jc.parse('path-list', path_string)

Schema:

    [
      {
        "path":                      string,
        "parent":                    string,
        "filename":                  string,
        "stem":                      string,
        "extension":                 string,
        "path_list": [
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
    version = '1.1'
    description = 'POSIX path list string parser'
    author = 'Michael Nietzold'
    author_email = 'https://github.com/muescha'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'string', 'slurpable']


__version__ = info.version


def _is_windows(data: str) -> bool:
    """
    A path list is a Windows path list if an entry separated by ';' starts
    with a drive letter or a UNC prefix, or if it contains backslashes and
    no forward slash or colon. Everything else is a POSIX path list.
    """
    for entry in data.split(';'):
        if path._WINDOWS_START.match(entry.strip()):
            return True

    return '\\' in data and '/' not in data and ':' not in data


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

    # This parser uses path.py

    raw_output = []

    # check the whole input once instead of for every entry
    if jc.utils.has_data(data):
        windows = _is_windows(data)
        delimiter = ";" if windows else ":"

        for line in data.rstrip('\r\n').split(delimiter):
            line = line.rstrip('\n')

            # an empty entry means the current directory. A whitespace-only
            # entry is a valid directory name and is kept as is.
            if line == '':
                line = '.'

            raw_output.append(path._parse_path(line, windows, raw))

    return raw_output
