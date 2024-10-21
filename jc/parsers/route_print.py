r"""jc - JSON Convert `route-print` command output parser


Usage (cli):

    $ route print | jc --route-print

Usage (module):

    import jc
    result = jc.parse('route-print', route_print_command_output)

Schema:

    {
        "interface_list": [
            {
                "interface_index": integer,
                "mac_address": string,
                "description": string
            }
        ],
        "ipv4_route_table": {
            "active_routes": [
                {
                    "network_destination": string,
                    "netmask": string,
                    "gateway": string,
                    "interface": string,
                    "metric": string
                }
            ],
            "persistent_routes": [
                {
                    "network_address": string,
                    "netmask": string,
                    "gateway_address": string,
                    "metric": string
                }
            ]
        },
        "ipv6_route_table": {
            "active_routes": [
                {
                    "interface": integer,
                    "metric": string,
                    "network_destination": string,
                    "gateway": string
                }
            ],
            "persistent_routes": [
                {
                    "interface": integer,
                    "metric": string,
                    "network_destination": string,
                    "gateway": string
                }
            ]
        }
    }

    Notes:
        - The `metric` field is typically an integer but can sometimes be set to "Default"


Examples:

    $ route print | jc --route-print -p | jq
    
        {
      "interface_list": [
        {
          "interface_index": 28,
          "mac_address": null,
          "description": "Tailscale Tunnel"
        },
        {
          "interface_index": 12,
          "mac_address": "00:1c:42:da:01:6a",
          "description": "Parallels VirtIO Ethernet Adapter"
        },
        {
          "interface_index": 1,
          "mac_address": null,
          "description": "Software Loopback Interface 1"
        }
      ],
      "ipv4_route_table": {
        "active_routes": [
          {
            "network_destination": "0.0.0.0",
            "netmask": "0.0.0.0",
            "gateway": "10.211.55.1",
            "interface": "10.211.55.3",
            "metric": "15"
          },
          {
            "network_destination": "10.0.0.0",
            "netmask": "255.0.0.0",
            "gateway": "192.168.22.1",
            "interface": "10.211.55.3",
            "metric": "16"
          },
          {
            "network_destination": "10.0.1.0",
            "netmask": "255.255.255.0",
            "gateway": "192.168.22.1",
            "interface": "10.211.55.3",
            "metric": "16"
          },
          {
            "network_destination": "10.0.3.0",
            "netmask": "255.255.255.0",
            "gateway": "192.168.22.1",
            "interface": "10.211.55.3",
            "metric": "16"
          },
          {
            "network_destination": "10.0.4.0",
            "netmask": "255.255.255.0",
            "gateway": "192.168.22.1",
            "interface": "10.211.55.3",
            "metric": "16"
          },
          {
            "network_destination": "10.211.55.0",
            "netmask": "255.255.255.0",
            "gateway": "On-link",
            "interface": "10.211.55.3",
            "metric": "271"
          },
          {
            "network_destination": "10.211.55.3",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "10.211.55.3",
            "metric": "271"
          },
          {
            "network_destination": "10.211.55.255",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "10.211.55.3",
            "metric": "271"
          },
          {
            "network_destination": "127.0.0.0",
            "netmask": "255.0.0.0",
            "gateway": "On-link",
            "interface": "127.0.0.1",
            "metric": "331"
          },
          {
            "network_destination": "127.0.0.1",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "127.0.0.1",
            "metric": "331"
          },
          {
            "network_destination": "127.255.255.255",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "127.0.0.1",
            "metric": "331"
          },
          {
            "network_destination": "169.254.0.0",
            "netmask": "255.255.0.0",
            "gateway": "On-link",
            "interface": "169.254.83.107",
            "metric": "261"
          },
          {
            "network_destination": "169.254.83.107",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "169.254.83.107",
            "metric": "261"
          },
          {
            "network_destination": "169.254.255.255",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "169.254.83.107",
            "metric": "261"
          },
          {
            "network_destination": "224.0.0.0",
            "netmask": "240.0.0.0",
            "gateway": "On-link",
            "interface": "127.0.0.1",
            "metric": "331"
          },
          {
            "network_destination": "224.0.0.0",
            "netmask": "240.0.0.0",
            "gateway": "On-link",
            "interface": "10.211.55.3",
            "metric": "271"
          },
          {
            "network_destination": "255.255.255.255",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "127.0.0.1",
            "metric": "331"
          },
          {
            "network_destination": "255.255.255.255",
            "netmask": "255.255.255.255",
            "gateway": "On-link",
            "interface": "10.211.55.3",
            "metric": "271"
          }
        ],
        "persistent_routes": [
          {
            "network_address": "10.0.1.0",
            "netmask": "255.255.255.0",
            "gateway_address": "192.168.22.1",
            "metric": "1"
          },
          {
            "network_address": "10.0.3.0",
            "netmask": "255.255.255.0",
            "gateway_address": "192.168.22.1",
            "metric": "1"
          },
          {
            "network_address": "10.0.4.0",
            "netmask": "255.255.255.0",
            "gateway_address": "192.168.22.1",
            "metric": "1"
          },
          {
            "network_address": "10.0.0.0",
            "netmask": "255.0.0.0",
            "gateway_address": "192.168.22.1",
            "metric": "1"
          }
        ]
      },
      "ipv6_route_table": {
        "active_routes": [
          {
            "interface": 1,
            "metric": "331",
            "network_destination": "::1/128",
            "gateway": "On-link"
          },
          {
            "interface": 12,
            "metric": "271",
            "network_destination": "2001:db8::/64",
            "gateway": "fe80::1"
          },
          {
            "interface": 12,
            "metric": "271",
            "network_destination": "fdb2:2c26:f4e4::/64",
            "gateway": "On-link"
          },
          {
            "interface": 12,
            "metric": "271",
            "network_destination": "fdb2:2c26:f4e4:0:670f:fec7:75b7:eb83/128",
            "gateway": "On-link"
          },
          {
            "interface": 12,
            "metric": "271",
            "network_destination": "fdb2:2c26:f4e4:0:b4d5:8083:6ce6:37d/128",
            "gateway": "On-link"
          },
          {
            "interface": 12,
            "metric": "271",
            "network_destination": "fe80::/64",
            "gateway": "On-link"
          },
          {
            "interface": 12,
            "metric": "271",
            "network_destination": "fe80::4abd:fa70:3d36:83fd/128",
            "gateway": "On-link"
          },
          {
            "interface": 1,
            "metric": "331",
            "network_destination": "ff00::/8",
            "gateway": "On-link"
          },
          {
            "interface": 12,
            "metric": "271",
            "network_destination": "ff00::/8",
            "gateway": "On-link"
          }
        ],
        "persistent_routes": [
          {
            "interface": 0,
            "metric": "4294967295",
            "network_destination": "2001:db8::/64",
            "gateway": "fe80::1"
          }
        ]
      }
    }
"""

