"""jc - JSON CLI output utility ifconfig Parser

Usage:

    specify --ifconfig as the first argument if the piped input is coming from ifconfig

    no ifconfig options are supported.

Compatibility:

    'linux', 'aix', 'freebsd', 'darwin'

Examples:

    $ ifconfig | jc --ifconfig -p
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
        "ipv4_addr": "192.168.71.137",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": 64,
        "ipv6_scope": "0x20",
        "mac_addr": "00:0c:29:3b:58:0e",
        "type": "Ethernet",
        "rx_packets": 8061,
        "rx_bytes": 1514413,
        "rx_errors": 0,
        "rx_dropped": 0,
        "rx_overruns": 0,
        "rx_frame": 0,
        "tx_packets": 4502,
        "tx_bytes": 866622,
        "tx_errors": 0,
        "tx_dropped": 0,
        "tx_overruns": 0,
        "tx_carrier": 0,
        "tx_collisions": 0,
        "metric": null
      },
      {
        "name": "lo",
        "flags": 73,
        "state": [
          "UP",
          "LOOPBACK",
          "RUNNING"
        ],
        "mtu": 65536,
        "ipv4_addr": "127.0.0.1",
        "ipv4_mask": "255.0.0.0",
        "ipv4_bcast": null,
        "ipv6_addr": "::1",
        "ipv6_mask": 128,
        "ipv6_scope": "0x10",
        "mac_addr": null,
        "type": "Local Loopback",
        "rx_packets": 73,
        "rx_bytes": 6009,
        "rx_errors": 0,
        "rx_dropped": 0,
        "rx_overruns": 0,
        "rx_frame": 0,
        "tx_packets": 73,
        "tx_bytes": 6009,
        "tx_errors": 0,
        "tx_dropped": 0,
        "tx_overruns": 0,
        "tx_carrier": 0,
        "tx_collisions": 0,
        "metric": null
      }
    ]

    $ ifconfig | jc --ifconfig -p -r
    [
      {
        "name": "ens33",
        "flags": "4163",
        "state": "UP,BROADCAST,RUNNING,MULTICAST",
        "mtu": "1500",
        "ipv4_addr": "192.168.71.137",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": "64",
        "ipv6_scope": "0x20",
        "mac_addr": "00:0c:29:3b:58:0e",
        "type": "Ethernet",
        "rx_packets": "8061",
        "rx_bytes": "1514413",
        "rx_errors": "0",
        "rx_dropped": "0",
        "rx_overruns": "0",
        "rx_frame": "0",
        "tx_packets": "4502",
        "tx_bytes": "866622",
        "tx_errors": "0",
        "tx_dropped": "0",
        "tx_overruns": "0",
        "tx_carrier": "0",
        "tx_collisions": "0",
        "metric": null
      },
      {
        "name": "lo",
        "flags": "73",
        "state": "UP,LOOPBACK,RUNNING",
        "mtu": "65536",
        "ipv4_addr": "127.0.0.1",
        "ipv4_mask": "255.0.0.0",
        "ipv4_bcast": null,
        "ipv6_addr": "::1",
        "ipv6_mask": "128",
        "ipv6_scope": "0x10",
        "mac_addr": null,
        "type": "Local Loopback",
        "rx_packets": "73",
        "rx_bytes": "6009",
        "rx_errors": "0",
        "rx_dropped": "0",
        "rx_overruns": "0",
        "rx_frame": "0",
        "tx_packets": "73",
        "tx_bytes": "6009",
        "tx_errors": "0",
        "tx_dropped": "0",
        "tx_overruns": "0",
        "tx_carrier": "0",
        "tx_collisions": "0",
        "metric": null
      }
    ]
"""
import re
from collections import namedtuple
import jc.utils


class info():
    version = '1.8'
    description = 'ifconfig command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using ifconfig-parser from https://github.com/KnightWhoSayNi/ifconfig-parser'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['ifconfig']


__version__ = info.version


