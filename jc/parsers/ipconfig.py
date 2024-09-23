r"""jc - JSON Convert `ipconfig` command output parser


Usage (cli):

    $ ipconfig /all | jc --ipconfig
    $ ipconfig | jc --ipconfig

Usage (module):

    import jc
    result = jc.parse('ipconfig', ipconfig_command_output)

Schema:

    {
      "host_name":                             string,
      "primary_dns_suffix":                    string,
      "node_type":                             string,
      "ip_routing_enabled":                    boolean,
      "wins_proxy_enabled":                    boolean,
      "dns_suffix_search_list": [
        string
      ],
      "adapters": [
        {
          "name_long":                         string,
          "name":                              string,
          "type":                              string,
          "connection_specific_dns_suffix":    string,
          "connection_specific_dns_suffix_search_list": [
                                               string
          ]
          "description":                       string,
          "physical_address":                  string,
          "dhcp_enabled":                      boolean,
          "autoconfiguration_enabled":         boolean,
          "ipv6_addresses": [
            {
              "address":                       string,
              "preferred":                     boolean,
            },
          ],
          "temporary_ipv6_addresses": [
            {
              "address":                       string,
              "preferred":                     boolean,
            },
          ],
          "link_local_ipv6_addresses": [
            {
              "address":                       string,
              "preferred":                     boolean,
            }
          ],
          "ipv4_addresses": [
            {
              "address":                       string,     # [2]
              "subnet_mask":                   string,
              "preferred":                     boolean,
              "autoconfigured":                boolean     # [1]
            }
          ],
          "default_gateways": [
                                               string
          ],
          "dhcp_server": null,
          "dhcpv6_iaid":                       string,
          "dhcpv6_client_duid":                string,
          "dns_servers": [
                                               string
          ],
          "primary_wins_server":               string,
          "lease_expires":                     string,     # [0]
          "lease_obtained":                    string,     # [0]
          "netbios_over_tcpip":                boolean,
          "media_state":                       string,
          "extras": [
                      string:                  string
          ]
        }
      ]
    }

    Notes:
      [0] - 'lease_expires' and 'lease_obtained' are parsed to ISO8601 format date strings. if the value was unable 
            to be parsed by datetime, the fields will be in their raw form
      [1] - 'autoconfigured' under 'ipv4_address' is only providing indication if the ipv4 address was labeled as
            "Autoconfiguration IPv4 Address" vs "IPv4 Address". It does not infer any information from other fields
      [2] - Windows XP uses 'IP Address' instead of 'IPv4 Address'. Both values are parsed to the 'ipv4_address' 
            object for consistency

Examples:

    $ ipconfig /all | jc --ipconfig -p
    {
      "host_name": "DESKTOP-LHJ9K5M",
      "primary_dns_suffix": null,
      "node_type": "Hybrid",
      "ip_routing_enabled": false,
      "wins_proxy_enabled": false,
      "dns_suffix_search_list": [
        "localdomain"
      ],
      "adapters": [
        {
          "name_long": "Ethernet adapter Ethernet",
          "name": "Ethernet",
          "type": "Ethernet",
          "connection_specific_dns_suffix": null,
          "description": "Intel(R) I211 Gigabit Network Connection",
          "physical_address": "24-4B-FE-AB-43-C3",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [],
          "ipv4_addresses": [],
          "default_gateways": [],
          "dhcp_server": null,
          "dhcpv6_iaid": null,
          "dhcpv6_client_duid": null,
          "dns_servers": [],
          "primary_wins_server": null,
          "lease_expires": null,
          "lease_obtained": null,
          "netbios_over_tcpip": null,
          "media_state": "Media disconnected",
          "extras": []
        },
        {
          "name_long": "Ethernet adapter Ethernet 2",
          "name": "Ethernet 2",
          "type": "Ethernet",
          "connection_specific_dns_suffix": null,
          "description": "Realtek PCIe 2.5GbE Family Controller",
          "physical_address": "24-4B-FE-57-3D-F2",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [],
          "ipv4_addresses": [],
          "default_gateways": [],
          "dhcp_server": null,
          "dhcpv6_iaid": null,
          "dhcpv6_client_duid": null,
          "dns_servers": [],
          "primary_wins_server": null,
          "lease_expires": null,
          "lease_obtained": null,
          "netbios_over_tcpip": null,
          "media_state": "Media disconnected",
          "extras": []
        },
        {
          "name_long": "Unknown adapter OpenVPN Data Channel Offload for NordVPN",
          "name": "OpenVPN Data Channel Offload for NordVPN",
          "type": "Unknown",
          "connection_specific_dns_suffix": null,
          "description": "OpenVPN Data Channel Offload",
          "physical_address": null,
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [],
          "ipv4_addresses": [],
          "default_gateways": [],
          "dhcp_server": null,
          "dhcpv6_iaid": null,
          "dhcpv6_client_duid": null,
          "dns_servers": [],
          "primary_wins_server": null,
          "lease_expires": null,
          "lease_obtained": null,
          "netbios_over_tcpip": null,
          "media_state": "Media disconnected",
          "extras": []
        },
        {
          "name_long": "Unknown adapter Local Area Connection",
          "name": "Local Area Connection",
          "type": "Unknown",
          "connection_specific_dns_suffix": null,
          "description": "TAP-NordVPN Windows Adapter V9",
          "physical_address": "00-FF-4C-F4-5E-49",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [],
          "ipv4_addresses": [],
          "default_gateways": [],
          "dhcp_server": null,
          "dhcpv6_iaid": null,
          "dhcpv6_client_duid": null,
          "dns_servers": [],
          "primary_wins_server": null,
          "lease_expires": null,
          "lease_obtained": null,
          "netbios_over_tcpip": null,
          "media_state": "Media disconnected",
          "extras": []
        },
        {
          "name_long": "Wireless LAN adapter Local Area Connection* 1",
          "name": "Local Area Connection* 1",
          "type": "Wireless LAN",
          "connection_specific_dns_suffix": null,
          "description": "Microsoft Wi-Fi Direct Virtual Adapter",
          "physical_address": "A8-7E-EA-5A-7F-DE",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [],
          "ipv4_addresses": [],
          "default_gateways": [],
          "dhcp_server": null,
          "dhcpv6_iaid": null,
          "dhcpv6_client_duid": null,
          "dns_servers": [],
          "primary_wins_server": null,
          "lease_expires": null,
          "lease_obtained": null,
          "netbios_over_tcpip": null,
          "media_state": "Media disconnected",
          "extras": []
        },
        {
          "name_long": "Wireless LAN adapter Local Area Connection* 2",
          "name": "Local Area Connection* 2",
          "type": "Wireless LAN",
          "connection_specific_dns_suffix": null,
          "description": "Microsoft Wi-Fi Direct Virtual Adapter #2",
          "physical_address": "AA-7E-EA-F3-64-C3",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [],
          "ipv4_addresses": [],
          "default_gateways": [],
          "dhcp_server": null,
          "dhcpv6_iaid": null,
          "dhcpv6_client_duid": null,
          "dns_servers": [],
          "primary_wins_server": null,
          "lease_expires": null,
          "lease_obtained": null,
          "netbios_over_tcpip": null,
          "media_state": "Media disconnected",
          "extras": []
        },
        {
          "name_long": "Ethernet adapter VMware Network Adapter VMnet1",
          "name": "VMware Network Adapter VMnet1",
          "type": "Ethernet",
          "connection_specific_dns_suffix": null,
          "description": "VMware Virtual Ethernet Adapter for VMnet1",
          "physical_address": "00-50-56-CC-27-73",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [
            {
              "address": "fe80::f47d:9c7f:69dc:591e%8",
              "preferred": true
            }
          ],
          "ipv4_addresses": [
            {
              "address": "192.168.181.1",
              "subnet_mask": "255.255.255.0",
              "preferred": true,
              "autoconfigured": false
            }
          ],
          "default_gateways": [],
          "dhcp_server": "192.168.181.254",
          "dhcpv6_iaid": "771772502",
          "dhcpv6_client_duid": "00-01-00-01-2C-CF-19-EB-24-4B-FE-5B-9B-E6",
          "dns_servers": [],
          "primary_wins_server": null,
          "lease_expires": "2024-09-19T18:01:29",
          "lease_obtained": "2024-09-19T08:31:29",
          "netbios_over_tcpip": true,
          "media_state": null,
          "extras": []
        },
        {
          "name_long": "Ethernet adapter VMware Network Adapter VMnet8",
          "name": "VMware Network Adapter VMnet8",
          "type": "Ethernet",
          "connection_specific_dns_suffix": null,
          "description": "VMware Virtual Ethernet Adapter for VMnet8",
          "physical_address": "00-50-56-C9-A3-78",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [
            {
              "address": "fe80::4551:bf0d:59dd:a4f0%10",
              "preferred": true
            }
          ],
          "ipv4_addresses": [
            {
              "address": "192.168.213.1",
              "subnet_mask": "255.255.255.0",
              "preferred": true,
              "autoconfigured": false
            }
          ],
          "default_gateways": [],
          "dhcp_server": "192.168.213.254",
          "dhcpv6_iaid": "788549718",
          "dhcpv6_client_duid": "00-01-00-01-2C-CF-19-EB-24-4B-FE-5B-9B-E6",
          "dns_servers": [],
          "primary_wins_server": "192.168.213.2",
          "lease_expires": "2024-09-19T18:01:29",
          "lease_obtained": "2024-09-19T08:31:29",
          "netbios_over_tcpip": true,
          "media_state": null,
          "extras": []
        },
        {
          "name_long": "Wireless LAN adapter Wi-Fi",
          "name": "Wi-Fi",
          "type": "Wireless LAN",
          "connection_specific_dns_suffix": "localdomain",
          "description": "Intel(R) Wi-Fi 6 AX200 160MHz",
          "physical_address": "A8-7E-EA-55-26-B0",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [
            {
              "address": "fd63:cc9c:65eb:3f95:57c2:aa:10d8:db08",
              "preferred": true
            }
          ],
          "temporary_ipv6_addresses": [
            {
              "address": "fd63:cc9c:65eb:3f95:8928:348e:d692:b7ef",
              "preferred": true
            }
          ],
          "link_local_ipv6_addresses": [
            {
              "address": "fe80::4fae:1380:5a1b:8b6b%11",
              "preferred": true
            }
          ],
          "ipv4_addresses": [
            {
              "address": "192.168.1.169",
              "subnet_mask": "255.255.255.0",
              "preferred": true,
              "autoconfigured": false
            }
          ],
          "default_gateways": [
            "192.168.1.1"
          ],
          "dhcp_server": "192.168.1.1",
          "dhcpv6_iaid": "162037482",
          "dhcpv6_client_duid": "00-01-00-01-2C-CF-19-EB-24-4B-FE-5B-9B-E6",
          "dns_servers": [
            "192.168.1.1"
          ],
          "primary_wins_server": null,
          "lease_expires": "2024-09-20T08:31:30",
          "lease_obtained": "2024-09-19T08:31:30",
          "netbios_over_tcpip": true,
          "media_state": null,
          "extras": []
        },
        {
          "name_long": "Ethernet adapter Bluetooth Network Connection",
          "name": "Bluetooth Network Connection",
          "type": "Ethernet",
          "connection_specific_dns_suffix": null,
          "description": "Bluetooth Device (Personal Area Network)",
          "physical_address": "A8-7E-EA-43-23-14",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [],
          "ipv4_addresses": [],
          "default_gateways": [],
          "dhcp_server": null,
          "dhcpv6_iaid": null,
          "dhcpv6_client_duid": null,
          "dns_servers": [],
          "primary_wins_server": null,
          "lease_expires": null,
          "lease_obtained": null,
          "netbios_over_tcpip": null,
          "media_state": "Media disconnected",
          "extras": []
        }
      ],
      "extras": []
    }
"""
from datetime import datetime
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`ipconfig` command parser'
    author = 'joehacksalot'
    author_email = 'joehacksalot@gmail.com'
    compatible = ['windows']
    magic_commands = ['ipconfig']
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
        # Initialize the parsed output dictionary with all fields set to None or empty lists
        raw_output = _parse(data)

    return raw_output if raw else _process(raw_output)



