"""jc - JSON CLI output utility `ping` command output streaming parser

> This streaming parser outputs JSON Lines

Supports `ping` and `ping6` output.

Usage (cli):

    $ ping | jc --ping-s

> Note: When piping `jc` converted `ping` output to other processes it may appear the output is hanging due to the OS pipe buffers. This is because `ping` output is too small to quickly fill up the buffer. Use the `-u` option to unbuffer the `jc` output if you would like immediate output. See the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output) for more information.

Usage (module):

    import jc.parsers.ping_s
    result = jc.parsers.ping_s.parse(ping_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "type":                        string,        # 'reply', 'timeout', 'summary', etc. See `_error_type.type_map` for all options.
      "source_ip":                   string,
      "destination_ip":              string,
      "sent_bytes":                  integer,
      "pattern":                     string,        # (null if not set)
      "destination":                 string,
      "timestamp":                   float,
      "response_bytes":              integer,
      "response_ip":                 string,
      "icmp_seq":                    integer,
      "ttl":                         integer,
      "time_ms":                     float,
      "duplicate":                   boolean,
      "packets_transmitted":         integer,
      "packets_received":            integer,
      "packet_loss_percent":         float,
      "duplicates":                  integer,
      "round_trip_ms_min":           float,
      "round_trip_ms_avg":           float,
      "round_trip_ms_max":           float,
      "round_trip_ms_stddev":        float,
      "_jc_meta":                                  # This object only exists if using -qq or ignore_exceptions=True
        {
          "success":                 boolean,      # true if successfully parsed, false if error
          "error":                   string,       # exists if "success" is false
          "line":                    string        # exists if "success" is false
        }
    }

Examples:

    $ ping 1.1.1.1 | jc --ping-s
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"pattern":null,"response_bytes":64,"response_ip":"1.1.1.1","icmp_seq":0,"ttl":56,"time_ms":23.703}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"pattern":null,"response_bytes":64,"response_ip":"1.1.1.1","icmp_seq":1,"ttl":56,"time_ms":22.862}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"pattern":null,"response_bytes":64,"response_ip":"1.1.1.1","icmp_seq":2,"ttl":56,"time_ms":22.82}
    ...

    $ ping 1.1.1.1 | jc --ping-s -r
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","pattern":null,"response_bytes":"64","response_ip":"1.1.1.1","icmp_seq":"0","ttl":"56","time_ms":"23.054"}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","pattern":null,"response_bytes":"64","response_ip":"1.1.1.1","icmp_seq":"1","ttl":"56","time_ms":"24.739"}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","pattern":null,"response_bytes":"64","response_ip":"1.1.1.1","icmp_seq":"2","ttl":"56","time_ms":"23.232"}
    ...
"""
import string
import ipaddress
import jc.utils
from jc.exceptions import ParseError
from jc.utils import stream_success, stream_error


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '0.6'
    description = '`ping` and `ping6` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    streaming = True


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = ['sent_bytes', 'packets_transmitted', 'packets_received', 'response_bytes', 'icmp_seq', 'ttl',
                'duplicates', 'vr', 'hl', 'tos', 'len', 'id', 'flg', 'off', 'pro', 'cks']
    float_list = ['packet_loss_percent', 'round_trip_ms_min', 'round_trip_ms_avg', 'round_trip_ms_max',
                  'round_trip_ms_stddev', 'timestamp', 'time_ms']

    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

        if key in float_list:
            proc_data[key] = jc.utils.convert_to_float(proc_data[key])

    return proc_data


class _state:
    os_detected = None
    linux = None
    bsd = None
    ipv4 = None
    hostname = None
    destination_ip = None
    sent_bytes = None
    pattern = None
    footer = False
    packets_transmitted = None
    packets_received = None
    packet_loss_percent = None
    time_ms = None
    duplicates = None


def _ipv6_in(line):
    line_list = line.replace('(', ' ').replace(')', ' ').replace(',', ' ').replace('%', ' ').split()
    ipv6 = False
    for item in line_list:
        try:
            _ = ipaddress.IPv6Address(item)
            ipv6 = True
        except Exception:
            pass
    return ipv6


