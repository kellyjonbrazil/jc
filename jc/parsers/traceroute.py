"""jc - JSON CLI output utility `traceroute` command output parser

Supports `traceroute` and `traceroute6` output.

Note: On some operating systems you will need to redirect `STDERR` to `STDOUT` for destination info since the header line is sent to `STDERR`. A warning message will be printed to `STDERR` if the header row is not found.

e.g. `$ traceroute 8.8.8.8 2>&1 | jc --traceroute`

Usage (cli):

    $ traceroute 1.2.3.4 | jc --traceroute

    or

    $ jc traceroute 1.2.3.4

Usage (module):

    import jc.parsers.traceroute
    result = jc.parsers.traceroute.parse(traceroute_command_output)

Schema:

    {
      "destination_ip":         string,
      "destination_name":       string,
      "hops": [
        {
          "hop":                integer,
          "probes": [
            {
              "annotation":     string,
              "asn":            integer,
              "ip":             string,
              "name":           string,
              "rtt":            float
            }
          ]
        }
      ]
    }

Examples:

    $ traceroute google.com | jc --traceroute -p
    {
      "destination_ip": "216.58.194.46",
      "destination_name": "google.com",
      "hops": [
        {
          "hop": 1,
          "probes": [
            {
              "annotation": null,
              "asn": null,
              "ip": "216.230.231.141",
              "name": "216-230-231-141.static.houston.tx.oplink.net",
              "rtt": 198.574
            },
            {
              "annotation": null,
              "asn": null,
              "ip": "216.230.231.141",
              "name": "216-230-231-141.static.houston.tx.oplink.net",
              "rtt": null
            },
            {
              "annotation": null,
              "asn": null,
              "ip": "216.230.231.141",
              "name": "216-230-231-141.static.houston.tx.oplink.net",
              "rtt": 198.65
            }
          ]
        },
        ...
      ]
    }

    $ traceroute google.com  | jc --traceroute -p -r
    {
      "destination_ip": "216.58.194.46",
      "destination_name": "google.com",
      "hops": [
        {
          "hop": "1",
          "probes": [
            {
              "annotation": null,
              "asn": null,
              "ip": "216.230.231.141",
              "name": "216-230-231-141.static.houston.tx.oplink.net",
              "rtt": "198.574"
            },
            {
              "annotation": null,
              "asn": null,
              "ip": "216.230.231.141",
              "name": "216-230-231-141.static.houston.tx.oplink.net",
              "rtt": null
            },
            {
              "annotation": null,
              "asn": null,
              "ip": "216.230.231.141",
              "name": "216-230-231-141.static.houston.tx.oplink.net",
              "rtt": "198.650"
            }
          ]
        },
        ...
      ]
    }
"""
import re
from decimal import Decimal
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`traceroute` and `traceroute6` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the trparse library by Luis Benitez at https://github.com/lbenitez000/trparse'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['traceroute', 'traceroute6']


__version__ = info.version


