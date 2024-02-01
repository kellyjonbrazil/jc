"""jc - JSON Convert `Curl` string parser

Supports output of Curl when run with the HEAD option (-I)

Usage (cli):

    $ curl --head example.org | jc --curl-head

Usage (module):

    import jc
    result = jc.parse('curl-head', curl_output)

Schema:

Curl output converted to a dictionary

    {
      "key1":       string,
      "key2":       string
    }

Examples:

curl --silent --head google.com | jc --curl-head --pretty
{
  "Location": "http://www.google.com/",
  "Content-Type": "text/html; charset=UTF-8",
  "Content-Security-Policy-Report-Only": "object-src 'none';base-uri 'self';script-src 'nonce-XXXXXXXX' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp",
  "Date": "Wed, 10 Jan 2024 19:12:42 GMT",
  "Expires": "Fri, 09 Feb 2024 19:12:42 GMT",
  "Cache-Control": "public, max-age=2592000",
  "Server": "gws",
  "Content-Length": "219",
  "X-XSS-Protection": "0",
  "X-Frame-Options": "SAMEORIGIN",
  "HTTP-Version": "1.1",
  "Status-Code": "301",
  "Status-Reason": "Moved Permanently"
}
"""
import jc.utils
import re
from jc.parsers import kv


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.0'
    description = 'curl head parser'
    author = 'Michael Nietzold'
    author_email = 'https://github.com/muescha'
    details = 'Using kv from the python standard library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['generic', 'file', 'string']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary representing a Key/Value pair document.
    """
    # remove quotation marks from beginning and end of values
    for key in proc_data:
        if proc_data[key] is None:
            proc_data[key] = ''

        elif proc_data[key].startswith('"') and proc_data[key].endswith('"'):
            proc_data[key] = proc_data[key][1:-1]

        elif proc_data[key].startswith("'") and proc_data[key].endswith("'"):
            proc_data[key] = proc_data[key][1:-1]

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

    raw_output = {}

    if jc.utils.has_data(data):
        http_pattern = re.compile(r'^HTTP/(?P<version>\d+(\.\d+)?) (?P<status_code>\d+)(?: (?P<status_reason>.+))?$')

        raw_output = kv.parse(data)

        for key, value in raw_output.items():
            match = http_pattern.match(key)
            if match:
                raw_output['HTTP-Version'] = match.group('version')
                raw_output['Status-Code'] = match.group('status_code')
                raw_output['Status-Reason'] = match.group('status_reason')
                # raw_output.update(match.groupdict())
                # Remove the original HTTP line from the dictionary
                del raw_output[key]
                break  # Break after the first match

    return raw_output if raw else _process(raw_output)