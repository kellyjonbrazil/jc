"""jc - JSON Convert `ifconfig` command output parser

No `ifconfig` options are supported.

Consider using the `ip` command instead of `ifconfig` as it supports native
JSON output.

Usage (cli):

    $ ifconfig | jc --ifconfig

or

    $ jc ifconfig

Usage (module):

    import jc
    result = jc.parse('ifconfig', ifconfig_command_output)

Schema:

    [
      {
        "name":                     string,
        "type":                     string,
        "metric":                   integer
        "flags":                    integer,
        "state": [
                                    string
        ],
        "mtu":                      integer,
        "mac_addr":                 string,
        "ipv4_addr":                string,    # [0]
        "ipv4_mask":                string,    # [0]
        "ipv4_bcast":               string,    # [0]
        "ipv6_addr":                string,    # [0]
        "ipv6_mask":                integer,   # [0]
        "ipv6_scope":               string,    # [0]
        "ipv6_scope_id":            string,    # [0]
        "ipv6_type":                string,    # [0]
        "rx_packets":               integer,
        "rx_bytes":                 integer,
        "rx_errors":                integer,
        "rx_dropped":               integer,
        "rx_overruns":              integer,
        "rx_frame":                 integer,
        "tx_packets":               integer,
        "tx_bytes":                 integer,
        "tx_errors":                integer,
        "tx_dropped":               integer,
        "tx_overruns":              integer,
        "tx_carrier":               integer,
        "tx_collisions":            integer,
        "options":                  string,
        "options_flags": [
                                    string
        ],
        "status":                   string,
        "hw_address":               string,
        "media":                    string,
        "media_flags": [
                                    string
        ],
        "nd6_options":              integer,
        "nd6_flags": [
                                    string
        ],
        "plugged":                  string,
        "vendor":                   string,
        "vendor_pn":                string,
        "vendor_sn":                string,
        "vendor_date":              string,
        "module_temperature":       string,
        "module_voltage":           string
        "ipv4": [
          {
            "address":              string,
            "mask":                 string,
            "broadcast":            string
          }
        ],
        "ipv6: [
          {
            "address":              string,
            "scope_id":             string,
            "mask":                 integer,
            "scope":                string,
            "type":                 string
          }
        ],
        "lanes": [
          {
            "lane":                 integer,
            "rx_power_mw":          float,
            "rx_power_dbm":         float,
            "tx_bias_ma":           float
          }
        ]
      }
    ]

    [0] these fields only pick up the last IP address in the interface
        output and are here for backwards compatibility. For information on
        all IP addresses, use the `ipv4` and `ipv6` objects which contain an
        array of IP address objects.

Examples:

    $ ifconfig ens33 | jc --ifconfig -p
    [
      {
        "name": "ens33",
        "flags": 4163,
        "state": [
          "UP",
          "BROADCAST",
          "RUNNING",
          "MULTICAST"
        ],
        "mtu": 1500,
        "type": "Ethernet",
        "mac_addr": "00:0c:29:3b:58:0e",
        "ipv4_addr": "192.168.71.137",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": 64,
        "ipv6_scope": "0x20",
        "ipv6_type": "link",
        "metric": null,
        "rx_packets": 8061,
        "rx_errors": 0,
        "rx_dropped": 0,
        "rx_overruns": 0,
        "rx_frame": 0,
        "tx_packets": 4502,
        "tx_errors": 0,
        "tx_dropped": 0,
        "tx_overruns": 0,
        "tx_carrier": 0,
        "tx_collisions": 0,
        "rx_bytes": 1514413,
        "tx_bytes": 866622,
        "ipv4": [
          {
            "address": "192.168.71.137",
            "mask": "255.255.255.0",
            "broadcast": "192.168.71.255"
          }
        ],
        "ipv6": [
          {
            "address": "fe80::c1cb:715d:bc3e:b8a0",
            "scope_id": null,
            "mask": 64,
            "scope": "0x20",
            "type": "link"
          }
        ]
      }
    ]

    $ ifconfig ens33 | jc --ifconfig -p -r
    [
      {
        "name": "ens33",
        "flags": "4163",
        "state": "UP,BROADCAST,RUNNING,MULTICAST",
        "mtu": "1500",
        "type": "Ethernet",
        "mac_addr": "00:0c:29:3b:58:0e",
        "ipv4_addr": "192.168.71.137",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": "64",
        "ipv6_scope": "0x20",
        "ipv6_type": "link",
        "metric": null,
        "rx_packets": "8061",
        "rx_errors": "0",
        "rx_dropped": "0",
        "rx_overruns": "0",
        "rx_frame": "0",
        "tx_packets": "4502",
        "tx_errors": "0",
        "tx_dropped": "0",
        "tx_overruns": "0",
        "tx_carrier": "0",
        "tx_collisions": "0",
        "rx_bytes": "1514413",
        "tx_bytes": "866622",
        "ipv4": [
          {
            "address": "192.168.71.137",
            "mask": "255.255.255.0",
            "broadcast": "192.168.71.255"
          }
        ],
        "ipv6": [
          {
            "address": "fe80::c1cb:715d:bc3e:b8a0",
            "scope_id": null,
            "mask": "64",
            "scope": "0x20",
            "type": "link"
          }
        ]
      }
    ]
"""
import re
from ipaddress import IPv4Network
from typing import List, Dict, Optional
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.3'
    description = '`ifconfig` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['ifconfig']
    tags = ['command']


