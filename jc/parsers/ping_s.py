"""jc - JSON CLI output utility `ping` command output streaming parser

Usage (cli):

    $ ping | jc --ping_s

Usage (module):

    import jc.parsers.ping_s
    result = jc.parsers.ping_s.parse(ping_command_output)    # result is an iterable object
    for item in result:
        # do something

> Note: When piping `jc` output to other processes it may appear the output is hanging due to the OS pipe buffers. This is because `ping` output is too small to quickly fill up the buffer. Use the `-u` option to unbuffer the `jc` output if you would like immediate output. See the [readme](https://github.com/kellyjonbrazil/jc/tree/streaming#streaming-parsers) for more information.

Schema:

    {
      "type":                        string,        # 'reply', 'timeout', 'summary'
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
      "_meta":                                     # This object only exists if using -q or quiet=True
        {
          "success":                 booean,       # true if successfully parsed, false if error
          "error":                   string,       # exists if "success" is false
          "line":                    string        # exists if "success" is false
        }
    }

Examples:

    $ ping | jc --ping-s
    {example output}
    ...

    $ ping | jc --ping-s -r
    {example output}
    ...
"""
import string
import jc.utils
from jc.utils import stream_success, stream_error


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '0.5'
    description = '`ping` and `ping6` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
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


def parse(data, raw=False, quiet=False):
    """
    Main text parsing generator function. Produces an iterable object.

    Parameters:

        data:        (string)  line-based text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages and ignore parsing errors if True

    Yields:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    destination_ip = None
    sent_bytes = None
    pattern = None
    footer = False
    packets_transmitted = None
    packets_received = None
    packet_loss_percent = None
    time_ms = None
    duplicates = None

    for line in data:
        try:
            output_line = {}

            # check for PATTERN
            if line.startswith('PATTERN: '):
                pattern = line.strip().split(': ')[1]
                continue

            if line.startswith('PING '):
                ipv4 = True if 'bytes of data' in line else False

                if ipv4 and line[5] not in string.digits:
                    hostname = True
                elif ipv4 and line[5] in string.digits:
                    hostname = False
                elif not ipv4 and ' (' in line:
                    hostname = True
                else:
                    hostname = False

                if ipv4 and not hostname:
                    dst_ip, dta_byts = (2, 3)
                elif ipv4 and hostname:
                    dst_ip, dta_byts = (2, 3)
                elif not ipv4 and not hostname:
                    dst_ip, dta_byts = (2, 3)
                else:
                    dst_ip, dta_byts = (3, 4)

                line = line.replace('(', ' ').replace(')', ' ')
                destination_ip = line.split()[dst_ip].lstrip('(').rstrip(')')
                sent_bytes = line.split()[dta_byts]

                continue

            if line.startswith('---'):
                footer = True
                continue

            if footer:
                if 'packets transmitted' in line:
                    if ' duplicates,' in line:
                        packets_transmitted = line.split()[0]
                        packets_received = line.split()[3]
                        packet_loss_percent = line.split()[7].rstrip('%')
                        duplicates = line.split()[5].lstrip('+')
                        time_ms = line.split()[11].replace('ms', '')

                        continue

                    else:
                        packets_transmitted = line.split()[0]
                        packets_received = line.split()[3]
                        packet_loss_percent = line.split()[5].rstrip('%')
                        duplicates = '0'
                        time_ms = line.split()[9].replace('ms', '')
                        
                        continue

                else:
                    split_line = line.split(' = ')[1]
                    split_line = split_line.split('/')
                    output_line = {
                        'type': 'summary',
                        'destination_ip': destination_ip or None,
                        'sent_bytes': sent_bytes or None,
                        'pattern': pattern or None,
                        'packets_transmitted': packets_transmitted or None,
                        'packets_received': packets_received or None,
                        'packet_loss_percent': packet_loss_percent or None,
                        'duplicates': duplicates or None,
                        'time_ms': time_ms or None,
                        'round_trip_ms_min': split_line[0],
                        'round_trip_ms_avg': split_line[1],
                        'round_trip_ms_max': split_line[2],
                        'round_trip_ms_stddev': split_line[3].split()[0]
                    }

                    yield stream_success(output_line, quiet) if raw else stream_success(_process(output_line), quiet)
                    continue

            # ping response lines
            else:
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
                        'destination_ip': destination_ip or None,
                        'sent_bytes': sent_bytes or None,
                        'pattern': pattern or None,
                        'timestamp': line.split()[0].lstrip('[').rstrip(']') if timestamp else None,
                        'icmp_seq': line.replace('=', ' ').split()[isequence]
                    }
                                        
                    yield stream_success(output_line, quiet) if raw else stream_success(_process(output_line), quiet)
                    continue

                # normal responses
                elif ' bytes from ' in line:
                    
                    line = line.replace('(', ' ').replace(')', ' ').replace('=', ' ')

                    # positions of items depend on whether ipv4/ipv6 and/or ip/hostname is used
                    if ipv4 and not hostname:
                        bts, rip, iseq, t2l, tms = (0, 3, 5, 7, 9)
                    elif ipv4 and hostname:
                        bts, rip, iseq, t2l, tms = (0, 4, 7, 9, 11)
                    elif not ipv4 and not hostname:
                        bts, rip, iseq, t2l, tms = (0, 3, 5, 7, 9)
                    elif not ipv4 and hostname:
                        bts, rip, iseq, t2l, tms = (0, 4, 7, 9, 11)

                    # if timestamp option is specified, then shift everything right by one
                    timestamp = False
                    if line[0] == '[':
                        timestamp = True
                        bts, rip, iseq, t2l, tms = (bts + 1, rip + 1, iseq + 1, t2l + 1, tms + 1)

                    output_line = {
                        'type': 'reply',
                        'destination_ip': destination_ip or None,
                        'sent_bytes': sent_bytes or None,
                        'pattern': pattern or None,
                        'timestamp': line.split()[0].lstrip('[').rstrip(']') if timestamp else None,
                        'response_bytes': line.split()[bts],
                        'response_ip': line.split()[rip].rstrip(':'),
                        'icmp_seq': line.split()[iseq],
                        'ttl': line.split()[t2l],
                        'time_ms': line.split()[tms],
                        'duplicate': True if 'DUP!' in line else False
                    }

                    yield stream_success(output_line, quiet) if raw else stream_success(_process(output_line), quiet)
            
        except Exception as e:
            yield stream_error(e, quiet, line)
