"""jc - JSON CLI output utility OSX netstat Parser"""


def normalize_headers(header):
    header = header.lower()
    header = header.replace('local address', 'local_address')
    header = header.replace('foreign address', 'foreign_address')
    header = header.replace('(state)', 'state')
    header = header.replace('inode', 'osx_inode')
    header = header.replace('flags', 'osx_flags')
    header = header.replace('-', '_')

    return header


def parse_item(headers, entry, kind):
    entry = entry.split(maxsplit=len(headers) - 1)

    # fixup udp records with no state field entry
    if kind == 'network' and entry[0].startswith('udp'):
        entry.insert(5, None)
    if kind == 'network' and 'socket' in headers and 'udp' in str(entry):
        entry.insert(7, None)

    output_line = dict(zip(headers, entry))
    output_line['kind'] = kind

    return output_line


def parse_post(raw_data):
    # create network and transport protocol fields
    for entry in raw_data:
        if 'local_address' in entry:
            if entry['local_address']:
                ladd = entry['local_address'].rsplit('.', maxsplit=1)[0]
                lport = entry['local_address'].rsplit('.', maxsplit=1)[1]
                entry['local_address'] = ladd
                entry['local_port'] = lport

        if 'foreign_address' in entry:
            if entry['foreign_address']:
                fadd = entry['foreign_address'].rsplit('.', maxsplit=1)[0]
                fport = entry['foreign_address'].rsplit('.', maxsplit=1)[1]
                entry['foreign_address'] = fadd
                entry['foreign_port'] = fport

        if 'proto' in entry and 'kind' in entry:
            if entry['kind'] == 'network':
                if entry['proto'] == 'udp46':
                    entry['transport_protocol'] = entry['proto'][:-2]
                elif entry['proto'].startswith('icm'):
                    entry['transport_protocol'] = 'icmp'
                else:
                    entry['transport_protocol'] = entry['proto'][:-1]

                if '6' in entry['proto']:
                    entry['network_protocol'] = 'ipv6'
                else:
                    entry['network_protocol'] = 'ipv4'

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
    multipath = False
    reg_kernel_control = False
    active_kernel_event = False
    active_kernel_control = False
    socket = False

    for line in cleandata:

        if line.startswith('Active Internet'):
            network = True
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            continue

        if line.startswith('Active Multipath Internet connections'):
            network = False
            multipath = True
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            continue

        if line.startswith('Active LOCAL (UNIX) domain sockets'):
            network = False
            multipath = False
            socket = True
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            continue

        if line.startswith('Registered kernel control modules'):
            network = False
            multipath = False
            socket = False
            reg_kernel_control = True
            active_kernel_event = False
            active_kernel_control = False
            continue

        if line.startswith('Active kernel event sockets'):
            network = False
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = True
            active_kernel_control = False
            continue

        if line.startswith('Active kernel control sockets'):
            network = False
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = True
            continue

        # get headers
        if network and (line.startswith('Socket ') or line.startswith('Proto ')):
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        if socket and line.startswith('Address '):
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        if reg_kernel_control and (line.startswith('id ') or line.startswith('kctlref ')):
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        if active_kernel_event and (line.startswith('Proto ') or line.startswith('             pcb ')):
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        if active_kernel_control and (line.startswith('Proto ') or line.startswith('             pcb ')):
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        # get items
        if network:
            raw_output.append(parse_item(headers, line, 'network'))
            continue

        if multipath:
            # not implemented
            continue

        if socket:
            raw_output.append(parse_item(headers, line, 'socket'))
            continue

        if reg_kernel_control:
            raw_output.append(parse_item(headers, line, 'Registered kernel control module'))
            continue

        if active_kernel_event:
            raw_output.append(parse_item(headers, line, 'Active kernel event socket'))
            continue

        if active_kernel_control:
            raw_output.append(parse_item(headers, line, 'Active kernel control socket'))
            continue

    return parse_post(raw_output)
