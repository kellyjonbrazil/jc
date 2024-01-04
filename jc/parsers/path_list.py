"""jc - JSON Convert URL string parser

Normalized, Encoded, and Decoded versions of the original URL and URL parts
are included in the output. Encoding and Decoding is best effort.

> Note: Do not use the Encoded fields for a URL that has already been
> Encoded. Similarly, do not use the Decoded fields for a URL that has
> already been Decoded.

Usage (cli):

    $ echo "/Users/admin/.docker/bin:/Users/admin/.asdf/shims" | jc --path-list

Usage (module):

    import jc
    result = jc.parse('path-list', path_string)

Schema:

    [
      {
        "url":                       string,
        "scheme":                    string or null,
        "netloc":                    string or null,
        "path":                      string or null,
        "parent":                    string or null,
        "filename":                  string or null,
        "stem":                      string or null,
        "extension":                 string or null,
        "path_list": [               array or null
                                     string
        ],
        "query":                     string or null,
        "query_obj": {               object or null
          <query-key>: [             array or null
            <query-value>            string            # [0]
          ]
        },
        "fragment":                  string or null,
        "username":                  string or null,
        "password":                  string or null,
        "hostname":                  string or null,
        "port":                      integer or null,  # [1]
        "encoded": {
          "url":                     string,
          "scheme":                  string or null,
          "netloc":                  string or null,
          "path":                    string or null,
          "parent":                  string or null,
          "filename":                string or null,
          "stem":                    string or null,
          "extension":               string or null,
          "path_list": [             array or null
                                     string
          ],
          "query":                   string or null,
          "fragment":                string or null,
          "username":                string or null,
          "password":                string or null,
          "hostname":                string or null,
          "port":                    integer or null,  # [1]
        },
        "decoded": {
          "url":                     string,
          "scheme":                  string or null,
          "netloc":                  string or null,
          "path":                    string or null,
          "parent":                  string or null,
          "filename":                string or null,
          "stem":                    string or null,
          "extension":               string or null,
          "path_list": [             array or null
                                     string
          ],
          "query":                   string or null,
          "fragment":                string or null,
          "username":                string or null,
          "password":                string or null,
          "hostname":                string or null,
          "port":                    integer or null,  # [1]
        }
      }
    ]

    [0] Duplicate query-keys will have their values consolidated into the
        array of query-values

    [1] Invalid port values will be converted to null/None and a warning
        message will be printed to `STDERR` if quiet=False

Examples:

    $ echo "/abc/def/gh.txt:/xyz/uvw/ab.app" | jc --path-list -p

    [
      {
        "url": "/abc/def/gh.txt",
        "scheme": null,
        "netloc": null,
        "path": "/abc/def/gh.txt",
        "parent": "/abc/def",
        "filename": "gh.txt",
        "stem": "gh",
        "extension": "txt",
        "path_list": [
          "abc",
          "def",
          "gh.txt"
        ],
        "query": null,
        "query_obj": null,
        "fragment": null,
        "username": null,
        "password": null,
        "hostname": null,
        "port": null,
        "encoded": {
          "url": "/abc/def/gh.txt",
          "scheme": null,
          "netloc": null,
          "path": "/abc/def/gh.txt",
          "parent": "/abc/def",
          "filename": "gh.txt",
          "stem": "gh",
          "extension": "txt",
          "path_list": [
            "abc",
            "def",
            "gh.txt"
          ],
          "query": null,
          "fragment": null,
          "username": null,
          "password": null,
          "hostname": null,
          "port": null
        },
        "decoded": {
          "url": "/abc/def/gh.txt",
          "scheme": null,
          "netloc": null,
          "path": "/abc/def/gh.txt",
          "parent": "/abc/def",
          "filename": "gh.txt",
          "stem": "gh",
          "extension": "txt",
          "path_list": [
            "abc",
            "def",
            "gh.txt"
          ],
          "query": null,
          "fragment": null,
          "username": null,
          "password": null,
          "hostname": null,
          "port": null
        }
      },
      {
        "url": "/xyz/uvw/ab.app",
        "scheme": null,
        "netloc": null,
        "path": "/xyz/uvw/ab.app",
        "parent": "/xyz/uvw",
        "filename": "ab.app",
        "stem": "ab",
        "extension": "app",
        "path_list": [
          "xyz",
          "uvw",
          "ab.app"
        ],
        "query": null,
        "query_obj": null,
        "fragment": null,
        "username": null,
        "password": null,
        "hostname": null,
        "port": null,
        "encoded": {
          "url": "/xyz/uvw/ab.app",
          "scheme": null,
          "netloc": null,
          "path": "/xyz/uvw/ab.app",
          "parent": "/xyz/uvw",
          "filename": "ab.app",
          "stem": "ab",
          "extension": "app",
          "path_list": [
            "xyz",
            "uvw",
            "ab.app"
          ],
          "query": null,
          "fragment": null,
          "username": null,
          "password": null,
          "hostname": null,
          "port": null
        },
        "decoded": {
          "url": "/xyz/uvw/ab.app",
          "scheme": null,
          "netloc": null,
          "path": "/xyz/uvw/ab.app",
          "parent": "/xyz/uvw",
          "filename": "ab.app",
          "stem": "ab",
          "extension": "app",
          "path_list": [
            "xyz",
            "uvw",
            "ab.app"
          ],
          "query": null,
          "fragment": null,
          "username": null,
          "password": null,
          "hostname": null,
          "port": null
        }
      }
    ]

"""

import jc.parsers.url as url
from typing import Dict, List
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'path list string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'string', 'slurpable']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
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

    # This parser is an alias of url.py
    url.info = info  # type: ignore

    raw_output: List[Dict] = []
    if jc.utils.has_data(data):
        for line in data.split(":"):
            parsed_line = url.parse(
                line,
                raw=raw,
                quiet=quiet
            )
            raw_output.append(parsed_line)

    return raw_output if raw else _process(raw_output)
