"""jc - JSON Convert URL string parser

This parser will work with naked and wrapped URL strings:

- `scheme://host/path`
- `URL:scheme://host/path`
- `<scheme://host/path>`
- `<URL:scheme://host/path>`

Normalized encoded and decoded versions of the original URL and URL parts
are included in the output.

> Note: Do not use the encoded fields for a URL that is already encoded.

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
      "username_encoded":          string or null,
      "password":                  string or null,
      "password_encoded":          string or null,
      "hostname":                  string or null,
      "hostname_encoded":          string or null,
      "port":                      integer or null,
      "port_encoded":              string or null
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
      "username_encoded": null,
      "password": null,
      "password_encoded": null,
      "hostname": "example.com",
      "hostname_encoded": "example.com",
      "port": null,
      "port_encoded": null
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
      "username_encoded": null,
      "password": null,
      "password_encoded": null,
      "hostname": "localhost",
      "hostname_encoded": "localhost",
      "port": null,
      "port_encoded": null
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

    # Best-effort to find safe characters in each URL part. Python
    # urllib.parse.quote will always treat the following as safe: `_.-~`
    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote
    #
    # Below are additional safe chars per URL part:

    # https://datatracker.ietf.org/doc/html/rfc3986#section-3.1 (scheme)
    SCHEME_SAFE = '+'

    # https://datatracker.ietf.org/doc/html/rfc3986#section-3.2 (netloc)
    NETLOC_SAFE = '+@:[]'

    # https://datatracker.ietf.org/doc/html/rfc3986#section-3.3 (path)
    PATH_SAFE = '+/@:;,='

    # https://datatracker.ietf.org/doc/html/rfc3986#section-3.4 (query)
    QUERY_SAFE = '+/@:;,=&?'

    # https://datatracker.ietf.org/doc/html/rfc3986#section-3.5 (fragment)
    FRAGMENT_SAFE = '+/@:;,=&?'

    if jc.utils.has_data(data):
        parts = urlsplit(unwrap(data))
        normalized = urlsplit(urlunsplit(parts))

        quoted = normalized._replace(scheme=quote(normalized.scheme, safe=SCHEME_SAFE),
                                     netloc=quote(normalized.netloc, safe=NETLOC_SAFE),
                                     path=quote(normalized.path, safe=PATH_SAFE),
                                     query=quote_plus(normalized.query, safe=QUERY_SAFE),
                                     fragment=quote(normalized.fragment, safe=FRAGMENT_SAFE)).geturl()

        unquoted = normalized._replace(scheme=unquote(normalized.scheme),
                                       netloc=unquote(normalized.netloc),
                                       path=unquote(normalized.path),
                                       query=unquote_plus(normalized.query),
                                       fragment=unquote(normalized.fragment)).geturl()

        quoted_parts = urlsplit(quoted)
        unquoted_parts = urlsplit(unquoted)

        my_path = None
        encoded_path = None
        path_list = None
        query_obj = None
        encoded_username = None
        encoded_password = None
        encoded_hostname = None
        encoded_port = None

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

        if unquoted_parts.username:
            encoded_username = quote(unquoted_parts.username, safe=NETLOC_SAFE)

        if unquoted_parts.password:
            encoded_password = quote(unquoted_parts.password, safe=NETLOC_SAFE)

        if unquoted_parts.hostname:
            encoded_hostname = quote(unquoted_parts.hostname, safe=NETLOC_SAFE)

        if unquoted_parts.port:
            encoded_port = quote(str(unquoted_parts.port), safe=NETLOC_SAFE)

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
            'username_encoded': encoded_username or None,
            'password': unquoted_parts.password or None,
            'password_encoded': encoded_password or None,
            'hostname': unquoted_parts.hostname or None,
            'hostname_encoded': encoded_hostname or None,
            'port': unquoted_parts.port or None,
            'port_encoded': encoded_port or None
        }

    return raw_output if raw else _process(raw_output)
