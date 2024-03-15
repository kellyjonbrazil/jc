r"""jc - JSON Convert POSIX path string parser

Parse a POSIX path.

Usage (cli):

    $ echo "/Users/admin/.docker/bin" | jc --path

Usage (module):

    import jc
    result = jc.parse('path', path_string)

Schema:

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

Examples:

    $ echo "/abc/def/gh.txt" | jc --path -p
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
    }
"""
from pathlib import PurePosixPath, PureWindowsPath
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'POSIX path string parser'
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

        Dictionary representing a Key/Value pair document.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    if not jc.utils.has_data(data):
        return {}

    data = data.rstrip("\n")

    if "\\" in data:
        path = PureWindowsPath(data)
    else:
        path = PurePosixPath(data)

    raw_output = {
        'path': str(path),
        'parent': str(path.parent),
        'filename': path.name,
        'stem': path.stem,
        'extension': path.suffix[1:],
        'path_list': list(path.parts)
    }

    return raw_output if raw else _process(raw_output)