__version__ = info.version


def _convert_cidr_to_quad(string: str) -> str:
    return str(IPv4Network('0.0.0.0/' + string).netmask)


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {
        'flags', 'mtu', 'ipv6_mask', 'rx_packets', 'rx_bytes', 'rx_errors', 'rx_dropped',
        'rx_overruns', 'rx_frame', 'tx_packets', 'tx_bytes', 'tx_errors', 'tx_dropped',
        'tx_overruns', 'tx_carrier', 'tx_collisions', 'metric', 'nd6_options', 'lane'
    }
    float_list = {'rx_power_mw', 'rx_power_dbm', 'tx_bias_ma'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        # convert OSX-style subnet mask to dotted quad
        if 'ipv4_mask' in entry:
            try:
                if entry['ipv4_mask'].startswith('0x'):
                    new_mask = entry['ipv4_mask']
                    new_mask = new_mask.lstrip('0x')
                    new_mask = '.'.join(str(int(i, 16)) for i in [new_mask[i:i + 2] for i in range(0, len(new_mask), 2)])
                    entry['ipv4_mask'] = new_mask
            except (ValueError, TypeError, AttributeError):
                pass

            # for new-style freebsd output convert CIDR mask to dotted-quad to match other output
            if entry['ipv4_mask'] and not '.' in entry['ipv4_mask']:
                entry['ipv4_mask'] = _convert_cidr_to_quad(entry['ipv4_mask'])

        # convert state value to an array
        if 'state' in entry:
            try:
                new_state = entry['state'].split(',')
                entry['state'] = new_state
            except (ValueError, TypeError, AttributeError):
                pass

        # conversions for list of ipv4 addresses
        if 'ipv4' in entry:
            for ip_address in entry['ipv4']:
                if 'mask' in ip_address:
                    try:
                        if ip_address['mask'].startswith('0x'):
                            new_mask = ip_address['mask']
                            new_mask = new_mask.lstrip('0x')
                            new_mask = '.'.join(str(int(i, 16)) for i in [new_mask[i:i + 2] for i in range(0, len(new_mask), 2)])
                            ip_address['mask'] = new_mask
                    except (ValueError, TypeError, AttributeError):
                        pass

                    # for new-style freebsd output convert CIDR mask to dotted-quad to match other output
                    if ip_address['mask'] and not '.' in ip_address['mask']:
                        ip_address['mask'] = _convert_cidr_to_quad(ip_address['mask'])

        # conversions for list of ipv6 addresses
        if 'ipv6' in entry:
            for ip_address in entry['ipv6']:
                if 'mask' in ip_address:
                    ip_address['mask'] = jc.utils.convert_to_int(ip_address['mask'])

        # conversions for list of lanes
        if 'lanes' in entry:
            for lane_item in entry['lanes']:
                for key in lane_item:
                    if key in int_list:
                        lane_item[key] = jc.utils.convert_to_int(lane_item[key])
                    if key in float_list:
                        lane_item[key] = jc.utils.convert_to_float(lane_item[key])

        # final conversions
        if entry.get('media_flags', None):
            entry['media_flags'] = entry['media_flags'].split(',')

        if entry.get('nd6_flags', None):
            entry['nd6_flags'] = entry['nd6_flags'].split(',')

        if entry.get('options_flags', None):
            entry['options_flags'] = entry['options_flags'].split(',')

    return proc_data


def _bundle_match(pattern_list, string):
    """Returns a match object if a string matches one of a list of patterns.
    If no match is found, returns None"""
    for pattern in pattern_list:
        match = re.search(pattern, string)
        if match:
            return match
    return None


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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
    jc.utils.input_type_check(data)

    raw_output: List[Dict] = []

    # for backwards compatibility, preset all fields to None
    interface_obj: Dict = {
        "name": None,
        "flags": None,
        "state": None,
        "mtu": None,
        "type": None,
        "mac_addr": None,
        "ipv4_addr": None,
        "ipv4_mask": None,
        "ipv4_bcast": None,
        "ipv6_addr": None,
        "ipv6_mask": None,
        "ipv6_scope": None,
        "ipv6_type": None,
        "metric": None,
        "rx_packets": None,
        "rx_errors": None,
        "rx_dropped": None,
        "rx_overruns": None,
        "rx_frame": None,
        "tx_packets": None,
        "tx_errors": None,
        "tx_dropped": None,
        "tx_overruns": None,
        "tx_carrier": None,
        "tx_collisions": None,
        "rx_bytes": None,
        "tx_bytes": None
    }

    interface_item: Dict = interface_obj.copy()
    ipv4_info: List = []
    ipv6_info: List = []
    lane_info: List = []

    # Below regular expression patterns are based off of the work of:
    # https://github.com/KnightWhoSayNi/ifconfig-parser
    # Author: threeheadedknight@protonmail.com

    # MIT License

    # Copyright (c) 2018 threeheadedknight@protonmail.com

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:

    # The above copyright notice and this permission notice shall be included in all
    # copies or substantial portions of the Software.

    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    # SOFTWARE.

    # Linux syntax
    re_linux_interface = re.compile(r'''
        (?P<name>[a-zA-Z0-9:._-]+)\s+
        Link\sencap:(?P<type>\S+\s?\S+)
        (\s+HWaddr\s+\b(?P<mac_addr>[0-9A-Fa-f:?]+))?
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_linux_ipv4 = re.compile(r'''
        inet\saddr:(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})(\s+
        Bcast:(?P<broadcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?\s+
        Mask:(?P<mask>(?:[0-9]{1,3}\.){3}[0-9]{1,3})
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_linux_ipv6 = re.compile(r'''
        inet6\saddr:\s+(?P<address>\S+)/
        (?P<mask>[0-9]+)\s+
        Scope:(?P<scope>Link|Host)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_linux_state = re.compile(r'''
        \W+(?P<state>(?:\w+\s)+)(?:\s+)?
        MTU:(?P<mtu>[0-9]+)\s+
        Metric:(?P<metric>[0-9]+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_linux_rx = re.compile(r'''
        RX\spackets:(?P<rx_packets>[0-9]+)\s+
        errors:(?P<rx_errors>[0-9]+)\s+
        dropped:(?P<rx_dropped>[0-9]+)\s+
        overruns:(?P<rx_overruns>[0-9]+)\s+
        frame:(?P<rx_frame>[0-9]+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_linux_tx = re.compile(r'''
        TX\spackets:(?P<tx_packets>[0-9]+)\s+
        errors:(?P<tx_errors>[0-9]+)\s+
        dropped:(?P<tx_dropped>[0-9]+)\s+
        overruns:(?P<tx_overruns>[0-9]+)\s+
        carrier:(?P<tx_carrier>[0-9]+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_linux_bytes = re.compile(r'''
        \W+RX\sbytes:(?P<rx_bytes>\d+)\s+\(.*\)\s+
        TX\sbytes:(?P<tx_bytes>\d+)\s+\(.*\)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_linux_tx_stats = re.compile(r'''
        collisions:(?P<tx_collisions>[0-9]+)\s+
        txqueuelen:[0-9]+
        ''', re.IGNORECASE | re.VERBOSE
    )

    # OpenBSD syntax
    re_openbsd_interface = re.compile(r'''
        (?P<name>[a-zA-Z0-9:._-]+):\s+
        flags=(?P<flags>[0-9]+)
        <(?P<state>\S+)?>\s+
        mtu\s+(?P<mtu>[0-9]+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_openbsd_ipv4 = re.compile(r'''
        inet\s(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+netmask\s+
        (?P<mask>(?:[0-9]{1,3}\.){3}[0-9]{1,3})(\s+broadcast\s+
        (?P<broadcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_openbsd_ipv6 = re.compile(r'''
        inet6\s+(?P<address>\S+)\s+
        prefixlen\s+(?P<mask>[0-9]+)\s+
        scopeid\s+(?P<scope>\w+x\w+)
        <(?P<type>link|host|global)>
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_openbsd_details = re.compile(r'''
        \S+\s+(?:(?P<mac_addr>[0-9A-Fa-f:?]+)\s+)?
        txqueuelen\s+[0-9]+\s+
        \((?P<type>\S+\s?\S+)\)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_openbsd_rx = re.compile(r'''
        RX\spackets\s(?P<rx_packets>[0-9]+)\s+
        bytes\s+(?P<rx_bytes>\d+)\s+.*
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_openbsd_rx_stats = re.compile(r'''
        RX\serrors\s(?P<rx_errors>[0-9]+)\s+
        dropped\s+(?P<rx_dropped>[0-9]+)\s+
        overruns\s+(?P<rx_overruns>[0-9]+)\s+
        frame\s+(?P<rx_frame>[0-9]+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_openbsd_tx = re.compile(r'''
        TX\spackets\s(?P<tx_packets>[0-9]+)\s+
        bytes\s+(?P<tx_bytes>\d+)\s+.*
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_openbsd_tx_stats = re.compile(r'''
        TX\serrors\s(?P<tx_errors>[0-9]+)\s+
        dropped\s+(?P<tx_dropped>[0-9]+)\s+
        overruns\s+(?P<tx_overruns>[0-9]+)\s+
        carrier\s+(?P<tx_carrier>[0-9]+)\s+
        collisions\s+(?P<tx_collisions>[0-9]+)
        ''', re.IGNORECASE | re.VERBOSE
    )

    # FreeBSD syntax
    re_freebsd_interface = re.compile(r'''
        (?P<name>[a-zA-Z0-9:._-]+):\s+
        flags=(?P<flags>[0-9]+)
        <(?P<state>\S+)>\s+
        metric\s+(?P<metric>[0-9]+)\s+
        mtu\s+(?P<mtu>[0-9]+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_ipv4 = re.compile(r'''
        inet\s(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+
        netmask\s+(?P<mask>0x\S+)(\s+
        broadcast\s+(?P<broadcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_ipv4_v2 = re.compile(r'''
        inet\s(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\/
        (?P<mask>\d+)(\s+
        broadcast\s+(?P<broadcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_ipv6 = re.compile(r'''
        \s?inet6\s(?P<address>.*?)
        (?:\%(?P<scope_id>\w+\d+))?\s
        prefixlen\s(?P<mask>\d+).*?(?=scopeid|$)  # positive lookahead for scopeid or end of line
        (?:scopeid\s(?P<scope>0x\w+))?
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_details = re.compile(r'''
        ether\s+(?P<mac_addr>[0-9A-Fa-f:?]+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_status = re.compile(r'''
        status:\s(?P<status>\w+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_hwaddr = re.compile(r'''
        hwaddr\s(?P<hw_address>[0-9A-Fa-f:?]+)
        (?:\s+media:\s(?P<media>.+)\s
        <(?P<media_flags>.+)>)?
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_media = re.compile(r'''
        media:\s(?P<media>.+)
        (?:\s+?<(?P<media_flags>.+)>)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_nd6_options = re.compile(r'''
        nd6\soptions=(?P<nd6_options>\d+)
        <(?P<nd6_flags>\S+)>
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_plugged = re.compile(r'''
        plugged:\s(?P<plugged>.+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_vendor_pn_sn_date = re.compile(r'''
        vendor:\s(?P<vendor>.+)\s
        PN:\s(?P<vendor_pn>.+)\s
        SN:\s(?P<vendor_sn>.+)\s
        DATE:\s(?P<vendor_date>.+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_temp_volts = re.compile(r'''
        module\stemperature:\s(?P<module_temperature>.+)\s
        voltage:\s(?P<module_voltage>.+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_tx_rx_power = re.compile(r'''
        RX:\s+(?P<rx_power>.+)\s+
        TX:\s(?P<tx_pwer>.+)
        ''', re.IGNORECASE | re.VERBOSE
    )
    re_freebsd_options = re.compile(r'''
        options=(?P<options>[0-9A-Fa-f]+)
        <(?P<options_flags>.+)>
        ''', re.IGNORECASE | re.VERBOSE
    )

    # this pattern is special since it is used to build the lane_info list
    re_freebsd_lane = re.compile(r'''
        lane\s(?P<lane>\d+):\s
        RX\spower:\s(?P<rx_power_mw>\S+)\smW\s
        \((?P<rx_power_dbm>\S+)\sdBm\)\s
        TX\sbias:\s(?P<tx_bias_ma>\S+)
        ''', re.IGNORECASE | re.VERBOSE
    )

    re_linux = [
        re_linux_interface, re_linux_ipv4, re_linux_ipv6, re_linux_state, re_linux_rx, re_linux_tx,
        re_linux_bytes, re_linux_tx_stats
    ]
    re_openbsd = [
        re_openbsd_interface, re_openbsd_ipv4, re_openbsd_ipv6, re_openbsd_details, re_openbsd_rx,
        re_openbsd_rx_stats, re_openbsd_tx, re_openbsd_tx_stats
    ]
    re_freebsd = [
        re_freebsd_interface, re_freebsd_ipv4, re_freebsd_ipv4_v2, re_freebsd_ipv6,
        re_freebsd_details, re_freebsd_status, re_freebsd_nd6_options, re_freebsd_plugged,
        re_freebsd_vendor_pn_sn_date, re_freebsd_temp_volts, re_freebsd_hwaddr, re_freebsd_media,
        re_freebsd_tx_rx_power, re_freebsd_options
    ]

    interface_patterns = [re_linux_interface, re_openbsd_interface, re_freebsd_interface]
    ipv4_patterns = [re_linux_ipv4, re_openbsd_ipv4, re_freebsd_ipv4, re_freebsd_ipv4_v2]
    ipv6_patterns = [re_linux_ipv6, re_openbsd_ipv6, re_freebsd_ipv6]

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):

            # Find new interface lines
            interface_match = _bundle_match(interface_patterns, line)
            if interface_match:
                if interface_item['name'] is not None:
                    if ipv4_info:
                        interface_item['ipv4'] = ipv4_info
                    if ipv6_info:
                        interface_item['ipv6'] = ipv6_info
                    if lane_info:
                        interface_item['lanes'] = lane_info
                    raw_output.append(interface_item)
                    interface_item = interface_obj.copy()
                    ipv4_info = []
                    ipv6_info = []
                    lane_info = []

                interface_item.update(interface_match.groupdict())
                continue

            ### for backwards compatibility!
            # add in old ipv4/ipv6 address fields in root of object.
            # this will only keep the last ip address in the interface output.
            # old fieldnames: ipv4_addr, ipv4_mask, ipv4_bcast, ipv6_addr, ipv6_mask, ipv6_scope
            ipv4_match_legacy = _bundle_match(ipv4_patterns, line)
            if ipv4_match_legacy:
                ipv4_dict = ipv4_match_legacy.groupdict()
                # rename to legacy names
                name_map = {
                    'address': 'ipv4_addr',
                    'mask': 'ipv4_mask',
                    'broadcast': 'ipv4_bcast'
                }
                for k, v in ipv4_dict.copy().items():
                    ipv4_dict[name_map[k]] = v
                    del ipv4_dict[k]
                interface_item.update(ipv4_dict)

            ipv6_match_legacy = _bundle_match(ipv6_patterns, line)
            if ipv6_match_legacy:
                ipv6_dict = ipv6_match_legacy.groupdict()
                # rename to legacy names
                name_map = {
                    'address': 'ipv6_addr',
                    'mask': 'ipv6_mask',
                    'broadcast': 'ipv6_bcast',
                    'scope': 'ipv6_scope',
                    'scope_id': 'ipv6_scope_id',
                    'type': 'ipv6_type'
                }
                for k, v in ipv6_dict.copy().items():
                    ipv6_dict[name_map[k]] = v
                    del ipv6_dict[k]
                interface_item.update(ipv6_dict)
            ### Backwards compatibility end

            # ipv4 information lines
            ipv4_match = _bundle_match(ipv4_patterns, line)
            if ipv4_match:
                ipv4_info.append(ipv4_match.groupdict())
                continue

            # ipv6 information lines
            ipv6_match = _bundle_match(ipv6_patterns, line)
            if ipv6_match:
                ipv6_info.append(ipv6_match.groupdict())
                continue

            # lane information lines
            lane_match = re.search(re_freebsd_lane, line)
            if lane_match:
                lane_info.append(lane_match.groupdict())
                continue

            # All other lines
            other_match = _bundle_match(re_linux + re_openbsd + re_freebsd, line)
            if other_match:
                interface_item.update(other_match.groupdict())
                continue

        if interface_item['name'] is not None:
            if ipv4_info:
                interface_item['ipv4'] = ipv4_info
            if ipv6_info:
                interface_item['ipv6'] = ipv6_info
            if lane_info:
                interface_item['lanes'] = lane_info
            raw_output.append(interface_item)

    return raw_output if raw else _process(raw_output)