def _error_type(line):
    # from https://github.com/dgibson/iputils/blob/master/ping.c
    # https://android.googlesource.com/platform/external/ping/+/8fc3c91cf9e7f87bc20b9e6d3ea2982d87b70d9a/ping.c
    # https://opensource.apple.com/source/network_cmds/network_cmds-328/ping.tproj/ping.c
    type_map = {
        'Destination Net Unreachable': 'destination_net_unreachable',
        'Destination Host Unreachable': 'destination_host_unreachable',
        'Destination Protocol Unreachable': 'destination_protocol_unreachable',
        'Destination Port Unreachable': 'destination_port_unreachable',
        'Frag needed and DF set': 'frag_needed_and_df_set',
        'Source Route Failed': 'source_route_failed',
        'Destination Net Unknown': 'destination_net_unknown',
        'Destination Host Unknown': 'destination_host_unknown',
        'Source Host Isolated': 'source_host_isolated',
        'Destination Net Prohibited': 'destination_net_prohibited',
        'Destination Host Prohibited': 'destination_host_prohibited',
        'Destination Net Unreachable for Type of Service': 'destination_net_unreachable_for_type_of_service',
        'Destination Host Unreachable for Type of Service': 'destination_host_unreachable_for_type_of_service',
        'Packet filtered': 'packet_filtered',
        'Precedence Violation': 'precedence_violation',
        'Precedence Cutoff': 'precedence_cutoff',
        'Dest Unreachable, Bad Code': 'dest_unreachable_bad_code',
        'Redirect Network': 'redirect_network',
        'Redirect Host': 'redirect_host',
        'Redirect Type of Service and Network': 'redirect_type_of_service_and_network',
        'Redirect, Bad Code': 'redirect_bad_code',
        'Time to live exceeded': 'time_to_live_exceeded',
        'Frag reassembly time exceeded': 'frag_reassembly_time_exceeded',
        'Time exceeded, Bad Code': 'time_exceeded_bad_code'
    }

    for err_type, code in type_map.items():
        if err_type in line:
            return code

    return None


def _bsd_parse(line, s):
    output_line = {}

    if line.startswith('PING '):
        s.destination_ip = line.split()[2].lstrip('(').rstrip(':').rstrip(')')
        s.sent_bytes = line.split()[3]
        return None

    if line.startswith('PING6('):
        line = line.replace('(', ' ').replace(')', ' ').replace('=', ' ')
        s.source_ip = line.split()[4]
        s.destination_ip = line.split()[6]
        s.sent_bytes = line.split()[1]
        return None

    if line.startswith('---'):
        s.footer = True
        return None

    if s.footer:
        if 'packets transmitted' in line:
            if ' duplicates,' in line:
                s.packets_transmitted = line.split()[0]
                s.packets_received = line.split()[3]
                s.packet_loss_percent = line.split()[8].rstrip('%')
                s.duplicates = line.split()[6].lstrip('+')
                return None

            s.packets_transmitted = line.split()[0]
            s.packets_received = line.split()[3]
            s.packet_loss_percent = line.split()[6].rstrip('%')
            s.duplicates = '0'
            return None

        split_line = line.split(' = ')[1]
        split_line = split_line.split('/')

        output_line = {
            'type': 'summary',
            'destination_ip': s.destination_ip or None,
            'sent_bytes': s.sent_bytes or None,
            'pattern': s.pattern or None,
            'packets_transmitted': s.packets_transmitted or None,
            'packets_received': s.packets_received or None,
            'packet_loss_percent': s.packet_loss_percent or None,
            'duplicates': s.duplicates or None,
            'round_trip_ms_min': split_line[0],
            'round_trip_ms_avg': split_line[1],
            'round_trip_ms_max': split_line[2],
            'round_trip_ms_stddev': split_line[3].replace(' ms', '')
        }

        return output_line

    # ping response lines

    # ipv4 lines
    if not _ipv6_in(line):

        # request timeout
        if line.startswith('Request timeout for '):
            output_line = {
                'type': 'timeout',
                'destination_ip': s.destination_ip or None,
                'sent_bytes': s.sent_bytes or None,
                'pattern': s.pattern or None,
                'icmp_seq': line.split()[4]
            }

            return output_line

        # catch error responses
        err = _error_type(line)
        if err:
            output_line = {
                'type': err
            }

            try:
                output_line['bytes'] = line.split()[0]
                output_line['destination_ip'] = s.destination_ip
                output_line['response_ip'] = line.split()[4].strip(':').strip('(').strip(')')
            except Exception:
                pass

            return output_line

        # normal response
        if ' bytes from ' in line:
            line = line.replace(':', ' ').replace('=', ' ')

            output_line = {
                'type': 'reply',
                'destination_ip': s.destination_ip or None,
                'sent_bytes': s.sent_bytes or None,
                'pattern': s.pattern or None,
                'response_bytes': line.split()[0],
                'response_ip': line.split()[3],
                'icmp_seq': line.split()[5],
                'ttl': line.split()[7],
                'time_ms': line.split()[9]
            }

            return output_line

    # ipv6 lines
    elif ' bytes from ' in line:
        line = line.replace(',', ' ').replace('=', ' ')

        output_line = {
            'type': 'reply',
            'destination_ip': s.destination_ip or None,
            'sent_bytes': s.sent_bytes or None,
            'pattern': s.pattern or None,
            'bytes': line.split()[0],
            'response_ip': line.split()[3],
            'icmp_seq': line.split()[5],
            'ttl': line.split()[7],
            'time_ms': line.split()[9]
        }

        return output_line


