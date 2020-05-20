"""jc - JSON CLI output utility OSX netstat Parser"""


def normalize_headers(header):
    header = header.lower()
    header = header.replace('local address', 'local_address')
    header = header.replace('foreign address', 'foreign_address')
    header = header.replace('(state)', 'state')
    header = header.replace('inode', 'osx_inode')
    header = header.replace('-', '_')

    return header


def parse_network(headers, entry):
    entry = entry.split(maxsplit=len(headers) - 1)

    # if len of line is one less than len of header, then insert None in field 5
    if len(entry) == len(headers) - 1:
        entry.insert(5, None)

    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'network'

    return output_line


def parse_socket(headers, entry):
    entry = entry.split(maxsplit=len(headers) - 1)
    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'socket'

    return output_line


def parse_reg_kernel_control(headers, entry):
    entry = entry.split(maxsplit=len(headers) - 1)
    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'Registered kernel control module'

    return output_line


def parse_active_kernel_event(headers, entry):
    entry = entry.split(maxsplit=len(headers) - 1)
    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'Active kernel event socket'

    return output_line


def parse_active_kernel_control(headers, entry):
    entry = entry.split(maxsplit=len(headers) - 1)
    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'Active kernel control socket'

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
                entry['transport_protocol'] = entry['proto'][:-1]

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
    multipath = False
    reg_kernel_control = False
    active_kernel_event = False
    active_kernel_control = False
    socket = False
    headers = ''
    network_list = []
    socket_list = []
    reg_kernel_control_list = []
    active_kernel_event_list = []
    active_kernel_control_list = []

    for line in cleandata:

        if line.startswith('Active Internet'):
            network_list = []
            network = True
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            continue

        if line.startswith('Active Multipath Internet connections'):
            # skip for now
            network = False
            multipath = True
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            continue

        if line.startswith('Active LOCAL (UNIX) domain sockets'):
            socket_list = []
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
            network_list.append(parse_network(headers, line))
            continue

        if multipath:
            # skip for now
            continue

        if socket:
            socket_list.append(parse_socket(headers, line))
            continue

        if reg_kernel_control:
            reg_kernel_control_list.append(parse_reg_kernel_control(headers, line))
            continue

        if active_kernel_event:
            active_kernel_event_list.append(parse_active_kernel_event(headers, line))
            continue

        if active_kernel_control:
            active_kernel_control_list.append(parse_active_kernel_control(headers, line))
            continue

    for item in [network_list, socket_list, reg_kernel_control_list, active_kernel_event_list, active_kernel_control_list]:
        raw_output.extend(item)

    return parse_post(raw_output)
