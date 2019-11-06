"""jc - JSON CLI output utility netstat Parser

Usage:
    Specify --netstat as the first argument if the piped input is coming from netstat
"""
import jc


def normalize_headers(header):
    header = header.lower()
    header = header.replace('local address', 'local_address')
    header = header.replace('foreign address', 'foreign_address')
    header = header.replace('pid/program name', 'program_name')
    header = header.replace('security context', 'security_context')
    return header.split()


def parse_network(headers, entry):
    # Count words in header
    # if len of line is one less than len of header, then insert None in field 5
    output_line = {}
    return output_line


def parse_socket(headers, entry):
    # get the column # of first letter of "state"
    # for each line check column # to see if state column is populated
    # remove [ and ] from each line
    output_line = {}
    return output_line


def post_process(network_list, socket_list):
    output = {}

    if network_list:
        output['network'] = network_list

    if socket_list:
        output['socket'] = socket_list

    # post process to split pid and program name and ip addresses and ports

    return output


def parse(data):
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    jc.jc.compatibility(__name__,
                        ['linux'])

    cleandata = data.splitlines()

    network = False
    socket = False
    headers = ''

    for line in cleandata:

        if line.find('Active Internet') == 0:
            network_list = []
            network = True
            socket = False
            continue

        if line.find('Active UNIX') == 0:
            socket_list = []
            network = False
            socket = True
            continue

        if line.find('Proto') == 0:
            headers = normalize_headers(line)
            continue

        if network:
            network_list.append(parse_network(headers, line))
            continue

        if socket:
            socket_list.append(parse_socket(headers, line))
            continue

    return post_process(network_list, socket_list)















    if entry.find('tcp') == 0:
        output_line['transport_protocol'] = 'tcp'

        if entry.find('p6') == 2:
            output_line['network_protocol'] = 'ipv6'

        else:
            output_line['network_protocol'] = 'ipv4'

    elif entry.find('udp') == 0:
        output_line['transport_protocol'] = 'udp'

        if entry.find('p6') == 2:
            output_line['network_protocol'] = 'ipv6'

        else:
            output_line['network_protocol'] = 'ipv4'
    else:
        return

    parsed_line = entry.split()

    output_line['local_address'] = parsed_line[3].rsplit(':', 1)[0]
    output_line['local_port'] = parsed_line[3].rsplit(':', 1)[-1]
    output_line['foreign_address'] = parsed_line[4].rsplit(':', 1)[0]
    output_line['foreign_port'] = parsed_line[4].rsplit(':', 1)[-1]

    if len(parsed_line) > 5:

        if parsed_line[5][0] not in string.digits and parsed_line[5][0] != '-':
            output_line['state'] = parsed_line[5]

            if len(parsed_line) > 6 and parsed_line[6][0] in string.digits:
                output_line['pid'] = parsed_line[6].split('/')[0]
                output_line['program_name'] = parsed_line[6].split('/')[1]
        else:
            if parsed_line[5][0] in string.digits:
                output_line['pid'] = parsed_line[5].split('/')[0]
                output_line['program_name'] = parsed_line[5].split('/')[1]

    output_line['receive_q'] = parsed_line[1]
    output_line['send_q'] = parsed_line[2]

    return output_line