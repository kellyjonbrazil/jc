"""jc - JSON CLI output utility `ping` command output streaming parser

Usage (cli):

    $ ping | jc --ping_s

Usage (module):

    import jc.parsers.ping_s
    result = jc.parsers.ping_s.parse(ping_command_output)    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "ping":            string,
      "_meta":                       # This object only exists if using -q or quiet=True
        {
          "success":    booean,      # true if successfully parsed, false if error
          "error_msg":  string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
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
import jc.utils


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
    # process the data

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

    for line in data:
        try:
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

            if quiet:
                output_line['_meta'] = {'success': True}
            
            if raw:
                yield output_line
            else:
                yield _process(output_line)
            
        except Exception as e:
            if not quiet:
                e.args = (str(e) + '... Use the quiet option (-q) to ignore errors.',)
                raise e
            else:
                yield {
                    '_meta':
                        {
                            'success': False,
                            'error': 'error parsing line',
                            'line': line.strip()
                        }
                }
