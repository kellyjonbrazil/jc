"""jc - JSON Convert URL string parser

Normalized, Encoded, and Decoded versions of the original URL and URL parts
are included in the output. Encoding and Decoding is best effort.

> Note: Do not use the Encoded fields for a URL that has already been
> Encoded. Similarly, do not use the Decoded fields for a URL that has
> already been Decoded.

This parser will work with naked and wrapped URL strings:

- `/path`
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

    [0] Duplicate query-keys will have their values consolidated into the
        array of query-values

    [1] Invalid port values will be converted to null/None and a warning
        message will be printed to `STDERR` if quiet=False

Examples:

    $ echo "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag" \\
           | jc --url -p
    {
      "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
      "scheme": "http",
      "netloc": "example.com",
      "path": "/test/path",
      "parent": "/test",
      "filename": "path",
      "stem": "path",
      "extension": null,
      "path_list": [
        "test",
        "path"
      ],
      "query": "q1=foo&q1=bar&q2=baz",
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
      "username": null,
      "password": null,
      "hostname": "example.com",
      "port": null,
      "encoded": {
        "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
        "scheme": "http",
        "netloc": "example.com",
        "path": "/test/path",
        "parent": "/test",
        "filename": "path",
        "stem": "path",
        "extension": null,
        "path_list": [
          "test",
          "path"
        ],
        "query": "q1=foo&q1=bar&q2=baz",
        "fragment": "frag",
        "username": null,
        "password": null,
        "hostname": "example.com",
        "port": null
      },
      "decoded": {
        "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
        "scheme": "http",
        "netloc": "example.com",
        "path": "/test/path",
        "parent": "/test",
        "filename": "path",
        "stem": "path",
        "extension": null,
        "path_list": [
          "test",
          "path"
        ],
        "query": "q1=foo&q1=bar&q2=baz",
        "fragment": "frag",
        "username": null,
        "password": null,
        "hostname": "example.com",
        "port": null
      }
    }

    $ echo "ftp://localhost/filepath" | jc --url -p
    {
      "url": "ftp://localhost/filepath",
      "scheme": "ftp",
      "netloc": "localhost",
      "path": "/filepath",
      "parent": "/",
      "filename": "filepath",
      "stem": "filepath",
      "extension": null,
      "path_list": [
        "filepath"
      ],
      "query": null,
      "query_obj": null,
      "fragment": null,
      "username": null,
      "password": null,
      "hostname": "localhost",
      "port": null,
      "encoded": {
        "url": "ftp://localhost/filepath",
        "scheme": "ftp",
        "netloc": "localhost",
        "path": "/filepath",
        "parent": "/",
        "filename": "filepath",
        "stem": "filepath",
        "extension": null,
        "path_list": [
          "filepath"
        ],
        "query": null,
        "fragment": null,
        "username": null,
        "password": null,
        "hostname": "localhost",
        "port": null
      },
      "decoded": {
        "url": "ftp://localhost/filepath",
        "scheme": "ftp",
        "netloc": "localhost",
        "path": "/filepath",
        "parent": "/",
        "filename": "filepath",
        "stem": "filepath",
        "extension": null,
        "path_list": [
          "filepath"
        ],
        "query": null,
        "fragment": null,
        "username": null,
        "password": null,
        "hostname": "localhost",
        "port": null
      }
    }
"""
import pathlib
import re
from urllib.parse import (
    urlsplit, unwrap, parse_qs, urlunsplit, quote, quote_plus, unquote, unquote_plus
)
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'URL string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
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
        decoded_path = None
        parent = None
        encoded_parent = None
        decoded_parent = None
        filename = None
        encoded_filename = None
        decoded_filename = None
        stem = None
        encoded_stem = None
        decoded_stem = None
        extension = None
        encoded_extension = None
        decoded_extension = None
        path_list = None
        encoded_path_list = None
        decoded_path_list = None
        query_obj = None
        encoded_username = None
        decoded_username = None
        encoded_password = None
        decoded_password = None
        encoded_hostname = None
        decoded_hostname = None
        normalized_port = None
        encoded_port = None
        decoded_port = None

        if normalized.path:
            # normalize the path by removing any duplicate `/` chars
            my_path = re.sub(r'/+', '/', normalized.path)
            encoded_path = re.sub(r'/+', '/', quoted_parts.path)
            decoded_path = re.sub(r'/+', '/', unquoted_parts.path)

            # get parent, file, stem, and exension info from path
            parent = str(pathlib.PurePosixPath(my_path).parent)
            encoded_parent = str(pathlib.PurePosixPath(encoded_path).parent)
            decoded_parent = str(pathlib.PurePosixPath(decoded_path).parent)

            filename = str(pathlib.PurePosixPath(my_path).name)
            encoded_filename = str(pathlib.PurePosixPath(encoded_path).name)
            decoded_filename = str(pathlib.PurePosixPath(decoded_path).name)

            stem = str(pathlib.PurePosixPath(my_path).stem)
            encoded_stem = str(pathlib.PurePosixPath(encoded_path).stem)
            decoded_stem = str(pathlib.PurePosixPath(decoded_path).stem)

            extension = str(pathlib.PurePosixPath(my_path).suffix)[1:]
            encoded_extension = str(pathlib.PurePosixPath(encoded_path).suffix)[1:]
            decoded_extension = str(pathlib.PurePosixPath(decoded_path).suffix)[1:]

            # remove first '/' and split
            path_list = my_path.replace('/', '', 1).split('/')
            encoded_path_list = encoded_path.replace('/', '', 1).split('/')
            decoded_path_list = decoded_path.replace('/', '', 1).split('/')

            if path_list[-1] == '':
                path_list.pop()

            if encoded_path_list[-1] == '':
                encoded_path_list.pop()

            if decoded_path_list[-1] == '':
                decoded_path_list.pop()

        if normalized.query:
            query_obj = parse_qs(normalized.query)

        if normalized.username:
            encoded_username = quote(normalized.username, safe=NETLOC_SAFE)
            decoded_username = unquote(normalized.username)

        if normalized.password:
            encoded_password = quote(normalized.password, safe=NETLOC_SAFE)
            decoded_password = unquote(normalized.password)

        if normalized.hostname:
            encoded_hostname = quote(normalized.hostname, safe=NETLOC_SAFE)
            decoded_hostname = unquote(normalized.hostname)

        # handle port differently since an encoded port can cause a ValueError if it's not an integer
        try:
            if normalized.port:
                normalized_port = normalized.port
                encoded_port = int(quote(str(normalized.port), safe=NETLOC_SAFE))
                decoded_port = int(unquote(str(normalized.port)))

        except ValueError:
            # Non-integer decoded port values can also cause a ValueError
            # try unquoting, otherwise set to None if it can't be converted
            try:
                if unquoted_parts.port:
                    normalized_port = int(unquote(str(unquoted_parts.port)))
                    encoded_port = int(quote(str(unquoted_parts.port), safe=NETLOC_SAFE))
                    decoded_port = int(unquote(str(unquoted_parts.port)))

            except ValueError:
                if not quiet:
                  jc.utils.warning_message(['Unable to convert invalid port value. Setting to null.'])

                normalized_port = None
                encoded_port = None
                decoded_port = None

        raw_output = {
            'url': normalized.geturl() or None,
            'scheme': normalized.scheme or None,
            'netloc': normalized.netloc or None,
            'path': my_path or None,
            'parent': parent or None,
            'filename': filename or None,
            'stem': stem or None,
            'extension': extension or None,
            'path_list': path_list or None,
            'query': normalized.query or None,
            'query_obj': query_obj or None,
            'fragment': normalized.fragment or None,
            'username': normalized.username or None,
            'password': normalized.password or None,
            'hostname': normalized.hostname or None,
            'port': normalized_port or None,
            'encoded': {
                'url': quoted or None,
                'scheme': quoted_parts.scheme or None,
                'netloc': quoted_parts.netloc or None,
                'path': encoded_path or None,
                'parent': encoded_parent or None,
                'filename': encoded_filename or None,
                'stem': encoded_stem or None,
                'extension': encoded_extension or None,
                'path_list': encoded_path_list or None,
                'query': quoted_parts.query or None,
                'fragment': quoted_parts.fragment or None,
                'username': encoded_username or None,
                'password': encoded_password or None,
                'hostname': encoded_hostname or None,
                'port': encoded_port or None,
            },
            'decoded': {
                'url': unquoted or None,
                'scheme': unquoted_parts.scheme or None,
                'netloc': unquoted_parts.netloc or None,
                'path': decoded_path or None,
                'parent': decoded_parent or None,
                'filename': decoded_filename or None,
                'stem': decoded_stem or None,
                'extension': decoded_extension or None,
                'path_list': decoded_path_list or None,
                'query': unquoted_parts.query or None,
                'fragment': unquoted_parts.fragment or None,
                'username': decoded_username or None,
                'password': decoded_password or None,
                'hostname': decoded_hostname or None,
                'port': decoded_port or None,
            }
        }

    return raw_output if raw else _process(raw_output)
