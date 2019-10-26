"""jc - JSON CLI output utility ifconfig Parser

Usage:
    specify --ifconfig as the first argument if the piped input is coming from ifconfig

    no ifconfig options are supported.

Example:

$ ifconfig | jc --ifconfig -p
[
  {
    "name": "docker0",
    "flags": "4099",
    "state": "UP,BROADCAST,MULTICAST",
    "mtu": "1500",
    "ipv4_addr": "172.17.0.1",
    "ipv4_mask": "255.255.0.0",
    "ipv4_bcast": "0.0.0.0",
    "mac_addr": "02:42:53:18:31:cc",
    "type": "Ethernet",
    "rx_packets": "0",
    "rx_errors": "0",
    "rx_dropped": "0",
    "rx_overruns": "0",
    "rx_frame": "0",
    "tx_packets": "0",
    "tx_errors": "0",
    "tx_dropped": "0",
    "tx_overruns": "0",
    "tx_carrier": "0",
    "tx_collisions": "0",
    "ipv6_addr": null,
    "ipv6_mask": null,
    "ipv6_scope": null,
    "metric": null
  },
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
from collections import namedtuple
from ifconfigparser import IfconfigParser


def parse(data):
    output = []

    parsed = IfconfigParser(console_output=data)
    interfaces = parsed.get_interfaces()

    # convert ifconfigparser output to a dictionary
    for iface in interfaces:
        d = interfaces[iface]._asdict()
        dct = dict(d)
        output.append(dct)

    return output