def _linux_parse(line, s):
    """
    Linux ping line parsing function.

    Parameters:

        line:        (string)        line of text data to parse
        s:           (state object)  global state

    Returns:

        Dictionary. Raw structured data.
    """
    output_line = {}

    if line.startswith('PING '):
        s.ipv4 = 'bytes of data' in line

        if s.ipv4 and line[5] not in string.digits:
            s.hostname = True
        elif s.ipv4 and line[5] in string.digits:
            s.hostname = False
        elif not s.ipv4 and ' (' in line:
            s.hostname = True
        else:
            s.hostname = False

        if s.ipv4 and not s.hostname:
            dst_ip, dta_byts = (2, 3)
        elif s.ipv4 and s.hostname:
            dst_ip, dta_byts = (2, 3)
        elif not s.ipv4 and not s.hostname:
            dst_ip, dta_byts = (2, 3)
        else:
            dst_ip, dta_byts = (3, 4)

        line = line.replace('(', ' ').replace(')', ' ')
        s.destination_ip = line.split()[dst_ip].lstrip('(').rstrip(')')
        s.sent_bytes = line.split()[dta_byts]

        return None

    if line.startswith('---'):
        s.footer = True
        return None

    if s.footer:
        if 'packets transmitted' in line:
            if ' duplicates,' in line:
                s.packets_transmitted = line.split()[0]
                s.packets_received = line.split()[3]
                s.packet_loss_percent = line.split()[7].rstrip('%')
                s.duplicates = line.split()[5].lstrip('+')
                s.time_ms = line.split()[11].replace('ms', '')
                return None

            s.packets_transmitted = line.split()[0]
            s.packets_received = line.split()[3]
            s.packet_loss_percent = line.split()[5].rstrip('%')
            s.duplicates = '0'
            s.time_ms = line.split()[9].replace('ms', '')
            return None

        split_line = line.split(' = ')[1]
        split_line = split_line.split('/')
        output_line = {
            'type': 'summary',
            'destination_ip': s.destination_ip or None,
            'sent_bytes': s.sent_bytes or None,
            'pattern': s.pattern or None,
            'packets_transmitted': s.packets_transmitted or None,
            'packets_received': s.packets_received or None,
            'packet_loss_percent': s.packet_loss_percent or None,
            'duplicates': s.duplicates or None,
            'time_ms': s.time_ms or None,
            'round_trip_ms_min': split_line[0],
            'round_trip_ms_avg': split_line[1],
            'round_trip_ms_max': split_line[2],
            'round_trip_ms_stddev': split_line[3].split()[0]
        }

        return output_line

    # ping response lines

    # request timeout
    if 'no answer yet for icmp_seq=' in line:
        timestamp = False
        isequence = 5

        # if timestamp option is specified, then shift icmp sequence field right by one
        if line[0] == '[':
            timestamp = True
            isequence = 6

        output_line = {
            'type': 'timeout',
            'destination_ip': s.destination_ip or None,
            'sent_bytes': s.sent_bytes or None,
            'pattern': s.pattern or None,
            'timestamp': line.split()[0].lstrip('[').rstrip(']') if timestamp else None,
            'icmp_seq': line.replace('=', ' ').split()[isequence]
        }

        return output_line

    # normal responses
    if ' bytes from ' in line:

        line = line.replace('(', ' ').replace(')', ' ').replace('=', ' ')

        # positions of items depend on whether ipv4/ipv6 and/or ip/hostname is used
        if s.ipv4 and not s.hostname:
            bts, rip, iseq, t2l, tms = (0, 3, 5, 7, 9)
        elif s.ipv4 and s.hostname:
            bts, rip, iseq, t2l, tms = (0, 4, 7, 9, 11)
        elif not s.ipv4 and not s.hostname:
            bts, rip, iseq, t2l, tms = (0, 3, 5, 7, 9)
        elif not s.ipv4 and s.hostname:
            bts, rip, iseq, t2l, tms = (0, 4, 7, 9, 11)

        # if timestamp option is specified, then shift everything right by one
        timestamp = False
        if line[0] == '[':
            timestamp = True
            bts, rip, iseq, t2l, tms = (bts + 1, rip + 1, iseq + 1, t2l + 1, tms + 1)

        output_line = {
            'type': 'reply',
            'destination_ip': s.destination_ip or None,
            'sent_bytes': s.sent_bytes or None,
            'pattern': s.pattern or None,
            'timestamp': line.split()[0].lstrip('[').rstrip(']') if timestamp else None,
            'response_bytes': line.split()[bts],
            'response_ip': line.split()[rip].rstrip(':'),
            'icmp_seq': line.split()[iseq],
            'ttl': line.split()[t2l],
            'time_ms': line.split()[tms],
            'duplicate': 'DUP!' in line
        }

        return output_line


