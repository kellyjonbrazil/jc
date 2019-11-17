"""jc - JSON CLI output utility ifconfig Parser

Usage:
    specify --ifconfig as the first argument if the piped input is coming from ifconfig

    no ifconfig options are supported.

Examples:

    $ ifconfig | jc --ifconfig -p
    [
      {
        "name": "ens33",
        "flags": 4163,
        "state": "UP,BROADCAST,RUNNING,MULTICAST",
        "mtu": 1500,
        "ipv4_addr": "192.168.71.138",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": 64,
        "ipv6_scope": "link",
        "mac_addr": "00:0c:29:3b:58:0e",
        "type": "Ethernet",
        "rx_packets": 6374,
        "rx_errors": 0,
        "rx_dropped": 0,
        "rx_overruns": 0,
        "rx_frame": 0,
        "tx_packets": 3707,
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
        "state": "UP,LOOPBACK,RUNNING",
        "mtu": 65536,
        "ipv4_addr": "127.0.0.1",
        "ipv4_mask": "255.0.0.0",
        "ipv4_bcast": null,
        "ipv6_addr": "::1",
        "ipv6_mask": 128,
        "ipv6_scope": "host",
        "mac_addr": null,
        "type": "Local Loopback",
        "rx_packets": 81,
        "rx_errors": 0,
        "rx_dropped": 0,
        "rx_overruns": 0,
        "rx_frame": 0,
        "tx_packets": 81,
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
        "ipv4_addr": "192.168.71.135",
        "ipv4_mask": "255.255.255.0",
        "ipv4_bcast": "192.168.71.255",
        "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
        "ipv6_mask": "64",
        "ipv6_scope": "link",
        "mac_addr": "00:0c:29:3b:58:0e",
        "type": "Ethernet",
        "rx_packets": "26348",
        "rx_errors": "0",
        "rx_dropped": "0",
        "rx_overruns": "0",
        "rx_frame": "0",
        "tx_packets": "5308",
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
        "ipv6_scope": "host",
        "mac_addr": null,
        "type": "Local Loopback",
        "rx_packets": "64",
        "rx_errors": "0",
        "rx_dropped": "0",
        "rx_overruns": "0",
        "rx_frame": "0",
        "tx_packets": "64",
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


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:
    
        [
          {
            "name":             string,
            "flags":            integer,
            "state":            string,
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
            "rx_errors":        integer,
            "rx_dropped":       integer,
            "rx_overruns":      integer,
            "rx_frame":         integer,
            "tx_packets":       integer,
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
        int_list = ['flags', 'mtu', 'ipv6_mask', 'rx_packets', 'rx_errors', 'rx_dropped', 'rx_overruns',
                    'rx_frame', 'tx_packets', 'tx_errors', 'tx_dropped', 'tx_overruns', 'tx_carrier',
                    'tx_collisions', 'metric']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError, TypeError):
                    entry[key] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:
        
        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        dictionary   raw or processed structured data
    """
    
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

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
