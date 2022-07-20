"""jc - JSON Convert URL string parser

This parser will work with naked and wrapped URL strings:

- `scheme://host/path`
- `URL:scheme://host/path`
- `<scheme://host/path>`
- `<URL:scheme://host/path>`

Usage (cli):

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url

Usage (module):

    import jc
    result = jc.parse('url', url_string)

Schema:

    {
      "quoted":               string,
      'unquoted":             string,
      "scheme":               string,
      "netloc":               string,
      "path":                 string or null,
      "path_list": [          array or null
                              string
      ],
      "query": {              object or null
        <query-key>: [        linst or null
                              string
        ]
      },
      "query_list": [         array or null
        <query-key>:          string
      ],
      "fragment":             string or null,
      "username":             string or null,
      "password":             string or null,
      "hostname":             string or null,
      "port":                 integer or null
    }

Examples:

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url -p
    {
      "scheme": "http",
      "netloc": "example.com",
      "path": "/test/path",
      "query": {
        "q1": "foo",
        "q2": "bar"
      },
      "fragment": "frag",
      "username": null,
      "password": null,
      "hostname": "example.com",
      "port": null
    }

    $ echo "ftp://localhost/filepath" | jc --url -p
    {
      "scheme": "ftp",
      "netloc": "localhost",
      "path": "/filepath",
      "path_list": ['filepath'],
      "query": null,
      "fragment": null,
      "username": null,
      "password": null,
      "hostname": "localhost",
      "port": null
    }
"""
import re
from urllib.parse import (
    urlsplit, unwrap, parse_qs, parse_qsl, urlunsplit, quote, quote_plus,
    unquote, unquote_plus
)
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'URL string parser'
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
        parts = urlsplit(unwrap(data))
        normalized = urlsplit(urlunsplit(parts))

        quoted = normalized._replace(path=quote(normalized.path),
                                     query=quote_plus(normalized.query)).geturl()

        unquoted = normalized._replace(path=unquote(normalized.path),
                                       query=unquote_plus(normalized.query)).geturl()

        unquoted_parts = urlsplit(unquoted)

        my_path = None
        path_list = None

        if unquoted_parts.path:
            # normalize the path by removing any duplicate `/` chars
            my_path = re.sub(r'/+', '/', unquoted_parts.path)

            # remove first '/' and split
            path_list = my_path.replace('/', '', 1).split('/')
            if path_list == ['']:
                path_list = None

        if unquoted_parts.query:
            query_obj = parse_qs(unquoted_parts.query)
            query_list = parse_qsl(unquoted_parts.query)

        raw_output = {
            'quoted': quoted or None,
            'unquoted': unquoted or None,
            'scheme': parts.scheme or None,
            'netloc': parts.netloc or None,
            'path': my_path or None,
            'path_list': path_list or None,
            'query': query_obj or None,
            'query_list': query_list or None,
            'fragment': parts.fragment or None,
            'username': parts.username,
            'password': parts.password,
            'hostname': parts.hostname,
            'port': parts.port
        }

    return raw_output if raw else _process(raw_output)
