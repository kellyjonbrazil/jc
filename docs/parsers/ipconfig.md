[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ipconfig"></a>

# jc.parsers.ipconfig

jc - JSON Convert `ipconfig` Windows command output parser

Usage (cli):

    $ ipconfig /all | jc --ipconfig
    $ ipconfig | jc --ipconfig
    $ jc ipconfig /all

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
              "status":                        string,
            },
          ],
          "temporary_ipv6_addresses": [
            {
              "address":                       string,
              "status":                        string,
            },
          ],
          "link_local_ipv6_addresses": [
            {
              "address":                       string,
              "status":                        string,
              "prefix_length":                 integer,
            }
          ],
          "ipv4_addresses": [
            {
              "address":                       string,     # [2]
              "subnet_mask":                   string,
              "status":                        string,
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
          "lease_expires":                     string,
          "lease_expires_epoch":               integer,    # [0]
          "lease_expires_iso":                 string,
          "lease_obtained":                    string,
          "lease_obtained_epoch":              integer,    # [0]
          "lease_obtained_iso":                string,
          "netbios_over_tcpip":                boolean,
          "media_state":                       string,
          "extras": [
            <string>:                          string
          ]
        }
      ],
      "extras": []
    }

    Notes:
      [0] - The epoch calculated timestamp field is naive. (i.e. based on
            the local time of the system the parser is run on)
      [1] - 'autoconfigured' under 'ipv4_address' is only providing
            indication if the ipv4 address was labeled as "Autoconfiguration
            IPv4 Address" vs "IPv4 Address". It does not infer any
            information from other fields
      [2] - Windows XP uses 'IP Address' instead of 'IPv4 Address'. Both
            values are parsed to the 'ipv4_address' object for consistency

Examples:

    $ ipconfig /all | jc --ipconfig -p
    {
      "host_name": "DESKTOP-WIN11-HOME",
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
          "connection_specific_dns_suffix_search_list": [],
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
          "connection_specific_dns_suffix_search_list": [],
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
          "connection_specific_dns_suffix_search_list": [],
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
          "connection_specific_dns_suffix_search_list": [],
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
          "connection_specific_dns_suffix_search_list": [],
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
          "connection_specific_dns_suffix_search_list": [],
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
          "connection_specific_dns_suffix_search_list": [],
          "description": "VMware Virtual Ethernet Adapter for VMnet1",
          "physical_address": "00-50-56-CC-27-73",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [
            {
              "address": "fe80::f47d:9c7f:69dc:591e",
              "prefix_length": 8,
              "status": "Preferred"
            }
          ],
          "ipv4_addresses": [
            {
              "address": "192.168.181.1",
              "subnet_mask": "255.255.255.0",
              "status": "Preferred",
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
          "connection_specific_dns_suffix_search_list": [],
          "description": "VMware Virtual Ethernet Adapter for VMnet8",
          "physical_address": "00-50-56-C9-A3-78",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [],
          "temporary_ipv6_addresses": [],
          "link_local_ipv6_addresses": [
            {
              "address": "fe80::4551:bf0d:59dd:a4f0",
              "prefix_length": 10,
              "status": "Preferred"
            }
          ],
          "ipv4_addresses": [
            {
              "address": "192.168.213.1",
              "subnet_mask": "255.255.255.0",
              "status": "Preferred",
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
          "connection_specific_dns_suffix_search_list": [],
          "description": "Intel(R) Wi-Fi 6 AX200 160MHz",
          "physical_address": "A8-7E-EA-55-26-B0",
          "dhcp_enabled": true,
          "autoconfiguration_enabled": true,
          "ipv6_addresses": [
            {
              "address": "fd63:cc9c:65eb:3f95:57c2:aa:10d8:db08",
              "status": "Preferred"
            }
          ],
          "temporary_ipv6_addresses": [
            {
              "address": "fd63:cc9c:65eb:3f95:8928:348e:d692:b7ef",
              "status": "Preferred"
            }
          ],
          "link_local_ipv6_addresses": [
            {
              "address": "fe80::4fae:1380:5a1b:8b6b",
              "prefix_length": 11,
              "status": "Preferred"
            }
          ],
          "ipv4_addresses": [
            {
              "address": "192.168.1.169",
              "subnet_mask": "255.255.255.0",
              "status": "Preferred",
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
          "connection_specific_dns_suffix_search_list": [],
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

<a id="jc.parsers.ipconfig.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Parsed dictionary. The raw and processed data structures are the same.

### Parser Information
Compatibility:  windows

Source: [`jc/parsers/ipconfig.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ipconfig.py)

Version 1.0 by joehacksalot (joehacksalot@gmail.com)
