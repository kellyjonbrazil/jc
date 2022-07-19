"""jc - JSON Convert URL string parser

Usage (cli):

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url

Usage (module):

    import jc
    result = jc.parse('url', url_string)

Schema:

    {
      "scheme":               string,
      "netloc":               string,
      "path":                 string or null,
      "query": {              object or null,
        <query-key>:          string
      },
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
      "query": null,
      "fragment": null,
      "username": null,
      "password": null,
      "hostname": "localhost",
      "port": null
    }
"""
from urllib.parse import urlparse
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
        parts = urlparse(data)
        query = {}
        query_list = []

        if parts.query:
            query_list = parts.query.split('&')

        if query_list:
            for q in query_list:
                k, v = q.split('=')
                query.update({k: v})

        raw_output = {
            'scheme': parts.scheme or None,
            'netloc': parts.netloc or None,
            'path': parts.path or None,
            'query': query or None,
            'fragment': parts.fragment or None,
            'username': parts.username,
            'password': parts.password,
            'hostname': parts.hostname,
            'port': parts.port
        }

    return raw_output if raw else _process(raw_output)
