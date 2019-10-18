"""jc - JSON CLI output utility ifconfig Parser

Usage:
    specify --ifconfig as the first argument if the piped input is coming from ifconfig

    no ifconfig options are supported.

Example:

$ ifconfig | jc --ifconfig -p

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
