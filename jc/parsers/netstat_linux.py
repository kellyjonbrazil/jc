"""jc - JSON CLI output utility Linux netstat Parser"""
import string


def normalize_headers(header):
    header = header.lower()
    header = header.replace('local address', 'local_address')
    header = header.replace('foreign address', 'foreign_address')
    header = header.replace('pid/program name', 'program_name')
    header = header.replace('security context', 'security_context')
    header = header.replace('i-node', 'inode')
    header = header.replace('-', '_')

    return header


def normalize_route_headers(header):
    header = header.lower()
    header = header.replace('flags', 'route_flags')
    header = header.replace('ref', 'route_refs')
    header = header.replace('-', '_')

    return header


def normalize_interface_headers(header):
    header = header.lower()
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


def parse_socket(header_text, headers, entry):
    # get the column # of first letter of "state"
    state_col = header_text.find('state')
    # get the program name column area
    pn_start = header_text.find('program_name')
    pn_end = header_text.find('path') - 1

    # remove [ and ] from each line
    entry = entry.replace('[ ]', '---')
    entry = entry.replace('[', ' ').replace(']', ' ')

    # find program_name column area and substitute spaces with \u2063 there
    old_pn = entry[pn_start:pn_end]
    new_pn = old_pn.replace(' ', '\u2063')
    entry = entry.replace(old_pn, new_pn)

    entry_list = entry.split(maxsplit=len(headers) - 1)
    # check column # to see if state column is populated
    if entry[state_col] in string.whitespace:
        entry_list.insert(4, None)

    output_line = dict(zip(headers, entry_list))
    output_line['kind'] = 'socket'

    # fix program_name field to turn \u2063 back to spaces
    if 'program_name' in output_line:
        if output_line['program_name']:
            old_d_pn = output_line['program_name']
            new_d_pn = old_d_pn.replace('\u2063', ' ')
            output_line['program_name'] = new_d_pn

    return output_line


def parse_route(headers, entry):
    entry = entry.split(maxsplit=len(headers) - 1)
    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'route'

    return output_line


def parse_interface(headers, entry):
    entry = entry.split(maxsplit=len(headers) - 1)
    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'interface'

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

        # add route_flags_pretty
        # Flag mapping from https://www.man7.org/linux/man-pages/man8/route.8.html
        if 'route_flags' in entry:
            flag_map = {
                'U': 'UP',
                'H': 'HOST',
                'G': 'GATEWAY',
                'R': 'REINSTATE',
                'D': 'DYNAMIC',
                'M': 'MODIFIED',
                'A': 'ADDRCONF',
                'C': 'CACHE',
                '!': 'REJECT'
            }

            pretty_flags = []

            for flag in entry['route_flags']:
                if flag in flag_map:
                    pretty_flags.append(flag_map[flag])

            entry['route_flags_pretty'] = pretty_flags

    return raw_data


def parse(cleandata):
    """
    Main text parsing function for OSX netstat

    Parameters:

        cleandata:   (string)  text data to parse

    Returns:

        List of dictionaries. Raw structured data.
    """
    raw_output = []
    network = False
    socket = False
    bluetooth = False
    routing_table = False
    interface_table = False
    headers = None

    for line in cleandata:

        if line.startswith('Active Internet'):
            network = True
            socket = False
            bluetooth = False
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Active UNIX'):
            network = False
            socket = True
            bluetooth = False
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Active Bluetooth'):
            network = False
            socket = False
            bluetooth = True
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Kernel IP routing table'):
            network = False
            socket = False
            bluetooth = False
            routing_table = True
            interface_table = False
            continue

        if line.startswith('Kernel Interface table'):
            network = False
            socket = False
            bluetooth = False
            routing_table = False
            interface_table = True
            continue

        # get headers
        if line.startswith('Proto'):
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        if line.startswith('Destination '):
            header_text = normalize_route_headers(line)
            headers = header_text.split()
            continue

        if line.startswith('Iface '):
            header_text = normalize_interface_headers(line)
            headers = header_text.split()
            continue

        # parse items
        if network:
            raw_output.append(parse_network(headers, line))
            continue

        if socket:
            raw_output.append(parse_socket(header_text, headers, line))
            continue

        if bluetooth:
            # not implemented
            continue

        if routing_table:
            raw_output.append(parse_route(headers, line))
            continue

        if interface_table:
            raw_output.append(parse_interface(headers, line))
            continue

    return parse_post(raw_output)
