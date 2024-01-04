"""jc - JSON Convert URL string parser

Normalized, Encoded, and Decoded versions of the original URL and URL parts
are included in the output. Encoding and Decoding is best effort.

> Note: Do not use the Encoded fields for a URL that has already been
> Encoded. Similarly, do not use the Decoded fields for a URL that has
> already been Decoded.

This parser will work with naked and wrapped URL strings:

- `scheme://host/path`
- `URL:scheme://host/path`
- `<scheme://host/path>`
- `<URL:scheme://host/path>`

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

    $ echo "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag" \\
           | jc --url -p
    {
      "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
      "scheme": "http",
      "netloc": "example.com",
      "path": "/test/path",
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

import jc.parsers.url as url
from typing import Dict
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


def _process(proc_data: Dict) -> Dict:
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
    # This parser is an alias of url.py
    url.info = info  # type: ignore

    if jc.utils.has_data(data):
        raw_output = []
        for line in data.split(":"):
            parsed_line = url.parse(
                line,
                raw=raw,
                quiet=quiet
            )
            raw_output.append(parsed_line)

    return raw_output if raw else _process(raw_output)
