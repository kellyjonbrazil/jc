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
import jc.utils
from ifconfigparser import IfconfigParser


class info():
    version = '1.5'
    description = 'ifconfig command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['ifconfig']


__version__ = info.version


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
                if entry['ipv4_mask'].find('0x') == 0:
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
