r"""jc - JSON Convert JWT string parser

> Note: `jc` will not check the integrity of the JWT payload.

Usage (cli):

    $ echo "eyJhbGciOiJIUzI1N..." | jc --jwt

Usage (module):

    import jc
    result = jc.parse('jwt', jwt_string)

Schema:

    {
      "header": {
        "alg":                    string,
        "typ":                    string
      },
      "payload": {
        <key name>:               string/integer/float/boolean/null
      },
      "signature":                string  # [0]
    }

    [0] in colon-delimited hex notation

Examples:

    % echo 'eyJhbGciOiJIUzI1N...' | jc --jwt -p
    {
      "header": {
        "alg": "HS256",
        "typ": "JWT"
      },
      "payload": {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1516239022
      },
      "signature": "49:f9:4a:c7:04:49:48:c7:8a:28:5d:90:4f:87:f0:a4:c7..."
    }
"""
from base64 import urlsafe_b64decode
import binascii
import json
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'JWT string parser'
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


def _b2a(byte_string: bytes) -> str:
    """Convert a byte string to a colon-delimited hex ascii string"""
    # need try/except since separator was only introduced in python 3.8.
    # provides compatibility for python 3.6 and 3.7.
    try:
      return binascii.hexlify(byte_string, ':').decode('utf-8')
    except TypeError:
      hex_string = binascii.hexlify(byte_string).decode('utf-8')
      colon_seperated = ':'.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
      return colon_seperated


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
        data = data.strip()
        header, payload, signature = data.split('.')

        header = urlsafe_b64decode(header + '==').decode('utf-8')
        payload = urlsafe_b64decode(payload + '==').decode('utf-8')
        signature_bytes = urlsafe_b64decode(signature + '==')

        header = json.loads(header)
        payload = json.loads(payload)
        signature = _b2a(signature_bytes)

        raw_output = {
            'header': header,
            'payload': payload,
            'signature': signature,
        }

    return raw_output if raw else _process(raw_output)
