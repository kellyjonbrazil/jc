"""jc - JSON Convert openvpn-status.log file parser

The `*_epoch` calculated timestamp fields are naive. (i.e. based on
the local time of the system the parser is run on)

Usage (cli):

    $ cat openvpn-status.log | jc --openvpn

Usage (module):

    import jc
    result = jc.parse('openvpn', openvpn_status_log_file_output)

Schema:

    {
      "clients": [
        {
          "common_name":                        string,
          "real_address":                       string,
          "real_address_prefix":                integer,  # [0]
          "real_address_port":                  integer,  # [0]
          "bytes_received":                     integer,
          "bytes_sent":                         integer,
          "connected_since":                    string,
          "connected_since_epoch":              integer,
          "updated":                            string,
          "updated_epoch":                      integer,
        }
      ],
      "routing_table": [
        {
          "virtual_address":                    string,
          "virtual_address_prefix":             integer,  # [0]
          "virtual_address_port":               integer,  # [0]
          "common_name":                        string,
          "real_address":                       string,
          "real_address_prefix":                integer,  # [0]
          "real_address_port":                  integer,  # [0]
          "last_reference":                     string,
          "last_reference_epoch":               integer,
        }
      ],
      "global_stats": {
        "max_bcast_mcast_queue_len":            integer
      }
    }

    [0] null/None if not found

Examples:

    $ cat openvpn-status.log | jc --openvpn -p
    {
      "clients": [
        {
          "common_name": "foo@example.com",
          "real_address": "10.10.10.10",
          "bytes_received": 334948,
          "bytes_sent": 1973012,
          "connected_since": "Thu Jun 18 04:23:03 2015",
          "updated": "Thu Jun 18 08:12:15 2015",
          "real_address_prefix": null,
          "real_address_port": 49502,
          "connected_since_epoch": 1434626583,
          "updated_epoch": 1434640335
        },
        {
          "common_name": "foo@example.com",
          "real_address": "10.10.10.10",
          "bytes_received": 334948,
          "bytes_sent": 1973012,
          "connected_since": "Thu Jun 18 04:23:03 2015",
          "updated": "Thu Jun 18 08:12:15 2015",
          "real_address_prefix": null,
          "real_address_port": 49503,
          "connected_since_epoch": 1434626583,
          "updated_epoch": 1434640335
        }
      ],
      "routing_table": [
        {
          "virtual_address": "192.168.255.118",
          "common_name": "baz@example.com",
          "real_address": "10.10.10.10",
          "last_reference": "Thu Jun 18 08:12:09 2015",
          "virtual_address_prefix": null,
          "virtual_address_port": null,
          "real_address_prefix": null,
          "real_address_port": 63414,
          "last_reference_epoch": 1434640329
        },
        {
          "virtual_address": "10.200.0.0",
          "common_name": "baz@example.com",
          "real_address": "10.10.10.10",
          "last_reference": "Thu Jun 18 08:12:09 2015",
          "virtual_address_prefix": 16,
          "virtual_address_port": null,
          "real_address_prefix": null,
          "real_address_port": 63414,
          "last_reference_epoch": 1434640329
        }
      ],
      "global_stats": {
        "max_bcast_mcast_queue_len": 0
      }
    }

    $ cat openvpn-status.log | jc --openvpn -p -r
    {
      "clients": [
        {
          "common_name": "foo@example.com",
          "real_address": "10.10.10.10:49502",
          "bytes_received": "334948",
          "bytes_sent": "1973012",
          "connected_since": "Thu Jun 18 04:23:03 2015",
          "updated": "Thu Jun 18 08:12:15 2015"
        },
        {
          "common_name": "foo@example.com",
          "real_address": "10.10.10.10:49503",
          "bytes_received": "334948",
          "bytes_sent": "1973012",
          "connected_since": "Thu Jun 18 04:23:03 2015",
          "updated": "Thu Jun 18 08:12:15 2015"
        }
      ],
      "routing_table": [
        {
          "virtual_address": "192.168.255.118",
          "common_name": "baz@example.com",
          "real_address": "10.10.10.10:63414",
          "last_reference": "Thu Jun 18 08:12:09 2015"
        },
        {
          "virtual_address": "10.200.0.0/16",
          "common_name": "baz@example.com",
          "real_address": "10.10.10.10:63414",
          "last_reference": "Thu Jun 18 08:12:09 2015"
        }
      ],
      "global_stats": {
        "max_bcast_mcast_queue_len": "0"
      }
    }
"""
import re
import ipaddress
from typing import List, Dict, Tuple
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'openvpn-status.log file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version