import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`route-print` command parser'
    author = 'joehacksalot'
    author_email = 'joehacksalot@gmail.com'
    compatible = ['windows']
    magic_commands = ['route-print']
    tags = ['command']


__version__ = info.version


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Parsed dictionary. The raw and processed data structures are the same.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}
    if jc.utils.has_data(data):
        try:
            raw_output = _parse(data)
            return raw_output if raw else _process(raw_output)
        except Exception as e:
            if not quiet:
                jc.utils.warning_message(['Could not parse data due to unexpected format.'])
            return {}

def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Processed Dictionary. Structured data to conform to the schema.
    """
    for interface in proc_data['interface_list']:
        if interface["mac_address"] == '' or interface["mac_address"] == '00 00 00 00 00 00 00 e0':  # Placeholder MAC address for virtual adapters
            mac_address = None
        else:
            mac_address = interface["mac_address"].replace(" ", ":")
        interface["mac_address"] = mac_address
        interface["interface_index"] = int(interface["interface_index"],0) # allow failure to convert to int exception to flow upwards
    for ipv6_active_route in proc_data['ipv6_route_table']['active_routes']:
        ipv6_active_route["interface"] = int(ipv6_active_route["interface"],0)
    for ipv6_persistent_route in proc_data['ipv6_route_table']['persistent_routes']:
        ipv6_persistent_route["interface"] = int(ipv6_persistent_route["interface"],0)
    return proc_data # No further processing is needed


class _PushbackIterator:
    """Iterator that allows pushing back values onto the iterator. Supports handing off
       parsing to localized parsers while maintaining line synchonization."""
    
    def __init__(self, iterator):
        self.iterator = iterator
        self.pushback_stack = []

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.pushback_stack:
            return self.pushback_stack.pop()
        else:
            return next(self.iterator)

    def pushback(self, value):
        self.pushback_stack.append(value)

    def contains(self, pattern):
        iter_lines = list(self.iterator)
        list_lines = self.pushback_stack.copy()
        list_lines.extend(iter_lines)
        self.iterator = iter(list_lines)
        self.pushback_stack = []

        # Check the pushback stack first
        for line in list_lines:
            if re.match(pattern, line):
                return True
        return False

    def skip_until(self, pattern):
        for line in self:
            if re.match(pattern, line):
                return line
        return None


def _parse_interface_list(data, lines_iter):
    start_of_interface_list_pattern = r'^Interface List'
    if lines_iter.contains(start_of_interface_list_pattern):
        line = lines_iter.skip_until(start_of_interface_list_pattern)
        for line in lines_iter:
            if re.match(r'^=+$', line):
                break  # End of interface list
            interface_index = line[:5].replace(".", "").strip()
            mac_address = line[5:30].replace(".","").strip()
            description = line[30:].strip()
            data['interface_list'].append({
                "interface_index": interface_index,
                "mac_address": mac_address,
                "description": description
            })

def _parse_ipv4_route_table(data, lines_iter):
    def _parse_ipv4_active_routes(data, lines_iter):
        line = lines_iter.skip_until(r'^Active Routes')
        line = next(lines_iter, '') # Skip the header line
        if line.strip() == 'None':
            return
        for line in lines_iter:
            if re.match(r'^=+$', line):
                break  # End of interface list
            if 'Default Gateway' in line:
                continue
            lines_split = line.split()
            network_destination = lines_split[0]
            netmask = lines_split[1]
            gateway = lines_split[2]
            interface = lines_split[3]
            metric = lines_split[4]
            data['ipv4_route_table']["active_routes"].append({
                "network_destination": network_destination,
                "netmask": netmask,
                "gateway": gateway,
                "interface": interface,
                "metric": metric
            })
    
    def _parse_ipv4_persistent_routes(data, lines_iter):
        line = lines_iter.skip_until(r'^Persistent Routes')
        line = next(lines_iter, '') # line is either "None" and we abort parsing this section or we skip header line
        if line.strip() == 'None':
            return
        for line in lines_iter:
            if re.match(r'^=+$', line):
                break 
            lines_split = line.split()
            network_address = lines_split[0]
            netmask = lines_split[1]
            gateway_address = lines_split[2]
            metric = lines_split[3]
            data['ipv4_route_table']["persistent_routes"].append({
                "network_address": network_address,
                "netmask": netmask,
                "gateway_address": gateway_address,
                "metric": metric
            })

    start_of_ipv4_route_table_pattern = r'^IPv4 Route Table'
    if lines_iter.contains(start_of_ipv4_route_table_pattern):
        line = lines_iter.skip_until(start_of_ipv4_route_table_pattern)
        line = next(lines_iter, '') # Skip the separator line
        _parse_ipv4_active_routes(data, lines_iter)
        _parse_ipv4_persistent_routes(data, lines_iter)

def _parse_ipv6_route_table(data, lines_iter):
    def _parse_ipv6_active_routes(data, lines_iter):
        line = lines_iter.skip_until(r'^Active Routes')
        line = next(lines_iter, '') # line is either "None" and we abort parsing this section or we skip header line
        if line.strip() == 'None':
            return
        for line in lines_iter:
            if re.match(r'^=+$', line):
                break
            split_line = line.split()
            interface = split_line[0]
            metric = split_line[1]
            network_destination = split_line[2]
            if len(split_line) > 3:
                gateway = split_line[3]
            else:
                gateway = next(lines_iter, '').strip()
            data['ipv6_route_table']["active_routes"].append({
                "interface": interface,
                "metric": metric,
                "network_destination": network_destination,
                "gateway": gateway
            })
    
    def _parse_ipv6_persistent_routes(data, lines_iter):
        line = lines_iter.skip_until(r'^Persistent Routes')
        line = next(lines_iter, '') # line is either "None" and we abort parsing this section or we skip header line
        if line.strip() == 'None':
            return
        for line in lines_iter:
            if re.match(r'^=+$', line):
                break
            split_line = line.split()
            interface = split_line[0]
            metric = split_line[1]
            network_destination = split_line[2]
            if len(split_line) > 3:
                gateway = split_line[3]
            else:
                gateway = next(lines_iter, '').strip()
            data['ipv6_route_table']["persistent_routes"].append({
                "interface": interface,
                "metric": metric,
                "network_destination": network_destination,
                "gateway": gateway
            })
    
    start_of_ipv6_route_table_pattern = r'^IPv6 Route Table'
    if lines_iter.contains(start_of_ipv6_route_table_pattern):
        line = lines_iter.skip_until(start_of_ipv6_route_table_pattern)
        line = next(lines_iter, '') # Skip the separator line
        _parse_ipv6_active_routes(data, lines_iter)
        _parse_ipv6_persistent_routes(data, lines_iter)


def _parse(output):
    data = {
        "interface_list": [],
        "ipv4_route_table": {
            "active_routes": [],
            "persistent_routes": []
        },
        "ipv6_route_table": {
            "active_routes": [],
            "persistent_routes": []
        }
    }
    
    lines = output.splitlines()
    _parse_interface_list(data, _PushbackIterator(iter(lines)))
    _parse_ipv4_route_table(data, _PushbackIterator(iter(lines)))
    _parse_ipv6_route_table(data, _PushbackIterator(iter(lines)))
    
    return data
