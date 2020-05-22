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


def normalize_route_headers(header):
    header = header.lower()
    header = header.replace('flags', 'route_flags')
    header = header.replace('refs', 'route_refs')
    header = header.replace('netif', 'iface')
    header = header.replace('-', '_')

    return header


def normalize_interface_headers(header):
    header = header.lower()
    header = header.replace('name', 'iface')
    header = header.replace('-', '_')

    return header


def parse_item(headers, entry, kind):
    entry = entry.split(maxsplit=len(headers) - 1)

    # fixup udp records with no state field entry
    if kind == 'network' and entry[0].startswith('udp'):
        entry.insert(5, None)
    if kind == 'network' and 'socket' in headers and 'udp' in str(entry):
        entry.insert(7, None)

    # fixup interface records with no address field entry
    if kind == 'interface' and len(entry) == 8:
        entry.insert(3, None)

    output_line = dict(zip(headers, entry))
    output_line['kind'] = kind

    return output_line


def parse_post(raw_data):
    for entry in raw_data:
        # fixup name field in Registered kernel control module
        if 'name' in entry:
            if entry['name']:
                entry['name'] = entry['name'].strip()

        # create network and transport protocol fields
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
    socket = False
    reg_kernel_control = False
    active_kernel_event = False
    active_kernel_control = False
    routing_table = False
    interface_table = False

    for line in cleandata:

        if line.startswith('Active Internet'):
            network = True
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Active Multipath Internet connections'):
            network = False
            multipath = True
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Active LOCAL (UNIX) domain sockets'):
            network = False
            multipath = False
            socket = True
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Registered kernel control modules'):
            network = False
            multipath = False
            socket = False
            reg_kernel_control = True
            active_kernel_event = False
            active_kernel_control = False
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Active kernel event sockets'):
            network = False
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = True
            active_kernel_control = False
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Active kernel control sockets'):
            network = False
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = True
            routing_table = False
            interface_table = False
            continue

        if line.startswith('Routing tables'):
            network = False
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            routing_table = True
            interface_table = False
            continue

        if line.startswith('Name  Mtu '):
            network = False
            multipath = False
            socket = False
            reg_kernel_control = False
            active_kernel_event = False
            active_kernel_control = False
            routing_table = False
            interface_table = True
            # don't continue since there is no real header row for this table

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

        if routing_table and line.startswith('Destination '):
            header_text = normalize_route_headers(line)
            headers = header_text.split()
            continue

        if interface_table and line.startswith('Name  Mtu '):
            header_text = normalize_interface_headers(line)
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

        if routing_table and not (line.startswith('Internet:') or line.startswith('Internet6:')):
            raw_output.append(parse_item(headers, line, 'route'))
            continue

        if interface_table:
            raw_output.append(parse_item(headers, line, 'interface'))
            continue

    return parse_post(raw_output)
