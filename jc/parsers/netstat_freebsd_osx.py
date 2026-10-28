r"""jc - JSON Convert FreeBSD and OSX netstat Parser"""
import re

# complete header lines of the routing and interface tables. Matching the
# whole header keeps a row whose first word is `Name` or `Destination` (for
# example a route to a host with that name) from being read as a header.
_ROUTE_HEADER_RE = re.compile(r'Destination\s+Gateway\s+Flags\s')
_INTERFACE_HEADER_RE = re.compile(r'Name\s+Mtu\s+Network\s+Address\s')
_TRANSPORT_SUFFIX_RE = re.compile(r'(tcp|udp|sctp)(46|4|6)')


def normalize_headers(header):
    header = header.lower()
    header = header.replace('local address', 'local_address')
    header = header.replace('foreign address', 'foreign_address')
    header = header.replace('(state)', 'state')
    header = header.replace('inode', 'unix_inode')
    header = header.replace('flags', 'unix_flags')
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


def header_flags(headers):
    """Check the header once for the columns that change how rows are parsed."""
    return 'socket' in headers, '0_win' in headers


def parse_item(headers, entry, kind, flags):
    has_socket, has_0win = flags
    entry = entry.split(maxsplit=len(headers) - 1)

    # only the protocol column says whether this is a udp row: other columns
    # (for example a peer host name) can contain the text `udp`
    proto_is_udp = False
    if 'proto' in headers:
        proto_index = headers.index('proto')
        proto_is_udp = proto_index < len(entry) and entry[proto_index].startswith('udp')

    # fixup udp records with no state field entry
    if kind == 'network' and entry[0].startswith('udp'):
        entry.insert(5, None)

    if kind == 'network' and has_socket and proto_is_udp:
        entry.insert(7, None)

    # fixup -T output on FreeBSD
    if kind == 'network' and has_0win and entry[0].startswith('udp'):
        entry.insert(1, '')
        entry.insert(1, '')
        entry.insert(1, '')

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
                if entry['proto'].startswith('icm'):
                    entry['transport_protocol'] = 'icmp'
                else:
                    # remove the address family suffix (4, 6 or 46) only
                    # from tcp, udp and sctp
                    suffixed = _TRANSPORT_SUFFIX_RE.fullmatch(entry['proto'])
                    if suffixed:
                        entry['transport_protocol'] = suffixed.group(1)
                    else:
                        entry['transport_protocol'] = entry['proto']

                if '6' in entry['proto']:
                    entry['network_protocol'] = 'ipv6'
                else:
                    entry['network_protocol'] = 'ipv4'

        # add route_flags_pretty field
        if 'route_flags' in entry:
            flag_map = {
                '1': 'PROTO1',
                '2': 'PROTO2',
                '3': 'PROTO3',
                'B': 'BLACKHOLE',
                'b': 'BROADCAST',
                'C': 'CLONING',
                'c': 'PRCLONING',
                'D': 'DYNAMIC',
                'G': 'GATEWAY',
                'H': 'HOST',
                'I': 'IFSCOPE',
                'i': 'IFREF',
                'L': 'LLINFO',
                'M': 'MODIFIED',
                'm': 'MULTICAST',
                'R': 'REJECT',
                'r': 'ROUTER',
                'S': 'STATIC',
                'U': 'UP',
                'W': 'WASCLONED',
                'X': 'XRESOLVE',
                'Y': 'PROXY',
            }

            pretty_flags = []

            for flag in entry['route_flags']:
                if flag in flag_map:
                    pretty_flags.append(flag_map[flag])

            entry['route_flags_pretty'] = pretty_flags

        # strip whitespace from beginning and end of all string values
        for item in entry:
            if isinstance(entry[item], str):
                entry[item] = entry[item].strip()

    return raw_data


def parse(cleandata):
    """
    Main text parsing function for OSX netstat

    Parameters:

        cleandata:   (string)  text data to parse

    Returns:

        List of Dictionaries. Raw structured data.
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

        if line.startswith('Active LOCAL (UNIX) domain sockets') or line.startswith('Active UNIX domain sockets'):
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

        if _INTERFACE_HEADER_RE.match(line):
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
        if network and (line.startswith('Socket ') or line.startswith('Proto ') or line.startswith('Tcpcb ')):
            header_text = normalize_headers(line)
            headers = header_text.split()
            flags = header_flags(headers)
            continue

        if socket and line.startswith('Address '):
            header_text = normalize_headers(line)
            headers = header_text.split()
            flags = header_flags(headers)
            continue

        if reg_kernel_control and (line.startswith('id ') or line.startswith('kctlref ')):
            header_text = normalize_headers(line)
            headers = header_text.split()
            flags = header_flags(headers)
            continue

        if active_kernel_event and (line.startswith('Proto ') or line.startswith('             pcb ')):
            header_text = normalize_headers(line)
            headers = header_text.split()
            flags = header_flags(headers)
            continue

        if active_kernel_control and (line.startswith('Proto ') or line.startswith('             pcb ')):
            header_text = normalize_headers(line)
            headers = header_text.split()
            flags = header_flags(headers)
            continue

        if routing_table and _ROUTE_HEADER_RE.match(line):
            header_text = normalize_route_headers(line)
            headers = header_text.split()
            flags = header_flags(headers)
            continue

        if interface_table and _INTERFACE_HEADER_RE.match(line):
            header_text = normalize_interface_headers(line)
            headers = header_text.split()
            flags = header_flags(headers)
            continue

        # get items
        if network:
            raw_output.append(parse_item(headers, line, 'network', flags))
            continue

        if multipath:
            # not implemented
            continue

        if socket:
            raw_output.append(parse_item(headers, line, 'socket', flags))
            continue

        if reg_kernel_control:
            raw_output.append(parse_item(headers, line, 'Registered kernel control module', flags))
            continue

        if active_kernel_event:
            raw_output.append(parse_item(headers, line, 'Active kernel event socket', flags))
            continue

        if active_kernel_control:
            raw_output.append(parse_item(headers, line, 'Active kernel control socket', flags))
            continue

        if routing_table and not (line.startswith('Internet:') or line.startswith('Internet6:')):
            raw_output.append(parse_item(headers, line, 'route', flags))
            continue

        if interface_table:
            raw_output.append(parse_item(headers, line, 'interface', flags))
            continue

    return parse_post(raw_output)
