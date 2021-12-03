"""jc - JSON CLI output utility `ping` command output parser

Supports `ping` and `ping6` output.

Usage (cli):

    Note:  Use the ping `-c` (count) option, otherwise data will not be piped to `jc`.

    $ ping -c 3 1.2.3.4 | jc --ping

    or

    $ jc ping -c 3 1.2.3.4

Usage (module):

    import jc.parsers.ping
    result = jc.parsers.ping.parse(ping_command_output)

Schema:

    {
      "source_ip":                   string,
      "destination_ip":              string,
      "data_bytes":                  integer,
      "pattern":                     string,        # (null if not set)
      "destination":                 string,
      "packets_transmitted":         integer,
      "packets_received":            integer,
      "packet_loss_percent":         float,
      "duplicates":                  integer,
      "round_trip_ms_min":           float,
      "round_trip_ms_avg":           float,
      "round_trip_ms_max":           float,
      "round_trip_ms_stddev":        float,
      "responses": [
        {
          "type":                    string,        # 'reply', 'timeout', 'unparsable_line', etc. See `_error_type.type_map` for all options
          "unparsed_line":           string,        # only if an 'unparsable_line' type
          "timestamp":               float,
          "bytes":                   integer,
          "response_ip":             string,
          "icmp_seq":                integer,
          "ttl":                     integer,
          "time_ms":                 float,
          "duplicate":               boolean,
          "vr":                      integer,       # hex value converted to decimal
          "hl":                      integer,       # hex value converted to decimal
          "tos":                     integer,       # hex value converted to decimal
          "len":                     integer,       # hex value converted to decimal
          "id":                      integer,       # hex value converted to decimal
          "flg":                     integer,       # hex value converted to decimal
          "off":                     integer,       # hex value converted to decimal
          "pro":                     integer,       # hex value converted to decimal
          "cks":                     ingeger,       # hex value converted to decimal
          "src":                     string,
          "dst":                     string
        }
      ]
    }

Examples:

    $ ping -c 3 -p ff cnn.com | jc --ping -p
    {
      "destination_ip": "151.101.1.67",
      "data_bytes": 56,
      "pattern": "0xff",
      "destination": "cnn.com",
      "packets_transmitted": 3,
      "packets_received": 3,
      "packet_loss_percent": 0.0,
      "duplicates": 0,
      "round_trip_ms_min": 28.015,
      "round_trip_ms_avg": 32.848,
      "round_trip_ms_max": 39.376,
      "round_trip_ms_stddev": 4.79,
      "responses": [
        {
          "type": "reply",
          "bytes": 64,
          "response_ip": "151.101.1.67",
          "icmp_seq": 0,
          "ttl": 59,
          "time_ms": 28.015,
          "duplicate": false
        },
        {
          "type": "reply",
          "bytes": 64,
          "response_ip": "151.101.1.67",
          "icmp_seq": 1,
          "ttl": 59,
          "time_ms": 39.376,
          "duplicate": false
        },
        {
          "type": "reply",
          "bytes": 64,
          "response_ip": "151.101.1.67",
          "icmp_seq": 2,
          "ttl": 59,
          "time_ms": 31.153,
          "duplicate": false
        }
      ]
    }

    $ ping -c 3 -p ff cnn.com | jc --ping -p -r
    {
      "destination_ip": "151.101.129.67",
      "data_bytes": "56",
      "pattern": "0xff",
      "destination": "cnn.com",
      "packets_transmitted": "3",
      "packets_received": "3",
      "packet_loss_percent": "0.0",
      "duplicates": "0",
      "round_trip_ms_min": "25.078",
      "round_trip_ms_avg": "29.543",
      "round_trip_ms_max": "32.553",
      "round_trip_ms_stddev": "3.221",
      "responses": [
        {
          "type": "reply",
          "bytes": "64",
          "response_ip": "151.101.129.67",
          "icmp_seq": "0",
          "ttl": "59",
          "time_ms": "25.078",
          "duplicate": false
        },
        {
          "type": "reply",
          "bytes": "64",
          "response_ip": "151.101.129.67",
          "icmp_seq": "1",
          "ttl": "59",
          "time_ms": "30.999",
          "duplicate": false
        },
        {
          "type": "reply",
          "bytes": "64",
          "response_ip": "151.101.129.67",
          "icmp_seq": "2",
          "ttl": "59",
          "time_ms": "32.553",
          "duplicate": false
        }
      ]
    }
"""
import string
import ipaddress
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = '`ping` and `ping6` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['ping', 'ping6']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = ['data_bytes', 'packets_transmitted', 'packets_received', 'bytes', 'icmp_seq', 'ttl',
                'duplicates', 'vr', 'hl', 'tos', 'len', 'id', 'flg', 'off', 'pro', 'cks']
    float_list = ['packet_loss_percent', 'round_trip_ms_min', 'round_trip_ms_avg', 'round_trip_ms_max',
                  'round_trip_ms_stddev', 'timestamp', 'time_ms']

    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

        if key in float_list:
            proc_data[key] = jc.utils.convert_to_float(proc_data[key])

        if key == 'responses':
            for entry in proc_data['responses']:
                for k in entry:
                    if k in int_list:
                        entry[k] = jc.utils.convert_to_int(entry[k])
                    if k in float_list:
                        entry[k] = jc.utils.convert_to_float(entry[k])

    return proc_data


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