def _process_ipv6_address(ip_address):
    preferred = True if ip_address.get("preferred","") is not None and 'preferred' in ip_address.get("preferred","") else False
    return {
              "address": ip_address["address"],
              "preferred": preferred
           }

def _process_ipv4_address(ip_address):
    preferred = True if ip_address.get("preferred","") is not None and 'preferred' in ip_address.get("preferred","") else False
    autoconfigured = True if ip_address.get("autoconfigured","") is not None and 'autoconfigured' in ip_address.get("autoconfigured","") else False
    subnet_mask = ip_address["subnet_mask"]
    return {
              "address": ip_address["address"],
              "subnet_mask": subnet_mask,
              "preferred": preferred,
              "autoconfigured": autoconfigured
          }

def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Processed Dictionary. Structured data to conform to the schema.
    """
    processed = proc_data
    
    
    if "ip_routing_enabled" in processed and processed["ip_routing_enabled"] is not None:
        processed["ip_routing_enabled"] = (processed["ip_routing_enabled"].lower() == "yes")

    if "wins_proxy_enabled" in processed and processed["wins_proxy_enabled"] is not None:
        processed["wins_proxy_enabled"] = (processed["wins_proxy_enabled"].lower() == "yes")

    for adapter in processed["adapters"]:
        if "dhcp_enabled" in adapter and adapter["dhcp_enabled"] is not None:
            adapter["dhcp_enabled"] = (adapter["dhcp_enabled"].lower() == "yes")
        if "autoconfiguration_enabled" in adapter and adapter["autoconfiguration_enabled"] is not None:
            adapter["autoconfiguration_enabled"] = (adapter["autoconfiguration_enabled"].lower() == "yes")
        if "netbios_over_tcpip" in adapter and adapter["netbios_over_tcpip"] is not None:
            adapter["netbios_over_tcpip"] = (adapter["netbios_over_tcpip"].lower() == "enabled")
        if "lease_expires" in adapter and adapter["lease_expires"] is not None and adapter["lease_expires"] != "":
            try:
                adapter["lease_expires"] = datetime.strptime(adapter["lease_expires"], "%A, %B %d, %Y %I:%M:%S %p").isoformat()
            except:
                pass # Leave date in raw format if not parseable
        if "lease_obtained" in adapter and adapter["lease_obtained"] is not None and adapter["lease_obtained"] != "":
            try:
                adapter["lease_obtained"] = datetime.strptime(adapter["lease_obtained"], "%A, %B %d, %Y %I:%M:%S %p").isoformat()
            except:
                pass # Leave date in raw format if not parseable
        adapter["ipv6_addresses"] = [_process_ipv6_address(address) for address in adapter.get("ipv6_addresses", [])]
        adapter["temporary_ipv6_addresses"] = [_process_ipv6_address(address) for address in adapter.get("temporary_ipv6_addresses", [])]
        adapter["link_local_ipv6_addresses"] = [_process_ipv6_address(address) for address in adapter.get("link_local_ipv6_addresses", [])]
        adapter["ipv4_addresses"] = [_process_ipv4_address(address) for address in adapter.get("ipv4_addresses", [])]
    return processed

class _PushbackIterator:
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

def _parse(data):
    # Initialize the parsed output dictionary with all fields set to None or empty lists
    parse_output = {
        "host_name": None,
        "primary_dns_suffix": None,
        "node_type": None,
        "ip_routing_enabled": None,
        "wins_proxy_enabled": None,
        "dns_suffix_search_list": [],
        "adapters": [],
        "extras": []  # To store unrecognized fields
    }

    lines = data.splitlines()
    lines = [line.rstrip() for line in lines if line.strip() != ""]

    line_iter = _PushbackIterator(iter(lines))
    adapter = None
    in_adapter_section = False

    for line in line_iter:
        line = line.rstrip()

        # Skip empty lines
        if not line.strip():
            continue

        # Header Section
        if not in_adapter_section:
            if "Windows IP Configuration" in line:
                continue
            elif _is_adapter_start_line(line):
                # Start of Adapter Section
                in_adapter_section = True
                adapter_name = line.strip(":").strip()
                adapter = _initialize_adapter(adapter_name)
                parse_output["adapters"].append(adapter)
            elif line.startswith("   "):
                key, value = _parse_line(line)
                if key:
                    _parse_header_line(parse_output, key, value, line_iter)
            else:
                continue
        else:
            # Adapter Sections
            if _is_adapter_start_line(line):
                # Start of new adapter
                adapter_name = line.strip(":").strip()
                adapter = _initialize_adapter(adapter_name)
                parse_output["adapters"].append(adapter)
            elif line.startswith("   "):
                key, value = _parse_line(line)
                if key:
                    _parse_adapter_line(adapter, key, value, line_iter)
            else:
                continue

    return parse_output

def _is_adapter_start_line(line):
    # Detect adapter start lines, e.g., "Ethernet adapter Ethernet:"
    return re.match(r"^[^\s].*adapter.*:", line, re.IGNORECASE)

def _initialize_adapter(adapter_name):
    adapter_name_split = adapter_name.split(" adapter ", 1)
    if len(adapter_name_split) > 1:
        adapter_type = adapter_name_split[0]
        adapter_short_name = adapter_name_split[1]
    else:
        adapter_type = None
        adapter_short_name = adapter_name

    # Initialize adapter dictionary with all fields set to None or empty lists
    return {
        "name_long": adapter_name,
        "name": adapter_short_name,
        "type": adapter_type,
        "connection_specific_dns_suffix": None,
        "connection_specific_dns_suffix_search_list": [],
        "description": None,
        "physical_address": None,
        "dhcp_enabled": None,
        "autoconfiguration_enabled": None,
        "ipv6_addresses": [],
        "temporary_ipv6_addresses": [],
        "link_local_ipv6_addresses": [],
        "ipv4_addresses": [],
        "default_gateways": [],
        "dhcp_server": None,
        "dhcpv6_iaid": None,
        "dhcpv6_client_duid": None,
        "dns_servers": [],
        "primary_wins_server": None,
        "lease_expires": None,
        "lease_obtained": None,
        "netbios_over_tcpip": None,
        "media_state": None,
        "extras": []  # To store unrecognized fields
    }

def _parse_line(line):
    # Split the line into key and value using ':' or multiple spaces
    key_value = re.split(r":", line.strip(), 1)
    if len(key_value) == 2:
        key, value = key_value
        key = key.strip().rstrip('. ')
        key = re.sub(r'[^\w]+', '_', key.lower())
        value = value.strip() if value.strip() != "" else None
        return key, value
    else:
        return None, None

def _parse_header_line(result, key, value, line_iter):
    if key == "host_name":
        result["host_name"] = value
    elif key == "primary_dns_suffix":
        result["primary_dns_suffix"] = value
    elif key == "node_type":
        result["node_type"] = value
    elif key == "ip_routing_enabled":
        result["ip_routing_enabled"] = value
    elif key == "wins_proxy_enabled":
        result["wins_proxy_enabled"] = value
    elif key == "dns_suffix_search_list":
        if value:
            result["dns_suffix_search_list"].append(value)
        # Process additional entries
        _parse_additional_entries(result["dns_suffix_search_list"], line_iter)
    else:
        # Store unrecognized fields in extras
        result["extras"].append({key: value})

def _parse_adapter_line(adapter, key, value, line_iter):
    if key == "connection_specific_dns_suffix":
        adapter["connection_specific_dns_suffix"] = value
    elif key == "media_state":
        adapter["media_state"] = value
    elif key == "description":
        adapter["description"] = value
    elif key == "physical_address":
        adapter["physical_address"] = value
    elif key == "dhcp_enabled":
        adapter["dhcp_enabled"] = value
    elif key == "autoconfiguration_enabled":
        adapter["autoconfiguration_enabled"] = value
    elif key == "dhcpv6_iaid":
        adapter["dhcpv6_iaid"] = value
    elif key == "dhcpv6_client_duid":
        adapter["dhcpv6_client_duid"] = value
    elif key == "netbios_over_tcpip":
        adapter["netbios_over_tcpip"] = value
    elif key == "dhcp_server":
        adapter["dhcp_server"] = value
    elif key == "lease_obtained":
        adapter["lease_obtained"] = value
    elif key == "lease_expires":
        adapter["lease_expires"] = value
    elif key == "primary_wins_server":
        adapter["primary_wins_server"] = value
    elif key in ["ipv6_address", "temporary_ipv6_address", "link_local_ipv6_address"]:
        address_dict = _parse_ipv6_address(value)
        if key == "ipv6_address":
            adapter["ipv6_addresses"].append(address_dict)
        elif key == "temporary_ipv6_address":
            adapter["temporary_ipv6_addresses"].append(address_dict)
        elif key == "link_local_ipv6_address":
            adapter["link_local_ipv6_addresses"].append(address_dict)
    elif key in ["ipv4_address", "autoconfiguration_ipv4_address", "ip_address", "autoconfiguration_ip_address"]:
        ipv4_address_dict = _parse_ipv4_address(value, key, line_iter)
        adapter["ipv4_addresses"].append(ipv4_address_dict)
    elif key == "connection_specific_dns_suffix_search_list":
        if value:
            adapter["connection_specific_dns_suffix_search_list"].append(value)
        # Process additional connection specific dns suffix search list entries
        _parse_additional_entries(adapter["connection_specific_dns_suffix_search_list"], line_iter)
    elif key == "default_gateway":
        if value:
            adapter["default_gateways"].append(value)
        # Process additional gateways
        _parse_additional_entries(adapter["default_gateways"], line_iter)
    elif key == "dns_servers":
        if value:
            adapter["dns_servers"].append(value)
        # Process additional DNS servers
        _parse_additional_entries(adapter["dns_servers"], line_iter)
    elif key == "subnet_mask":
        # Subnet Mask should be associated with the last IPv4 address
        if adapter["ipv4_addresses"]:
            adapter["ipv4_addresses"][-1]["subnet_mask"] = value
    else:
        # Store unrecognized fields in extras
        adapter["extras"].append({key: value})

def _parse_ipv6_address(value):
    # Handle multiple status indicators
    match = re.match(r"([^\(]+)\((.*)\)", value) if value else None
    if match:
        address = match.group(1).strip()
        statuses = match.group(2).lower().split(')(')
        statuses = [status.strip('()') for status in statuses]
        preferred = 'preferred' if 'preferred' in statuses else None
    else:
        address = value
        preferred = None
        statuses = []
    return {
        "address": address,
        "preferred": preferred,
        "statuses": statuses
    }

def _parse_ipv4_address(value, key, line_iter):
    # Handle preferred and autoconfigured status
    match = re.match(r"([^\(]+)\((.*)\)", value) if value else None
    if match:
        address = match.group(1).strip()
        statuses = match.group(2).lower().split(')(')
        statuses = [status.strip('()') for status in statuses]
        preferred = 'preferred' if 'preferred' in statuses else None
        autoconfigured = 'autoconfigured' if 'autoconfiguration' in key or 'autoconfigured' in statuses else None
    else:
        address = value
        preferred = None
        statuses = []
        autoconfigured = 'autoconfigured' if 'autoconfiguration' in key else None
    # Get subnet mask
    subnet_mask = None
    # Peek ahead for "Subnet Mask" line
    try:
        next_line = next(line_iter)
        next_key, next_value = _parse_line(next_line)
        if next_key == "subnet_mask":
            subnet_mask = next_value
        else:
            # If it's not "Subnet Mask", put it back into the iterator
            line_iter.pushback(next_line)
    except StopIteration:
        pass
    return {
            "address": address,
            "subnet_mask": subnet_mask,
            "preferred": preferred,
            "autoconfigured": autoconfigured,
            "statuses": statuses
        }

def _parse_additional_entries(entry_list, line_iter):
    # Process additional lines that belong to the current entry (e.g., additional DNS servers, DNS Suffix Search List)
    while True:
        try:
            next_line = next(line_iter)
            if not next_line.strip():
                continue  # Skip empty lines

            # Check if the line is indented (starts with whitespace)
            if re.match(r"^\s\s\s\s", next_line):
                # It's an indented line; append the stripped line to entry_list
                entry_list.append(next_line.strip())
            else:
                # Not an indented line; push it back and exit
                line_iter.pushback(next_line)
                break
        except StopIteration:
            break