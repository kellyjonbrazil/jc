"""jc - JSON CLI output utility OSX netstat Parser"""
import string
import jc.utils


def normalize_headers(header):
    header = header.lower()
    header = header.replace('local address', 'local_address')
    header = header.replace('foreign address', 'foreign_address')
    header = header.replace('(state)', 'state')
    header = header.replace('-', '_')

    return header


def parse_network(headers, entry):
    # Count words in header
    # if len of line is one less than len of header, then insert None in field 5
    entry = entry.split(maxsplit=len(headers) - 1)

    if len(entry) == len(headers) - 1:
        entry.insert(5, None)

    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'network'

    return output_line


def parse_socket(headers, entry):
    # Count words in header
    # if len of line is one less than len of header, then insert None in field 5
    entry = entry.split(maxsplit=len(headers) - 1)

    if len(entry) == len(headers) - 1:
        entry.insert(5, None)

    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'socket'

    return output_line


def parse_post(raw_data):
    # clean up trailing whitespace on each item in each entry
    # flags --- = null
    # program_name - = null
    # split pid and program name and ip addresses and ports
    # create network and transport protocol fields

    for entry in raw_data:
        for item in entry:
            try:
                entry[item] = entry[item].rstrip()
            except (AttributeError):
                # skips trying to rstrip Null entries
                pass

        if 'flags' in entry:
            if entry['flags'] == '---':
                entry['flags'] = None

        if 'program_name' in entry:
            entry['program_name'] = entry['program_name'].strip()
            if entry['program_name'] == '-':
                entry['program_name'] = None

            if entry['program_name']:
                pid = entry['program_name'].split('/', maxsplit=1)[0]
                name = entry['program_name'].split('/', maxsplit=1)[1]
                entry['pid'] = pid
                entry['program_name'] = name

        if 'local_address' in entry:
            if entry['local_address']:
                ladd = entry['local_address'].rsplit(':', maxsplit=1)[0]
                lport = entry['local_address'].rsplit(':', maxsplit=1)[1]
                entry['local_address'] = ladd
                entry['local_port'] = lport

        if 'foreign_address' in entry:
            if entry['foreign_address']:
                fadd = entry['foreign_address'].rsplit(':', maxsplit=1)[0]
                fport = entry['foreign_address'].rsplit(':', maxsplit=1)[1]
                entry['foreign_address'] = fadd
                entry['foreign_port'] = fport

        if 'proto' in entry and 'kind' in entry:
            if entry['kind'] == 'network':
                if 'tcp' in entry['proto']:
                    entry['transport_protocol'] = 'tcp'
                elif 'udp' in entry['proto']:
                    entry['transport_protocol'] = 'udp'
                else:
                    entry['transport_protocol'] = None

                if '6' in entry['proto']:
                    entry['network_protocol'] = 'ipv6'
                else:
                    entry['network_protocol'] = 'ipv4'

    return raw_data


def parse(cleandata):
    """
    Main text parsing function

    Parameters:

        cleandata:   (string)  text data to parse

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    raw_output = []
    network = False
    socket = False
    bluetooth = False
    headers = ''
    network_list = []
    socket_list = []

    for line in cleandata:

        if line.startswith('Active Internet'):
            network_list = []
            network = True
            socket = False
            bluetooth = False
            continue

        if line.startswith('Active LOCAL (UNIX) domain sockets'):
            socket_list = []
            network = False
            socket = True
            bluetooth = False
            continue

        if line.startswith('Active Bluetooth'):
            network = False
            socket = False
            bluetooth = True
            continue

        if line.startswith('Socket ') or line.startswith('Proto '):
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        if line.startswith('Address '):
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        if network:
            network_list.append(parse_network(headers, line))
            continue

        if socket:
            socket_list.append(parse_socket(headers, line))
            continue

        if bluetooth:
            # maybe implement later if requested
            continue

    for item in [network_list, socket_list]:
        for entry in item:
            raw_output.append(entry)

    return raw_output

