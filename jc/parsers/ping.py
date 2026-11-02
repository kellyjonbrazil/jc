r"""jc - JSON Convert `ping` command output parser

Supports `ping` and `ping6` output.

Usage (cli):

> Note:  Use the ping `-c` (count) option, otherwise data will not be
> piped to `jc`.

    $ ping -c 3 1.2.3.4 | jc --ping

or

    $ jc ping -c 3 1.2.3.4

Usage (module):

    import jc
    result = jc.parse('ping', ping_command_output)

Schema:

    {
      "source_ip":                   string,
      "destination_ip":              string,
      "data_bytes":                  integer,
      "pattern":                     string,        # null if not set
      "destination":                 string,
      "packets_transmitted":         integer,
      "packets_received":            integer,
      "packet_loss_percent":         float,
      "duplicates":                  integer,
      "errors":                      integer,
      "corrupted":                   integer,
      "round_trip_ms_min":           float,
      "round_trip_ms_avg":           float,
      "round_trip_ms_max":           float,
      "round_trip_ms_stddev":        float,
      "responses": [
        {
          "type":                    string,        # [0]
          "unparsed_line":           string,        # [1]
          "timestamp":               float,
          "bytes":                   integer,
          "response_ip":             string,
          "icmp_seq":                integer,
          "ttl":                     integer,
          "time_ms":                 float,
          "duplicate":               boolean,
          "vr":                      integer,       # [2]
          "hl":                      integer,       # [2]
          "tos":                     integer,       # [2]
          "len":                     integer,       # [2]
          "id":                      integer,       # [2]
          "flg":                     integer,       # [2]
          "off":                     integer,       # [2]
          "pro":                     integer,       # [2]
          "cks":                     integer,       # [2]
          "src":                     string,
          "dst":                     string
        }
      ]
    }

    [0] 'reply', 'timeout', 'unparsable_line', etc. See
        `_error_type.type_map` and `_error_type_v6.type_map` for all
        options
    [1] only if an 'unparsable_line' type
    [2] hex value converted to decimal

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
import re
import string
import ipaddress
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.12'
    description = '`ping` and `ping6` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['ping', 'ping6']
    tags = ['command']


__version__ = info.version


# Linux reply line: '[<timestamp>] <bytes> bytes from <name> (<ip>): icmp_seq=N ttl=N time=X ms ...'
# The sender is either '<name> (<ip>)' or a bare '<ip>'. The name branch is
# greedy so the last '(<ip>): icmp_seq=' on the line is used.
_LINUX_REPLY_RE = re.compile(
    r'^(?:\[(?P<timestamp>[^\] ]+)\] )?'
    r'(?P<bytes>\d+) bytes from '
    r'(?:.* \((?P<paren_ip>[^ ()]+)\)|(?P<bare_ip>[^ ()]+))'
    r': (?:icmp_seq|icmp_req|seq)=(?P<icmp_seq>\d+)'
    r'(?: (?:ttl|hlim)=(?P<ttl>\d+))?'
    r'(?: time=(?P<time_ms>[0-9.]+) ms)?'
    r'(?P<rest>(?:\D.*)?)$'
)


# Linux header line:
#   'PING <host> (<ip>) [from <src> <dev>: ]<n>(<m>) bytes of data.'
#   'PING <host> (<ip>) [from <src> <dev>: ]<n> data bytes' (IPv6)
#   'PING <host>(<ip>) [from <src> <dev>: ]<n> data bytes' (older IPv6)
#   'PING <host>(<name> (<ip>)) [from <src> <dev>: ]<n> data bytes' (older IPv6)
# 'from' can be part of a host name, so the header is matched as a whole.
_LINUX_HEADER_RE = re.compile(
    r'^PING [^ ()]* ?\((?:[^ ()]+ \((?P<named_ip>[^ ()]+)\)|(?P<ip>[^ ()]+))\) '
    r'(?:, flow 0x[0-9a-fA-F]+, )?'
    r'(?:from [^ ]+ [^ ]*: )?'
    r'(?P<data_bytes>\d+)(?:\(\d+\))? (?:bytes of data\.|data bytes)$'
)


# BSD header line:
#   'PING <host> (<ip>)[ from <src>]: <n> data bytes'
_BSD_HEADER_RE = re.compile(
    r'^PING [^ ]+ \((?P<ip>[^ ()]+)\)(?: from [^ ]+)?: (?P<data_bytes>\d+) data bytes$'
)


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = {
        'data_bytes', 'packets_transmitted', 'packets_received', 'bytes', 'icmp_seq', 'ttl',
        'duplicates', 'corrupted', 'errors', 'vr', 'hl', 'tos', 'len', 'id', 'flg', 'off', 'pro', 'cks'
    }

    float_list = {
        'packet_loss_percent', 'round_trip_ms_min', 'round_trip_ms_avg', 'round_trip_ms_max',
        'round_trip_ms_stddev', 'timestamp', 'time_ms'
    }

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
    # IPv4 ICMP error messages from pr_icmph() in:
    # https://github.com/iputils/iputils/blob/master/ping/ping.c
    # https://github.com/freebsd/freebsd-src/blob/main/sbin/ping/ping.c
    # https://github.com/apple-oss-distributions/network_cmds/blob/main/ping.tproj/ping.c
    # and IPv6 ICMP error messages from pr_icmph() in:
    # https://github.com/freebsd/freebsd-src/blob/main/sbin/ping/ping6.c
    # https://github.com/apple-oss-distributions/network_cmds/blob/main/ping6.tproj/ping6.c
    type_map = {
        'Destination Net Unreachable': 'destination_net_unreachable',
        'Destination Host Unreachable': 'destination_host_unreachable',
        'Destination Protocol Unreachable': 'destination_protocol_unreachable',
        'Destination Port Unreachable': 'destination_port_unreachable',
        'Frag needed and DF set': 'frag_needed_and_df_set',
        'frag needed and DF set': 'frag_needed_and_df_set',
        'Source Route Failed': 'source_route_failed',
        'Destination Net Unknown': 'destination_net_unknown',
        'Destination Host Unknown': 'destination_host_unknown',
        'Source Host Isolated': 'source_host_isolated',
        'Destination Net Prohibited': 'destination_net_prohibited',
        'Destination Host Prohibited': 'destination_host_prohibited',
        'Destination Net Unreachable for Type of Service': 'destination_net_unreachable_for_type_of_service',
        'Destination Host Unreachable for Type of Service': 'destination_host_unreachable_for_type_of_service',
        'Packet filtered': 'packet_filtered',
        'Communication prohibited by filter': 'communication_prohibited_by_filter',
        'Precedence Violation': 'precedence_violation',
        'Precedence Cutoff': 'precedence_cutoff',
        'Dest Unreachable, Bad Code': 'dest_unreachable_bad_code',
        'Source Quench': 'source_quench',
        'Redirect Network': 'redirect_network',
        'Redirect Host': 'redirect_host',
        'Redirect Type of Service and Network': 'redirect_type_of_service_and_network',
        'Redirect Type of Service and Host': 'redirect_type_of_service_and_host',
        'Redirect, Bad Code': 'redirect_bad_code',
        'Time to live exceeded': 'time_to_live_exceeded',
        'Frag reassembly time exceeded': 'frag_reassembly_time_exceeded',
        'Time exceeded, Bad Code': 'time_exceeded_bad_code',
        'Parameter problem': 'parameter_problem',
        # IPv6 messages of BSD ping6 that are not in the list above
        'No Route to Destination': 'no_route_to_destination',
        'Destination Administratively Unreachable': 'destination_administratively_unreachable',
        'Destination Unreachable Beyond Scope': 'destination_unreachable_beyond_scope',
        'Destination Unreachable, Bad Code': 'destination_unreachable_bad_code',
        'Packet too big': 'packet_too_big'
    }

    # longest first, so 'Destination Net Unreachable for Type of Service'
    # is not taken for 'Destination Net Unreachable'
    for err_type in sorted(type_map, key=len, reverse=True):
        if err_type in line:
            return type_map[err_type]

    return None


def _error_type_v6(line):
    # IPv6 ICMP error messages from pr_icmph() in:
    # https://github.com/iputils/iputils/blob/master/ping/ping6_common.c
    type_map = {
        'Destination unreachable': 'destination_unreachable',
        'Packet too big': 'packet_too_big',
        'Time exceeded:': 'time_exceeded',
        'Parameter problem:': 'parameter_problem',
    }
    code_map = {
        'destination_unreachable': {
            'No route': 'no_route',
            'Administratively prohibited': 'administratively_prohibited',
            "Beyond scope of source address": 'beyond_scope_of_source_address',
            'Address unreachable': 'address_unreachable',
            'Port unreachable': 'port_unreachable',
        },
        'time_exceeded': {
            'Hop limit': 'hop_limit',
            'Defragmentation failure': 'fragment_reassembly_time_exceeded',
        },
    }

    return_code = None
    for err_type, code in type_map.items():
        if err_type in line:
            return_code = code
            for err_code, code_name in code_map.get(code, {}).items():
                if err_code in line:
                    return_code += '_' + code_name
    return return_code


def _linux_error_response(line, err):
    # 'From <ip> icmp_seq=N <message>' or, if ping resolved the sender to a
    # name, 'From <name> (<ip>) icmp_seq=N <message>'. With -D the line
    # starts with '[<timestamp>] '.
    line_list = line.split()
    timestamp = line.startswith('[')
    timestamp_offset = 1 if timestamp else 0
    shift = 0
    response_ip = line_list[timestamp_offset + 1]
    if len(line_list) > timestamp_offset + 2 and line_list[timestamp_offset + 2].startswith('('):
        shift = 1
        response_ip = line_list[timestamp_offset + 2].strip('()')

    return {
        'type': err,
        'response_ip': response_ip,
        'icmp_seq': line.replace('=', ' ').split()[timestamp_offset + 3 + shift],
        'timestamp': line_list[0].lstrip('[').rstrip(']') if timestamp else None
    }


def _bsd_reply_fields(line):
    # '<bytes> bytes from <ip>: icmp_seq=N ttl=N time=X ms' (IPv4) or
    # '<bytes> bytes from <ip>, icmp_seq=N hlim=N time=X ms' (IPv6) once ':'
    # or ',' and '=' are replaced with spaces. BusyBox prints 'seq=' for
    # 'icmp_seq='. Error messages that are not in _error_type() also start
    # with '<bytes> bytes from <ip>: ', so check the labels.
    fields = line.split()
    if (len(fields) < 10
            or fields[4] not in ('icmp_seq', 'seq')
            or fields[6] not in ('ttl', 'hlim')
            or fields[8] != 'time'):
        raise ValueError('not a reply line')
    return fields


def _linux_parse(data):
    raw_output = {}
    ping_responses = []
    pattern = None
    footer = False

    linedata = jc.utils.splitlines(data)

    # check for PATTERN
    if linedata[0].startswith('PATTERN: '):
        pattern = linedata.pop(0).split(': ')[1]

    while not linedata[0].startswith('PING '):
        linedata.pop(0)

    ipv4 = True if 'bytes of data' in linedata[0] else False

    if ipv4 and linedata[0][5] not in string.digits:
        hostname = True
        # fixup for missing hostname
        linedata[0] = linedata[0][:5] + 'nohost' + linedata[0][5:]
    elif ipv4 and linedata[0][5] in string.digits:
        hostname = False
    elif not ipv4 and ' (' in linedata[0]:
        hostname = True
    else:
        hostname = False

    for line in filter(None, linedata):
        if line.startswith('PING '):
            m = _LINUX_HEADER_RE.match(line)
            if m:
                destination_ip = m.group('named_ip') or m.group('ip')
                data_bytes = m.group('data_bytes')

            else:
                source_ip = ' from ' in line
                if ipv4:
                    if source_ip:
                        dst_ip, dta_byts = (2, 6)
                    else:
                        dst_ip, dta_byts = (2, 3)
                else:
                    if source_ip and hostname:
                        dst_ip, dta_byts = (3, 7)
                    elif source_ip and not hostname:
                        dst_ip, dta_byts = (2, 6)
                    elif not source_ip and hostname:
                        dst_ip, dta_byts = (3, 4)
                    else:
                        dst_ip, dta_byts = (2, 3)

                line = line.replace('(', ' ').replace(')', ' ')
                destination_ip = line.split()[dst_ip].lstrip('(').rstrip(')')
                data_bytes = line.split()[dta_byts]

            raw_output.update(
                {
                    'destination_ip': destination_ip,
                    'data_bytes': data_bytes,
                    'pattern': pattern
                }
            )
            continue

        if line.startswith('---'):
            footer = True
            if line[4] != ' ':  # fixup for missing hostname
                raw_output['destination'] = line.split()[1]
            continue

        if footer:
            # Init in zero, to keep compatibility with previous behaviour
            if 'duplicates' not in raw_output:
                raw_output['duplicates'] = '0'

            #
            # See: https://github.com/dgibson/iputils/blob/master/ping_common.c#L995
            #
            m = re.search(r'(?<!\d)(\d+) packets transmitted', line)
            if m:
                raw_output['packets_transmitted'] = m.group(1)

            m = re.search(r'(?<!\d)(\d+) received,', line)
            if m:
                raw_output['packets_received'] = m.group(1)

            m = re.search(r'[+](\d+) duplicates', line)
            if m:
                raw_output['duplicates'] = m.group(1)

            m = re.search(r'[+](\d+) corrupted', line)
            if m:
                raw_output['corrupted'] = m.group(1)

            m = re.search(r'[+](\d+) errors', line)
            if m:
                raw_output['errors'] = m.group(1)

            m = re.search(r'(?<![\d\.])([\d\.]+)% packet loss', line)
            if m:
                raw_output['packet_loss_percent'] = m.group(1)

            m = re.search(r'time (\d+)ms', line)
            if m:
                raw_output['time_ms'] = m.group(1)

            m = re.search(r'rtt min\/avg\/max\/mdev += +([\d\.]+)\/([\d\.]+)\/([\d\.]+)\/([\d\.]+) ms', line)
            if m:
                raw_output['round_trip_ms_min'] = m.group(1)
                raw_output['round_trip_ms_avg'] = m.group(2)
                raw_output['round_trip_ms_max'] = m.group(3)
                raw_output['round_trip_ms_stddev'] = m.group(4)

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
            if ' bytes from ' in line:
                m = _LINUX_REPLY_RE.match(line.strip())
                if m:
                    response = {
                        'type': 'reply',
                        'timestamp': m.group('timestamp'),
                        'bytes': m.group('bytes'),
                        'response_ip': m.group('paren_ip') or m.group('bare_ip'),
                        'icmp_seq': m.group('icmp_seq'),
                        'ttl': m.group('ttl'),
                        'time_ms': m.group('time_ms'),
                        'duplicate': 'DUP!' in m.group('rest')
                    }
                    ping_responses.append(response)
                    continue

            # error responses
            err = _error_type(line) if ipv4 else _error_type_v6(line)
            if err:
                try:
                    response = _linux_error_response(line, err)
                except Exception:
                    response = {
                        'type': 'unparsable_line',
                        'unparsed_line': line
                    }

                ping_responses.append(response)
                continue

            if ' bytes from ' in line:
                response = {
                    'type': 'unparsable_line',
                    'unparsed_line': line
                }
                ping_responses.append(response)
                continue

    raw_output['responses'] = ping_responses

    return raw_output


def _bsd_error_sender(line):
    # error lines are 'N bytes from <ip>: <message>' or, when the sender
    # was resolved to a name, 'N bytes from <name> (<ip>): <message>'
    line_list = line.split()
    if len(line_list) > 4 and line_list[4].startswith('('):
        return line_list[4].strip(':').strip('(').strip(')')

    sender = line_list[3]
    if sender.endswith(':'):
        sender = sender[:-1]

    return sender


def _bsd_parse(data):
    raw_output = {}
    ping_responses = []
    pattern = None
    footer = False
    ping_error = False
    ipv6 = False

    linedata = jc.utils.splitlines(data)

    # check for PATTERN
    if linedata[0].startswith('PATTERN: '):
        pattern = linedata.pop(0).split(': ')[1]

    for line in filter(None, linedata):
        if line.startswith('PING '):
            m = _BSD_HEADER_RE.match(line.strip())
            if m:
                destination_ip = m.group('ip')
                data_bytes = m.group('data_bytes')
            else:
                destination_ip = line.split()[2].lstrip('(').rstrip(':').rstrip(')')
                data_bytes = line.split()[3]

            raw_output.update(
                {
                    'destination_ip': destination_ip,
                    'data_bytes': data_bytes,
                    'pattern': pattern
                }
            )
            continue

        # FreeBSD 13 and newer print 'PING(' instead of 'PING6('
        if line.startswith(('PING6(', 'PING(')):
            ipv6 = True
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
            # ipv6 error lines. The returned IPv6 header that follows them
            # is not read.
            if ipv6:
                err = _error_type(line)
                if err:
                    response = {
                        'type': err
                    }

                    try:
                        response['bytes'] = line.split()[0]
                        response['response_ip'] = _bsd_error_sender(line)
                    except Exception:
                        pass

                    ping_responses.append(response)
                    continue

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
                        response['response_ip'] = _bsd_error_sender(line)
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
                        fields = _bsd_reply_fields(line.replace(':', ' ').replace('=', ' '))

                        response = {
                            'type': 'reply',
                            'bytes': fields[0],
                            'response_ip': fields[3],
                            'icmp_seq': fields[5],
                            'ttl': fields[7],
                            'time_ms': fields[9]
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
                    fields = _bsd_reply_fields(line.replace(',', ' ').replace('=', ' '))

                    response = {
                        'type': 'reply',
                        'bytes': fields[0],
                        'response_ip': fields[3],
                        'icmp_seq': fields[5],
                        'ttl': fields[7],
                        'time_ms': fields[9]
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
        seen_seq = set()
        for reply in ping_responses:
            if 'icmp_seq' in reply:
                reply['duplicate'] = reply['icmp_seq'] in seen_seq
                seen_seq.add(reply['icmp_seq'])

    raw_output['responses'] = ping_responses

    return raw_output


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):

        lines = [line for line in jc.utils.splitlines(data) if line.strip()]

        # the linux statistics line ('..., time 4149ms') is followed by the
        # rtt line, or is the last line when nothing was received. Look at the
        # last two non-blank lines since trailing blank lines may be stripped.
        last_lines = lines[-2:]

        # without the statistics lines (e.g. ping was stopped at once) the
        # linux header line tells
        header = next((line.strip() for line in lines if line.startswith('PING ')), '')
        linux_header = header.endswith(' bytes of data.') or _LINUX_HEADER_RE.match(header)

        if linux_header or any(' time ' in line for line in last_lines):
            raw_output = _linux_parse(data)
        else:
            raw_output = _bsd_parse(data)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