def _linux_parse(data):
    raw_output = {}
    ping_responses = []
    pattern = None
    footer = False

    linedata = data.splitlines()

    # check for PATTERN
    if linedata[0].startswith('PATTERN: '):
        pattern = linedata.pop(0).split(': ')[1]

    while not linedata[0].startswith('PING '):
        linedata.pop(0)

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
                if ' duplicates,' in line:
                    raw_output.update(
                        {
                            'packets_transmitted': line.split()[0],
                            'packets_received': line.split()[3],
                            'packet_loss_percent': line.split()[7].rstrip('%'),
                            'duplicates': line.split()[5].lstrip('+'),
                            'time_ms': line.split()[11].replace('ms', '')
                        }
                    )
                    continue
                else:
                    raw_output.update(
                        {
                            'packets_transmitted': line.split()[0],
                            'packets_received': line.split()[3],
                            'packet_loss_percent': line.split()[5].rstrip('%'),
                            'duplicates': '0',
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
                        'round_trip_ms_stddev': split_line[3].split()[0]
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
            elif ' bytes from ' in line:
                try:
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
                        'time_ms': line.split()[tms],
                        'duplicate': True if 'DUP!' in line else False
                    }
                except Exception:
                    response = {
                        'type': 'unparsable_line',
                        'unparsed_line': line
                    }

                ping_responses.append(response)
                continue

    raw_output['responses'] = ping_responses

    return raw_output


def _bsd_parse(data):
    raw_output = {}
    ping_responses = []
    pattern = None
    footer = False
    ping_error = False

    linedata = data.splitlines()

    # check for PATTERN
    if linedata[0].startswith('PATTERN: '):
        pattern = linedata.pop(0).split(': ')[1]

    for line in filter(None, linedata):
        if line.startswith('PING '):
            raw_output.update(
                {
                    'destination_ip': line.split()[2].lstrip('(').rstrip(':').rstrip(')'),
                    'data_bytes': line.split()[3],
                    'pattern': pattern
                }
            )
            continue

        if line.startswith('PING6('):
            line = line.replace('(', ' ').replace(')', ' ').replace('=', ' ')
            raw_output.update(
                {
                    'source_ip': line.split()[4],
                    'destination_ip': line.split()[6],
                    'data_bytes': line.split()[1],
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
                if ' duplicates,' in line:
                    raw_output.update(
                        {
                            'packets_transmitted': line.split()[0],
                            'packets_received': line.split()[3],
                            'packet_loss_percent': line.split()[8].rstrip('%'),
                            'duplicates': line.split()[6].lstrip('+'),
                        }
                    )
                    continue
                else:
                    raw_output.update(
                        {
                            'packets_transmitted': line.split()[0],
                            'packets_received': line.split()[3],
                            'packet_loss_percent': line.split()[6].rstrip('%'),
                            'duplicates': '0',
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
                        'round_trip_ms_stddev': split_line[3].replace(' ms', '') if len(split_line) == 4 else None
                    }
                )

        # ping response lines
        else:
            # ipv4 lines
            if not _ipv6_in(line):

                # request timeout
                if line.startswith('Request timeout for '):
                    response = {
                        'type': 'timeout',
                        'icmp_seq': line.split()[4]
                    }
                    ping_responses.append(response)
                    continue

                # catch error responses
                err = _error_type(line)
                if err:
                    response = {
                        'type': err
                    }

                    try:
                        response['bytes'] = line.split()[0]
                        response['response_ip'] = line.split()[4].strip(':').strip('(').strip(')')
                    except Exception:
                        pass

                    ping_error = True
                    continue

                if ping_error:
                    if line.startswith('Vr'):
                        continue
                    else:
                        error_line = line.split()

                        try:
                            response.update(
                                {
                                    'vr': int(error_line[0], 16),   # convert from hex to decimal
                                    'hl': int(error_line[1], 16),
                                    'tos': int(error_line[2], 16),
                                    'len': int(error_line[3], 16),
                                    'id': int(error_line[4], 16),
                                    'flg': int(error_line[5], 16),
                                    'off': int(error_line[6], 16),
                                    'ttl': int(error_line[7], 16),
                                    'pro': int(error_line[8], 16),
                                    'cks': int(error_line[9], 16),
                                    'src': error_line[10],
                                    'dst': error_line[11],
                                }
                            )
                        except Exception:
                            pass

                        if response:
                            ping_responses.append(response)

                        ping_error = False
                        continue

                # normal response
                elif ' bytes from ' in line:
                    try:
                        line = line.replace(':', ' ').replace('=', ' ')

                        response = {
                            'type': 'reply',
                            'bytes': line.split()[0],
                            'response_ip': line.split()[3],
                            'icmp_seq': line.split()[5],
                            'ttl': line.split()[7],
                            'time_ms': line.split()[9]
                        }
                    except Exception:
                        response = {
                            'type': 'unparsable_line',
                            'unparsed_line': line
                        }

                    ping_responses.append(response)
                    continue

            # ipv6 lines
            elif ' bytes from ' in line:
                try:
                    line = line.replace(',', ' ').replace('=', ' ')
                    response = {
                        'type': 'reply',
                        'bytes': line.split()[0],
                        'response_ip': line.split()[3],
                        'icmp_seq': line.split()[5],
                        'ttl': line.split()[7],
                        'time_ms': line.split()[9]
                    }
                except Exception:
                    response = {
                        'type': 'unparsable_line',
                        'unparsed_line': line
                    }

                ping_responses.append(response)
                continue

    # identify duplicates in responses
    if ping_responses:
        seq_list = []
        for reply in ping_responses:
            if 'icmp_seq' in reply:
                seq_list.append(reply['icmp_seq'])
                reply['duplicate'] = True if seq_list.count(reply['icmp_seq']) > 1 else False

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

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):

        if ' time ' in data.splitlines()[-2] or ' time ' in data.splitlines()[-3]:
            raw_output = _linux_parse(data)
        else:
            raw_output = _bsd_parse(data)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
