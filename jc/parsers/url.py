"""jc - JSON Convert URL parser

Usage (cli):

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url

Usage (module):

    import jc
    result = jc.parse('url', url_string)

Schema:

    [
      {
        "url":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url -p
    []

    $ FTP example, etc.
    []
"""
from urllib.parse import urlparse
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'URL parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
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

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}

    if jc.utils.has_data(data):
        parts = urlparse(data)

        raw_output = {
            'scheme': parts.scheme,
            'netloc': parts.netloc,
            'path': parts.path,
            'params': parts.params,
            'query': parts.query,
            'fragment': parts.fragment
        }

    return raw_output if raw else _process(raw_output)
