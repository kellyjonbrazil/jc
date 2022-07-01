"""jc - JSON Convert X.509 Certificate format file parser

This parser will convert DER, PEM, and PKCS#12 encoded X.509 certificates.

Usage (cli):

    $ cat certificate.pem | jc --x509-cert

Usage (module):

    import jc
    result = jc.parse('x509_cert', x509_cert_file_output)

Schema:

    [
      {
        "x509_cert":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ cat certificate.pem | jc --x509-cert -p
    []

    $ cat certificate.der | jc --x509-cert -p -r
    []
"""
import binascii
from collections import OrderedDict
from datetime import datetime
from typing import List, Dict, Union
import jc.utils
from jc.parsers.asn1crypto import pem, x509


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'X.509 certificate file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the asn1crypto library at https://github.com/wbond/asn1crypto/releases/tag/1.5.1'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

    return proc_data


def _b2a(byte_string: bytes) -> str:
    return binascii.hexlify(byte_string, ':').decode('utf-8')


def _fix_objects(obj):
    """
    Recursively traverse the nested dictionary or list and convert objects
    into JSON serializable types.
    """
    if isinstance(obj, set):
        obj = list(obj)

    if isinstance(obj, OrderedDict):
        obj = dict(obj)

    if isinstance(obj, datetime):
        obj = int(round(obj.timestamp()))

    if isinstance(obj, bytes):
        obj = _b2a(obj)

    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, datetime):
                v = int(round(v.timestamp()))
                obj.update({k: v})
                continue

            if isinstance(v, bytes):
                v = _b2a(v)
                obj.update({k: v})
                continue

            if isinstance(v, set):
                v = list(v)
                obj.update({k: v})

            if isinstance(v, OrderedDict):
                v = dict(v)
                obj.update({k: v})

            if isinstance(v, dict):
                obj.update({k: _fix_objects(v)})
                continue

            if isinstance(v, list):
                newlist =[]
                for i in v:
                    newlist.append(_fix_objects(i))
                obj.update({k: newlist})
                continue

    if isinstance(obj, list):
        new_list = []
        for i in obj:
            new_list.append(_fix_objects(i))
        obj = new_list

    return obj


def parse(
    data: Union[str, bytes],
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)

    raw_output: List = []

    if jc.utils.has_data(data):
        # convert to bytes, if not already for PEM detection since that's
        # what pem.detect() needs. (cli.py will auto-convert to UTF-8 if it can)
        try:
            der_bytes = bytes(data, 'utf-8')  # type: ignore
        except TypeError:
            der_bytes = data  # type: ignore

        if pem.detect(der_bytes):
            type_name, headers, der_bytes = pem.unarmor(der_bytes)

        cert = x509.Certificate.load(der_bytes)

        # convert bytes to hexadecimal representation strings for JSON conversion: _b2a()
        # convert datetime objects to timestamp integers for JSON conversion:
        # timestamp = int(round(dt_obj.timestamp()))

        clean_dict = _fix_objects(cert.native)
        # import pprint
        # pprint.pprint(clean_dict)

        raw_output = clean_dict


    return raw_output if raw else _process(raw_output)
