"""jc - JSON CLI output utility ping Parser

Usage:

    specify --ping as the first argument if the piped input is coming from ping

Compatibility:

    'linux', 'darwin', 'cygwin', 'freebsd'

Examples:

    $ ping | jc --ping -p
    []

    $ ping | jc --ping -p -r
    []
"""
import string
import jc.utils


class info():
    version = '1.0'
    description = 'ping command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'freebsd']
    magic_commands = ['ping', 'ping6']


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
            "ping":     string,
            "bar":     boolean,
            "baz":     integer
          }
        ]
    """

    # rebuild output for added semantic information
    return proc_data


def linux_parse(data):
    raw_output = {}
    ping_responses = []
    pattern = None
    footer = False

    linedata = data.splitlines()

    # check for PATTERN
    if linedata[0].startswith('PATTERN: '):
        pattern = linedata.pop(0).split(': ')[1]

    ipv4 = True if 'bytes of data' in linedata[0] else False

    if ipv4 and linedata[0][5] not in string.digits:
        hostname = True
    elif ipv4 and linedata[0][5] in string.digits:
        hostname = False
    elif not ipv4 and ' (' in linedata[0]:
        hostname = True
    else:
        hostname = False

    for line in filter(None, linedata):
        if line.startswith('PING '):
            if ipv4 and not hostname:
                dst_ip, dta_byts = (2, 3)
            elif ipv4 and hostname:
                dst_ip, dta_byts = (2, 3)
            elif not ipv4 and not hostname:
                dst_ip, dta_byts = (2, 3)
            else:
                dst_ip, dta_byts = (3, 4)

            line = line.replace('(', ' ').replace(')', ' ')
            raw_output.update(
                {
                    'destination_ip': line.split()[dst_ip].lstrip('(').rstrip(')'),
                    'data_bytes': line.split()[dta_byts],
                    'pattern': pattern
                }
            )
            continue

        if line.startswith('---'):
            footer = True
            raw_output['destination'] = line.split()[1]
            continue

        if footer:
            if 'packets transmitted' in line:
                raw_output.update(
                    {
                        'packets_transmitted': line.split()[0],
                        'packets_received': line.split()[3],
                        'packet_loss_percent': line.split()[5].rstrip('%'),
                        'time_ms': line.split()[9].replace('ms', '')
                    }
                )
                continue

            else:
                split_line = line.split(' = ')[1]
                split_line = split_line.split('/')
                raw_output.update(
                    {
                        'round_trip_ms_min': split_line[0],
                        'round_trip_ms_avg': split_line[1],
                        'round_trip_ms_max': split_line[2],
                        'round_trip_ms_stddev': split_line[3].replace(' ms', '')
                    }
                )

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

                response = {
                    'type': 'timeout',
                    'timestamp': line.split()[0].lstrip('[').rstrip(']') if timestamp else None,
                    'icmp_seq': line.replace('=', ' ').split()[isequence]
                }
                ping_responses.append(response)
                continue

            # normal responses
            else:

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

                response = {
                    'type': 'reply',
                    'timestamp': line.split()[0].lstrip('[').rstrip(']') if timestamp else None,
                    'bytes': line.split()[bts],
                    'response_ip': line.split()[rip].rstrip(':'),
                    'icmp_seq': line.split()[iseq],
                    'ttl': line.split()[t2l],
                    'time_ms': line.split()[tms]
                }
                ping_responses.append(response)
                continue

    raw_output['responses'] = ping_responses

    return raw_output


def bsd_parse(data):
    raw_output = {}
    ping_responses = []
    footer = False

    for line in filter(None, data.splitlines()):
        if line.startswith('PING '):
            raw_output.update(
                {
                    'destination_ip': line.split()[2].lstrip('(').rstrip(':').rstrip(')'),
                    'data_bytes': line.split()[3]
                }
            )
            continue

        if line.startswith('PING6('):
            line = line.replace('(', ' ').replace(')', ' ').replace('=', ' ')
            raw_output.update(
                {
                    'source_ip': line.split()[4],
                    'destination_ip': line.split()[6],
                    'data_bytes': line.split()[1]
                }
            )
            continue

        if line.startswith('---'):
            footer = True
            raw_output['destination'] = line.split()[1]
            continue

        if footer:
            if 'packets transmitted' in line:
                raw_output.update(
                    {
                        'packets_transmitted': line.split()[0],
                        'packets_received': line.split()[3],
                        'packet_loss_percent': line.split()[6].rstrip('%')
                    }
                )
                continue

            else:
                split_line = line.split(' = ')[1]
                split_line = split_line.split('/')
                raw_output.update(
                    {
                        'round_trip_ms_min': split_line[0],
                        'round_trip_ms_avg': split_line[1],
                        'round_trip_ms_max': split_line[2],
                        'round_trip_ms_stddev': split_line[3].replace(' ms', '')
                    }
                )

        # ping response lines
        else:
            # ipv4 lines
            if ',' not in line:

                # request timeout
                if line.startswith('Request timeout for '):
                    response = {
                        'type': 'timeout',
                        'icmp_seq': line.split()[4]
                    }
                    ping_responses.append(response)
                    continue

                # normal response
                else:
                    line = line.replace(':', ' ').replace('=', ' ')
                    response = {
                        'type': 'reply',
                        'bytes': line.split()[0],
                        'response_ip': line.split()[3],
                        'icmp_seq': line.split()[5],
                        'ttl': line.split()[7],
                        'time_ms': line.split()[9]
                    }
                    ping_responses.append(response)
                    continue

            # ipv6 lines
            else:
                line = line.replace(',', ' ').replace('=', ' ')
                response = {
                    'type': 'reply',
                    'bytes': line.split()[0],
                    'response_ip': line.split()[3],
                    'icmp_seq': line.split()[5],
                    'ttl': line.split()[7],
                    'time_ms': line.split()[9]
                }
                ping_responses.append(response)
                continue

    raw_output['responses'] = ping_responses

    return raw_output


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

    raw_output = {}

    if jc.utils.has_data(data):

        if 'time' in data.splitlines()[-2]:
            raw_output = linux_parse(data)
        else:
            raw_output = bsd_parse(data)

    if raw:
        return raw_output
    else:
        return process(raw_output)