def _split_addr(addr_str: str) -> Tuple:
    """Check the type of address (v4, v6, mac) and split out the address,
    prefix, and port. Values are None if they don't exist."""
    address = possible_addr = prefix = port = possible_port = None

    try:
        address, prefix = addr_str.rsplit('/', maxsplit=1)
    except Exception:
        address = addr_str

    # is this a mac address? then stop
    if re.match(r'(?:\S\S\:){5}\S\S', address):
        return address, prefix, port

    # is it an ipv4 with port or just ipv6?
    if ':' in address:
        try:
            possible_addr, possible_port = address.rsplit(':', maxsplit=1)
            _ = ipaddress.IPv4Address(possible_addr)
            address = possible_addr
            port = possible_port
        # assume it was an IPv6 address
        except Exception:
            pass

    return address, prefix, port


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list = {'bytes_received', 'bytes_sent', 'max_bcast_mcast_queue_len'}
    date_fields = {'connected_since', 'updated', 'last_reference'}
    addr_fields = {'real_address', 'virtual_address'}

    if 'clients' in proc_data:
        for item in proc_data['clients']:
            for k, v in item.copy().items():
                if k in int_list:
                    item[k] = jc.utils.convert_to_int(v)

                if k in date_fields:
                    dt = jc.utils.timestamp(item[k], format_hint=(1000,))
                    item[k + '_epoch'] = dt.naive

                if k in addr_fields:
                    addr, prefix, port = _split_addr(v)
                    item[k] = addr
                    item[k + '_prefix'] = jc.utils.convert_to_int(prefix)
                    item[k + '_port'] = jc.utils.convert_to_int(port)

    if 'routing_table' in proc_data:
        for item in proc_data['routing_table']:
            for k, v in item.copy(). items():
                if k in date_fields:
                    dt = jc.utils.timestamp(item[k], format_hint=(1000,))
                    item[k + '_epoch'] = dt.naive

                if k in addr_fields:
                    addr, prefix, port = _split_addr(v)
                    item[k] = addr
                    item[k + '_prefix'] = jc.utils.convert_to_int(prefix)
                    item[k + '_port'] = jc.utils.convert_to_int(port)

    if 'global_stats' in proc_data:
        for k, v in proc_data['global_stats'].items():
            if k in int_list:
                if k in int_list:
                    proc_data['global_stats'][k] = jc.utils.convert_to_int(v)

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
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
    clients: List[Dict] = []
    routing_table: List[Dict] = []
    global_stats: Dict = {}
    section: str = ''  # clients, routing, stats
    updated: str = ''

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            if line.startswith('OpenVPN CLIENT LIST'):
                section = 'clients'
                continue

            if line.startswith('ROUTING TABLE'):
                section = 'routing'
                continue

            if line.startswith('GLOBAL STATS'):
                section = 'stats'
                continue

            if line.startswith('END'):
                break

            if section == 'clients' and line.startswith('Updated,'):
                _, updated = line.split(',', maxsplit=1)
                continue

            if section == 'clients' and line.startswith('Common Name,Real Address,'):
                continue

            if section == 'clients':
                c_name, real_addr, r_bytes, s_bytes, connected = line.split(',', maxsplit=5)
                clients.append(
                    {
                        'common_name': c_name,
                        'real_address': real_addr,
                        'bytes_received': r_bytes,
                        'bytes_sent': s_bytes,
                        'connected_since': connected,
                        'updated': updated
                    }
                )
                continue

            if section == 'routing' and line.startswith('Virtual Address,Common Name,'):
                continue

            if section == 'routing':
                # Virtual Address,Common Name,Real Address,Last Ref
                # 192.168.255.118,baz@example.com,10.10.10.10:63414,Thu Jun 18 08:12:09 2015
                virt_addr, c_name, real_addr, last_ref = line.split(',', maxsplit=4)
                route = {
                    'virtual_address': virt_addr,
                    'common_name': c_name,
                    'real_address': real_addr,
                    'last_reference': last_ref
                }

                # fixup for virtual addresses ending in "C"
                if 'virtual_address' in route:
                    if route['virtual_address'].endswith('C'):
                        route['virtual_address'] = route['virtual_address'][:-1]

                routing_table.append(route)
                continue

            if section == "stats":
                if line.startswith('Max bcast/mcast queue length'):
                    global_stats['max_bcast_mcast_queue_len'] = line.split(',', maxsplit=1)[1]
                    continue

        raw_output['clients'] = clients
        raw_output['routing_table'] = routing_table
        raw_output['global_stats'] = {}
        raw_output['global_stats'].update(global_stats)

    return raw_output if raw else _process(raw_output)