class IfconfigParser(object):
    # Author: threeheadedknight@protonmail.com
    # Date created: 30.06.2018 17:03
    # Python Version: 3.7

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

    attributes = ['name', 'type', 'mac_addr', 'ipv4_addr', 'ipv4_bcast', 'ipv4_mask', 'ipv6_addr', 'ipv6_mask',
                  'ipv6_scope', 'state', 'mtu', 'metric', 'rx_packets', 'rx_errors', 'rx_dropped', 'rx_overruns',
                  'rx_frame', 'tx_packets', 'tx_errors', 'tx_dropped', 'tx_overruns', 'tx_carrier', 'tx_collisions',
                  'rx_bytes', 'tx_bytes']

    def __init__(self, console_output):
        """
        :param console_output:
        """

        if isinstance(console_output, list):
            source_data = " ".join(console_output)
        else:
            source_data = console_output.replace("\n", " ")
        self.interfaces = self.parser(source_data=source_data)

    def list_interfaces(self):
        """
        :return:
        """
        return sorted(self.interfaces.keys())

    def count_interfaces(self):
        """
        :return:
        """
        return len(self.interfaces.keys())

    def filter_interfaces(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        for attr in kwargs.keys():
            if attr not in IfconfigParser.attributes:
                raise ValueError("Attribute [{}] not supported.".format(attr))

        filtered_interfaces = []
        for name, details in self.interfaces.items():

            if all(getattr(details, attr) == kwargs[attr] for attr in kwargs.keys()):
                filtered_interfaces.append(name)

        return sorted(filtered_interfaces)

    def get_interface(self, name):
        """
        :param name:
        :return:
        """
        if name in self.list_interfaces():
            return self.interfaces[name]
        else:
            raise InterfaceNotFound("Interface [{}] not found.".format(name))

    def get_interfaces(self):
        """
        :return:
        """
        return self.interfaces

    def is_available(self, name):
        """
        :param name:
        :return:
        """
        return name in self.interfaces

    def parser(self, source_data):
        """
        :param source_data:
        :return:
        """

        # Linux syntax
        re_linux_interface = re.compile(
            r"(?P<name>[a-zA-Z0-9:._-]+)\s+Link encap:(?P<type>\S+\s?\S+)(\s+HWaddr\s+\b"
            r"(?P<mac_addr>[0-9A-Fa-f:?]+))?",
            re.I)
        re_linux_ipv4 = re.compile(
            r"inet addr:(?P<ipv4_addr>(?:[0-9]{1,3}\.){3}[0-9]{1,3})(\s+Bcast:"
            r"(?P<ipv4_bcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?\s+Mask:(?P<ipv4_mask>(?:[0-9]{1,3}\.){3}[0-9]{1,3})",
            re.I)
        re_linux_ipv6 = re.compile(
            r"inet6 addr:\s+(?P<ipv6_addr>\S+)/(?P<ipv6_mask>[0-9]+)\s+Scope:(?P<ipv6_scope>Link|Host)",
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
        re_linux = [re_linux_interface, re_linux_ipv4, re_linux_ipv6, re_linux_state, re_linux_rx, re_linux_tx,
                    re_linux_bytes, re_linux_tx_stats]

        # OpenBSD syntax
        re_openbsd_interface = re.compile(
            r"(?P<name>[a-zA-Z0-9:._-]+):\s+flags=(?P<flags>[0-9]+)<(?P<state>\S+)?>\s+mtu\s+(?P<mtu>[0-9]+)",
            re.I)
        re_openbsd_ipv4 = re.compile(
            r"inet (?P<ipv4_addr>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+netmask\s+"
            r"(?P<ipv4_mask>(?:[0-9]{1,3}\.){3}[0-9]{1,3})(\s+broadcast\s+"
            r"(?P<ipv4_bcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?",
            re.I)
        re_openbsd_ipv6 = re.compile(
            r"inet6\s+(?P<ipv6_addr>\S+)\s+prefixlen\s+(?P<ipv6_mask>[0-9]+)\s+scopeid\s+(?P<ipv6_scope>\w+x\w+)<"
            r"(?:link|host)>",
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
            r"inet (?P<ipv4_addr>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+netmask\s+(?P<ipv4_mask>0x\S+)(\s+broadcast\s+"
            r"(?P<ipv4_bcast>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?",
            re.I)
        re_freebsd_ipv6 = re.compile(r"\s?inet6\s(?P<ipv6_addr>.*)(?:\%\w+\d+)\sprefixlen\s(?P<ipv6_mask>\d+)(?:\s\w+)?\sscopeid\s(?P<ipv6_scope>\w+x\w+)", re.I)
        re_freebsd_details = re.compile(r"ether\s+(?P<mac_addr>[0-9A-Fa-f:?]+)", re.I)
        re_freebsd = [re_freebsd_interface, re_freebsd_ipv4, re_freebsd_ipv6, re_freebsd_details]

        available_interfaces = dict()

        for pattern in [re_linux_interface, re_openbsd_interface, re_freebsd_interface]:
            network_interfaces = re.finditer(pattern, source_data)
            positions = []
            while True:
                try:
                    pos = next(network_interfaces)
                    positions.append(max(pos.start() - 1, 0))
                except StopIteration:
                    break
            if positions:
                positions.append(len(source_data))
                break

        if not positions:
            return available_interfaces

        for l, r in zip(positions, positions[1:]):
            chunk = source_data[l:r]
            _interface = dict()
            for pattern in re_linux + re_openbsd + re_freebsd:
                match = re.search(pattern, chunk.replace('\t', '\n'))
                if match:
                    details = match.groupdict()
                    for k, v in details.items():
                        if isinstance(v, str): details[k] = v.strip()
                    _interface.update(details)
            if _interface is not None:
                available_interfaces[_interface['name']] = self.update_interface_details(_interface)

        return available_interfaces

    @staticmethod
    def update_interface_details(interface):
        for attr in IfconfigParser.attributes:
            if attr not in interface:
                interface[attr] = None
        return namedtuple('Interface', interface.keys())(**interface)


class InterfaceNotFound(Exception):
    pass


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "name":             string,
            "flags":            integer,
            "state": [
                                string
            ],
            "mtu":              integer,
            "ipv4_addr":        string,
            "ipv4_mask":        string,
            "ipv4_bcast":       string,
            "ipv6_addr":        string,
            "ipv6_mask":        integer,
            "ipv6_scope":       string,
            "mac_addr":         string,
            "type":             string,
            "rx_packets":       integer,
            "rx_bytes":         integer,
            "rx_errors":        integer,
            "rx_dropped":       integer,
            "rx_overruns":      integer,
            "rx_frame":         integer,
            "tx_packets":       integer,
            "tx_bytes":         integer,
            "tx_errors":        integer,
            "tx_dropped":       integer,
            "tx_overruns":      integer,
            "tx_carrier":       integer,
            "tx_collisions":    integer,
            "metric":           integer
          }
        ]
    """
    for entry in proc_data:
        int_list = ['flags', 'mtu', 'ipv6_mask', 'rx_packets', 'rx_bytes', 'rx_errors', 'rx_dropped', 'rx_overruns',
                    'rx_frame', 'tx_packets', 'tx_bytes', 'tx_errors', 'tx_dropped', 'tx_overruns', 'tx_carrier',
                    'tx_collisions', 'metric']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError, TypeError):
                    entry[key] = None

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

        # convert state value to an array
        if 'state' in entry:
            try:
                new_state = entry['state'].split(',')
                entry['state'] = new_state
            except (ValueError, TypeError, AttributeError):
                pass

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        parsed = IfconfigParser(console_output=data)
        interfaces = parsed.get_interfaces()

        # convert ifconfigparser output to a dictionary
        for iface in interfaces:
            d = interfaces[iface]._asdict()
            dct = dict(d)
            raw_output.append(dct)

    if raw:
        return raw_output
    else:
        return process(raw_output)
