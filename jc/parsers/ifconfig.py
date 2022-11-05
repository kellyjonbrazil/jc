"""jc - JSON Convert `foo` command output parser

<<Short foo description and caveats>>

Usage (cli):

    $ foo | jc --foo

or

    $ jc foo

Usage (module):

    import jc
    result = jc.parse('foo', foo_command_output)

Schema:

    [
      {
        "foo":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ foo | jc --foo -p
    []

    $ foo | jc --foo -p -r
    []
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.0'
    description = '`ifconfig` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using ifconfig-parser from https://github.com/KnightWhoSayNi/ifconfig-parser'
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['ifconfig']


__version__ = info.version


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
        'tx_overruns', 'tx_carrier', 'tx_collisions', 'metric'
    }

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        # convert OSX-style subnet mask to dotted quad
        if 'ipv4_mask' in entry:
            try:
                if entry['ipv4_mask'].startswith('0x'):  # type: ignore
                    new_mask = entry['ipv4_mask']
                    new_mask = new_mask.lstrip('0x')  # type: ignore
                    new_mask = '.'.join(str(int(i, 16)) for i in [new_mask[i:i + 2] for i in range(0, len(new_mask), 2)])
                    entry['ipv4_mask'] = new_mask
            except (ValueError, TypeError, AttributeError):
                pass

        # convert state value to an array
        if 'state' in entry:
            try:
                new_state = entry['state'].split(',')  # type: ignore
                entry['state'] = new_state
            except (ValueError, TypeError, AttributeError):
                pass

        # conversions for list of ipv4 addresses
        if 'ipv4' in entry:
            for ip_address in entry['ipv4']:  # type: ignore
                if 'mask' in ip_address:
                    try:
                        if ip_address['mask'].startswith('0x'):  # type: ignore
                            new_mask = ip_address['mask']  # type: ignore
                            new_mask = new_mask.lstrip('0x')
                            new_mask = '.'.join(str(int(i, 16)) for i in [new_mask[i:i + 2] for i in range(0, len(new_mask), 2)])
                            ip_address['mask'] = new_mask  # type: ignore
                    except (ValueError, TypeError, AttributeError):
                        pass

        # conversions for list of ipv6 addresses
        if 'ipv6' in entry:
            for ip_address in entry['ipv6']:  # type: ignore
                if 'mask' in ip_address:
                    ip_address['mask'] = jc.utils.convert_to_int(ip_address['mask'])  # type: ignore

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
    interface_item: Dict = {}
    ipv4_info: List = []
    ipv6_info: List = []

    # Linux syntax
    re_linux_interface = re.compile(
        r"(?P<name>[a-zA-Z0-9:._-]+)\s+Link encap:(?P<type>\S+\s?\S+)(\s+HWaddr\s+\b"
        r"(?P<mac_addr>[0-9A-Fa-f:?]+))?",
        re.I)
    re_linux_ipv4 = re.compile(
        r"inet addr:(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})(\s+Bcast:"
        r"(?P<broadcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?\s+Mask:(?P<mask>(?:[0-9]{1,3}\.){3}[0-9]{1,3})",
        re.I)
    re_linux_ipv6 = re.compile(
        r"inet6 addr:\s+(?P<address>\S+)/(?P<mask>[0-9]+)\s+Scope:(?P<scope>Link|Host)",
        re.I)
    re_linux_state = re.compile(
        r"\W+(?P<state>(?:\w+\s)+)(?:\s+)?MTU:(?P<mtu>[0-9]+)\s+Metric:(?P<metric>[0-9]+)", re.I)
    re_linux_rx = re.compile(
        r"RX packets:(?P<rx_packets>[0-9]+)\s+errors:(?P<rx_errors>[0-9]+)\s+dropped:"
        r"(?P<rx_dropped>[0-9]+)\s+overruns:(?P<rx_overruns>[0-9]+)\s+frame:(?P<rx_frame>[0-9]+)",
        re.I)
    re_linux_tx = re.compile(
        r"TX packets:(?P<tx_packets>[0-9]+)\s+errors:(?P<tx_errors>[0-9]+)\s+dropped:"
        r"(?P<tx_dropped>[0-9]+)\s+overruns:(?P<tx_overruns>[0-9]+)\s+carrier:(?P<tx_carrier>[0-9]+)",
        re.I)
    re_linux_bytes = re.compile(r"\W+RX bytes:(?P<rx_bytes>\d+)\s+\(.*\)\s+TX bytes:(?P<tx_bytes>\d+)\s+\(.*\)", re.I)
    re_linux_tx_stats = re.compile(r"collisions:(?P<tx_collisions>[0-9]+)\s+txqueuelen:[0-9]+", re.I)

    # OpenBSD syntax
    re_openbsd_interface = re.compile(
        r"(?P<name>[a-zA-Z0-9:._-]+):\s+flags=(?P<flags>[0-9]+)<(?P<state>\S+)?>\s+mtu\s+(?P<mtu>[0-9]+)",
        re.I)
    re_openbsd_ipv4 = re.compile(
        r"inet (?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+netmask\s+"
        r"(?P<mask>(?:[0-9]{1,3}\.){3}[0-9]{1,3})(\s+broadcast\s+"
        r"(?P<broadcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?",
        re.I)
    re_openbsd_ipv6 = re.compile(
        r'inet6\s+(?P<address>\S+)\s+prefixlen\s+(?P<mask>[0-9]+)\s+scopeid\s+(?P<scope>\w+x\w+)<(?P<type>link|host|global)>',
        re.I)
    re_openbsd_details = re.compile(
        r"\S+\s+(?:(?P<mac_addr>[0-9A-Fa-f:?]+)\s+)?txqueuelen\s+[0-9]+\s+\((?P<type>\S+\s?\S+)\)", re.I)
    re_openbsd_rx = re.compile(r"RX packets (?P<rx_packets>[0-9]+)\s+bytes\s+(?P<rx_bytes>\d+)\s+.*", re.I)
    re_openbsd_rx_stats = re.compile(
        r"RX errors (?P<rx_errors>[0-9]+)\s+dropped\s+(?P<rx_dropped>[0-9]+)\s+overruns\s+"
        r"(?P<rx_overruns>[0-9]+)\s+frame\s+(?P<rx_frame>[0-9]+)",
        re.I)
    re_openbsd_tx = re.compile(r"TX packets (?P<tx_packets>[0-9]+)\s+bytes\s+(?P<tx_bytes>\d+)\s+.*", re.I)
    re_openbsd_tx_stats = re.compile(
        r"TX errors (?P<tx_errors>[0-9]+)\s+dropped\s+(?P<tx_dropped>[0-9]+)\s+overruns\s+"
        r"(?P<tx_overruns>[0-9]+)\s+carrier\s+(?P<tx_carrier>[0-9]+)\s+collisions\s+(?P<tx_collisions>[0-9]+)",
        re.I)
    re_openbsd = [re_openbsd_interface, re_openbsd_ipv4, re_openbsd_ipv6, re_openbsd_details, re_openbsd_rx,
                    re_openbsd_rx_stats, re_openbsd_tx, re_openbsd_tx_stats]

    # FreeBSD syntax
    re_freebsd_interface = re.compile(
        r"(?P<name>[a-zA-Z0-9:._-]+):\s+flags=(?P<flags>[0-9]+)<(?P<state>\S+)>\s+metric\s+"
        r"(?P<metric>[0-9]+)\s+mtu\s+(?P<mtu>[0-9]+)",
        re.I)
    re_freebsd_ipv4 = re.compile(
        r"inet (?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+netmask\s+(?P<mask>0x\S+)(\s+broadcast\s+"
        r"(?P<broadcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?",
        re.I)
    re_freebsd_ipv6 = re.compile(r"\s?inet6\s(?P<address>.*)(?:\%\w+\d+)\sprefixlen\s(?P<mask>\d+)(?:\s\w+)?\sscopeid\s(?P<scope>\w+x\w+)", re.I)
    re_freebsd_details = re.compile(r"ether\s+(?P<mac_addr>[0-9A-Fa-f:?]+)", re.I)


    re_linux = [
        re_linux_interface, re_linux_ipv4, re_linux_ipv6, re_linux_state, re_linux_rx, re_linux_tx,
        re_linux_bytes, re_linux_tx_stats
    ]
    re_openbsd = [
        re_openbsd_interface, re_openbsd_ipv4, re_openbsd_ipv6, re_openbsd_details, re_openbsd_rx,
        re_openbsd_rx_stats, re_openbsd_tx, re_openbsd_tx_stats
    ]
    re_freebsd = [re_freebsd_interface, re_freebsd_ipv4, re_freebsd_ipv6, re_freebsd_details]

    interface_patterns = [re_linux_interface, re_openbsd_interface, re_freebsd_interface]
    ipv4_patterns = [re_linux_ipv4, re_openbsd_ipv4, re_freebsd_ipv4]
    ipv6_patterns = [re_linux_ipv6, re_openbsd_ipv6, re_freebsd_ipv6]

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):

            # Find new interface lines
            interface_match = _bundle_match(interface_patterns, line)
            if interface_match:
                if interface_item:
                    if ipv4_info:
                        interface_item['ipv4'] = ipv4_info
                    if ipv6_info:
                        interface_item['ipv6'] = ipv6_info
                    raw_output.append(interface_item)
                    interface_item = {}
                    ipv4_info = []
                    ipv6_info = []

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

            # All other lines
            other_match = _bundle_match(re_linux + re_openbsd + re_freebsd, line)
            if other_match:
                interface_item.update(other_match.groupdict())
                continue

        if interface_item:
            if ipv4_info:
                interface_item['ipv4'] = ipv4_info
            if ipv6_info:
                interface_item['ipv6'] = ipv6_info
            raw_output.append(interface_item)

    return raw_output if raw else _process(raw_output)
