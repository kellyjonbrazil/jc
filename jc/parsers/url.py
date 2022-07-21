"""jc - JSON Convert URL string parser

This parser will work with naked and wrapped URL strings:

- `scheme://host/path`
- `URL:scheme://host/path`
- `<scheme://host/path>`
- `<URL:scheme://host/path>`

Two query representations are available and documented in the schema.

Normalized quoted and unquoted versions of the original URL are also
included.

Usage (cli):

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url

Usage (module):

    import jc
    result = jc.parse('url', url_string)

Schema:

    {
      "url":                       string,
      'url_encoded":               string,
      "scheme":                    string,
      "scheme_encoded":            string,
      "netloc":                    string,
      "netloc_encoded":            string,
      "path":                      string or null,
      "path_encoded":              string or null,
      "path_list": [               array or null
                                   string
      ],
      "query":                     string or Null,
      "query_encoded":             string or Null,
      "query_obj": {               object or null
        <query-key>: [             array or null
          <query-value>            string             # [0]
        ]
      },
      "fragment":                  string or null,
      "fragment_encoded":          string or null,
      "username":                  string or null,
      "password":                  string or null,
      "hostname":                  string or null,
      "port":                      integer or null,
    }

    [0] Duplicate query-keys will have their values consolidated into the
        array of query-values

Examples:

    % echo "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag" \\
           | jc --url -p
    {
      "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
      "url_encoded": "http://example.com/test/path?q1%3Dfoo%26q1%3Dbar%26q2%3Dbaz#frag",
      "scheme": "http",
      "scheme_encoded": "http",
      "netloc": "example.com",
      "netloc_encoded": "example.com",
      "path": "/test/path",
      "path_encoded": "/test/path",
      "path_list": [
        "test",
        "path"
      ],
      "query": "q1=foo&q1=bar&q2=baz",
      "query_encoded": "q1%3Dfoo%26q1%3Dbar%26q2%3Dbaz",
      "query_obj": {
        "q1": [
          "foo",
          "bar"
        ],
        "q2": [
          "baz"
        ]
      },
      "fragment": "frag",
      "fragment_encoded": "frag",
      "username": null,
      "password": null,
      "hostname": "example.com",
      "port": null
    }

    $ echo "ftp://localhost/filepath" | jc --url -p
    {
      "url": "ftp://localhost/filepath",
      "url_encoded": "ftp://localhost/filepath",
      "scheme": "ftp",
      "scheme_encoded": "ftp",
      "netloc": "localhost",
      "netloc_encoded": "localhost",
      "path": "/filepath",
      "path_encoded": "/filepath",
      "path_list": [
        "filepath"
      ],
      "query": null,
      "query_encoded": null,
      "query_obj": null,
      "fragment": null,
      "fragment_encoded": null,
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

        quoted = normalized._replace(scheme=quote_plus(normalized.scheme),
                                     netloc=quote_plus(normalized.netloc),
                                     path=quote(normalized.path),
                                     query=quote_plus(normalized.query, safe='+'),
                                     fragment=quote_plus(normalized.fragment)).geturl()

        unquoted = normalized._replace(scheme=unquote_plus(normalized.scheme),
                                       netloc=unquote_plus(normalized.netloc),
                                       path=unquote(normalized.path),
                                       query=unquote_plus(normalized.query),
                                       fragment=unquote_plus(normalized.fragment)).geturl()

        quoted_parts = urlsplit(quoted)
        unquoted_parts = urlsplit(unquoted)

        my_path = None
        encoded_path = None
        path_list = None
        query_obj = None

        if unquoted_parts.path:
            # normalize the path by removing any duplicate `/` chars
            my_path = re.sub(r'/+', '/', unquoted_parts.path)
            encoded_path = re.sub(r'/+', '/', quoted_parts.path)

            # remove first '/' and split
            path_list = my_path.replace('/', '', 1).split('/')

            if path_list == ['']:
                path_list = None

        if unquoted_parts.query:
            query_obj = parse_qs(unquoted_parts.query)

        raw_output = {
            'url': unquoted or None,
            'url_encoded': quoted or None,
            'scheme': unquoted_parts.scheme or None,
            'scheme_encoded': quoted_parts.scheme or None,
            'netloc': unquoted_parts.netloc or None,
            'netloc_encoded': quoted_parts.netloc or None,
            'path': my_path or None,
            'path_encoded': encoded_path or None,
            'path_list': path_list or None,
            'query': unquoted_parts.query or None,
            'query_encoded': quoted_parts.query or None,
            'query_obj': query_obj or None,
            'fragment': unquoted_parts.fragment or None,
            'fragment_encoded': quoted_parts.fragment or None,
            'username': unquoted_parts.username or None,
            'password': unquoted_parts.password or None,
            'hostname': unquoted_parts.hostname or None,
            'port': unquoted_parts.port or None,
        }

    return raw_output if raw else _process(raw_output)