def parse(data, raw=False, quiet=False, ignore_exceptions=False):
    """
    Main text parsing generator function. Returns an iterator object.

    Parameters:

        data:              (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
        raw:               (boolean)   output preprocessed JSON if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Yields:

        Dictionary. Raw or processed structured data.

    Returns:

        Iterator object
    """
    s = _state()

    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.streaming_input_type_check(data)

    for line in data:
        output_line = {}
        try:
            jc.utils.streaming_line_input_type_check(line)

            # skip blank lines
            if line.strip() == '':
                continue

            # skip warning lines
            if line.startswith('WARNING: '):
                continue

            # check for PATTERN
            if line.startswith('PATTERN: '):
                s.pattern = line.strip().split(': ')[1]
                continue

            # detect Linux vs. BSD ping
            if not s.os_detected and line.strip().endswith('bytes of data.'):
                s.os_detected = True
                s.linux = True

            elif not s.os_detected and '-->' in line:
                s.os_detected = True
                s.bsd = True

            elif not s.os_detected and _ipv6_in(line) and line.strip().endswith('data bytes'):
                s.os_detected = True
                s.linux = True

            elif not s.os_detected and not _ipv6_in(line) and line.strip().endswith('data bytes'):
                s.os_detected = True
                s.bsd = True

            # parse the data
            if s.os_detected and s.linux:
                output_line = _linux_parse(line, s)

            elif s.os_detected and s.bsd:
                output_line = _bsd_parse(line, s)

            else:
                raise ParseError('Could not detect ping OS')

            # yield the output line if it has data
            if output_line:
                yield stream_success(output_line, ignore_exceptions) if raw else stream_success(_process(output_line), ignore_exceptions)
            else:
                continue

        except Exception as e:
            yield stream_error(e, ignore_exceptions, line)