'''
Copyright (C) 2015 Luis Benitez

Parses the output of a traceroute execution into an AST (Abstract Syntax Tree).

The MIT License (MIT)

Copyright (c) 2014 Luis Benitez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

RE_HEADER = re.compile(r'(\S+)\s+\((\d+\.\d+\.\d+\.\d+|[0-9a-fA-F:]+)\)')
RE_PROBE_NAME_IP = re.compile(r'(\S+)\s+\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[0-9a-fA-F:]+)\)+')
RE_PROBE_BSD_IPV6 = re.compile(r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b')
RE_HOP = re.compile(r'^\s*(\d+)?\s+(.+)$')
RE_PROBE_ASN = re.compile(r'\[AS(\d+)\]')
RE_PROBE_RTT_ANNOTATION = re.compile(r'(?:(\d+(?:\.?\d+)?)\s+ms|(\s+\*\s+))\s*(!\S*)?')


class _Traceroute(object):
    def __init__(self, dest_name, dest_ip):
        self.dest_name = dest_name
        self.dest_ip = dest_ip
        self.hops = []

    def add_hop(self, hop):
        self.hops.append(hop)

    def __str__(self):
        text = "Traceroute for %s (%s)\n\n" % (self.dest_name, self.dest_ip)
        for hop in self.hops:
            text += str(hop)
        return text


class _Hop(object):
    def __init__(self, idx):
        self.idx = idx  # Hop count, starting at 1 (usually)
        self.probes = []  # Series of Probe instances

    def add_probe(self, probe):
        """Adds a Probe instance to this hop's results."""
        if self.probes:
            probe_last = self.probes[-1]
            if not probe.ip:
                probe.ip = probe_last.ip
                probe.name = probe_last.name
        self.probes.append(probe)

    def __str__(self):
        text = "{:>3d} ".format(self.idx)
        text_len = len(text)
        for n, probe in enumerate(self.probes):
            text_probe = str(probe)
            if n:
                text += (text_len * " ") + text_probe
            else:
                text += text_probe
        text += "\n"
        return text


class _Probe(object):
    def __init__(self, name=None, ip=None, asn=None, rtt=None, annotation=None):
        self.name = name
        self.ip = ip
        self.asn = asn  # Autonomous System number
        self.rtt = rtt  # RTT in ms
        self.annotation = annotation  # Annotation, such as !H, !N, !X, etc

    def __str__(self):
        text = ""
        if self.asn is not None:
            text += "[AS{:d}] ".format(self.asn)
        if self.rtt:
            text += "{:s} ({:s}) {:1.3f} ms".format(self.name, self.ip, self.rtt)
        else:
            text = "*"
        if self.annotation:
            text += " {:s}".format(self.annotation)
        text += "\n"
        return text


def _loads(data):
    lines = data.splitlines()

    # Get headers
    match_dest = RE_HEADER.search(lines[0])
    dest_name, dest_ip = None, None
    if match_dest:
        dest_name = match_dest.group(1)
        dest_ip = match_dest.group(2)

    # The Traceroute node is the root of the tree
    traceroute = _Traceroute(dest_name, dest_ip)

    # Parse the remaining lines, they should be only hops/probes
    for line in lines[1:]:
        # Skip empty lines
        if not line:
            continue

        hop_match = RE_HOP.match(line)

        if hop_match.group(1):
            hop_index = int(hop_match.group(1))
        else:
            hop_index = None

        if hop_index is not None:
            hop = _Hop(hop_index)
            traceroute.add_hop(hop)

        hop_string = hop_match.group(2)

        probe_asn_match = RE_PROBE_ASN.search(hop_string)
        if probe_asn_match:
            probe_asn = int(probe_asn_match.group(1))
        else:
            probe_asn = None

        probe_name_ip_match = RE_PROBE_NAME_IP.search(hop_string)
        probe_bsd_ipv6_match = RE_PROBE_BSD_IPV6.search(hop_string)
        if probe_name_ip_match:
            probe_name = probe_name_ip_match.group(1)
            probe_ip = probe_name_ip_match.group(2)
        elif probe_bsd_ipv6_match:
            probe_name = None
            probe_ip = probe_bsd_ipv6_match.group(0)
        else:
            probe_name = None
            probe_ip = None

        probe_rtt_annotations = RE_PROBE_RTT_ANNOTATION.findall(hop_string)

        for probe_rtt_annotation in probe_rtt_annotations:
            if probe_rtt_annotation[0]:
                probe_rtt = Decimal(probe_rtt_annotation[0])
            elif probe_rtt_annotation[1]:
                probe_rtt = None
            else:
                message = f"Expected probe RTT or *. Got: '{probe_rtt_annotation[0]}'"
                raise ParseError(message)

            probe_annotation = probe_rtt_annotation[2] or None

            probe = _Probe(
                name=probe_name,
                ip=probe_ip,
                asn=probe_asn,
                rtt=probe_rtt,
                annotation=probe_annotation
            )

            # only add probe if there is data
            if any([probe_name, probe_ip, probe_asn, probe_rtt, probe_annotation]):
                hop.add_probe(probe)

    return traceroute


class ParseError(Exception):
    pass


########################################################################################

def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list = ['hop', 'asn']
    float_list = ['rtt']

    if 'hops' in proc_data:
        for entry in proc_data['hops']:
            for key in entry:
                if key in int_list:
                    entry[key] = jc.utils.convert_to_int(entry[key])

                if key in float_list:
                    entry[key] = jc.utils.convert_to_float(entry[key])

            if 'probes' in entry:
                for item in entry['probes']:
                    for key in item:
                        if key in int_list:
                            item[key] = jc.utils.convert_to_int(item[key])

                        if key in float_list:
                            item[key] = jc.utils.convert_to_float(item[key])

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):

        # remove any warning lines
        new_data = []
        for data_line in data.splitlines():
            if 'traceroute: Warning: ' not in data_line and 'traceroute6: Warning: ' not in data_line:
                new_data.append(data_line)
            else:
                continue

        # check if header row exists, otherwise add a dummy header
        if not new_data[0].startswith('traceroute to ') and not new_data[0].startswith('traceroute6 to '):
            new_data[:0] = ['traceroute to <<_>>  (<<_>>), 30 hops max, 60 byte packets']

            # print warning to STDERR
            if not quiet:
                jc.utils.warning_message('No header row found. For destination info redirect STDERR to STDOUT')

        data = '\n'.join(new_data)

        tr = _loads(data)
        hops = tr.hops
        hops_list = []

        if hops:
            for hop in hops:
                hop_obj = {}
                hop_obj['hop'] = str(hop.idx)
                probe_list = []

                if hop.probes:
                    for probe in hop.probes:
                        probe_obj = {
                            'annotation': probe.annotation,
                            'asn': None if probe.asn is None else str(probe.asn),
                            'ip': probe.ip,
                            'name': probe.name,
                            'rtt': None if probe.rtt is None else str(probe.rtt)
                        }
                        probe_list.append(probe_obj)

                hop_obj['probes'] = probe_list
                hops_list.append(hop_obj)

        raw_output = {
            'destination_ip': tr.dest_ip,
            'destination_name': tr.dest_name,
            'hops': hops_list
        }

    if raw:
        return raw_output
    else:
        return _process(raw_output)
