"""jc - JSON Convert IP Address string parser

Usage (cli):

    $ echo '192.168.1.1' | jc --ip-address

Usage (module):

    import jc
    result = jc.parse('ip_address', ip_address_string)

Schema:

    [
      {
        "ip_address":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ ip_address | jc --ip_address -p
    []

    $ ip_address | jc --ip_address -p -r
    []
"""
from typing import List, Dict
import binascii
import ipaddress
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'IP Address string parser'
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


def _b2a(byte_string: bytes) -> str:
    """Convert a byte string to a colon-delimited hex ascii string"""
    # need try/except since seperator was only introduced in python 3.8.
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

        interface = ipaddress.ip_interface(data.strip())
        network_string = str(interface.network).split('/')[0]
        network_cidr = str(interface.with_prefixlen).split('/')[1]
        network = ipaddress.ip_network(f'{network_string}/{network_cidr}')

        raw_output = {
            'version': int(interface.version),
            'max_prefix_length': int(interface.max_prefixlen),
            'ip': str(interface.ip),
            'ip_compressed': str(interface.compressed),
            'ip_exploded': str(interface.exploded),
            'dns_ptr': str(interface.reverse_pointer),
            'network': network_string,
            'broadcast': str(network.broadcast_address),
            'hostmask': str(interface.with_hostmask).split('/')[1],
            'netmask': str(interface.with_netmask).split('/')[1],
            'cidr_netmask': network_cidr,
            'first_host': 1,     # implement
            'last_host': 2,      # implement
            'is_multicast': interface.is_multicast,
            'is_private': interface.is_private,
            'is_global': interface.is_global,
            'is_link_local': interface.is_link_local,
            'is_loopback': interface.is_loopback,
            'is_reserved': interface.is_reserved,
            'is_unspecified': interface.is_unspecified,
            'hex': {
                'ip': _b2a(interface.packed),
                'network': 1,       # implement
                'broadcast': 2,     # implement
                'hostmask': 3,      # implement
                'netmask': 4,       # implement
                'first_host': 1,     # implement
                'last_host': 2,      # implement
            },
            'bin': {
                'ip': 1,            # implement
                'network': 1,       # implement
                'broadcast': 2,     # implement
                'hostmask': 3,      # implement
                'netmask': 4,       # implement
                'first_host': 1,     # implement
                'last_host': 2,      # implement
            }
        }

    return raw_output if raw else _process(raw_output)
