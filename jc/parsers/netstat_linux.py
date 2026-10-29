r"""jc - JSON Convert Linux netstat Parser"""
import string
import re


def normalize_headers(header):
    header = header.lower()
    header = header.replace('local address', 'local_address')
    header = header.replace('foreign address', 'foreign_address')
    # keep the width so column positions still line up with the data rows
    header = header.replace('pid/program name', 'program_name    ')
    header = header.replace('security context', 'security_context')
    header = header.replace('i-node', ' inode')
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


NETWORK_HEADERS = ['proto', 'recv_q', 'send_q', 'local_address', 'foreign_address', 'state']
NETWORK_OPTIONAL = ['user', 'inode', 'program_name', 'timer']
SOCKET_HEADERS = ['proto', 'refcnt', 'flags', 'type', 'state', 'inode']
SOCKET_OPTIONAL = ['program_name']
ROUTE_HEADERS = ['destination', 'gateway', 'genmask', 'route_flags']
ROUTE_OPTIONAL = ['metric', 'route_refs', 'use', 'mss', 'window', 'irtt', 'iface']
INTERFACE_HEADERS = ['iface', 'mtu', 'rx_ok', 'rx_err', 'rx_drp', 'rx_ovr', 'tx_ok', 'tx_err', 'tx_drp', 'tx_ovr']
INTERFACE_OPTIONAL = ['met', 'flg']


def is_header(headers, required, optional, last=None):
    """
    Check that the normalized header words are a full header line: the
    required columns first, then only known optional columns (each once),
    and the last column, if given, at the end.
    """
    if headers[:len(required)] != required:
        return False

    rest = headers[len(required):]
    if last:
        if not rest or rest[-1] != last:
            return False
        rest = rest[:-1]

    return len(set(rest)) == len(rest) and all(word in optional or word.endswith('_context') for word in rest)


def is_network_header(headers):
    return is_header(headers, NETWORK_HEADERS, NETWORK_OPTIONAL)


def is_socket_header(headers):
    return is_header(headers, SOCKET_HEADERS, SOCKET_OPTIONAL, last='path')


def is_route_header(headers):
    return 'iface' in headers and is_header(headers, ROUTE_HEADERS, ROUTE_OPTIONAL)


def is_interface_header(headers):
    return is_header(headers, INTERFACE_HEADERS, INTERFACE_OPTIONAL)


def parse_network(headers, entry, has_user):
    LIST_OF_STATES = [
        "ESTABLISHED", "SYN_SENT", "SYN_RECV", "FIN_WAIT1", "FIN_WAIT2",
        "TIME_WAIT", "CLOSED", "CLOSE_WAIT", "LAST_ACK", "LISTEN", "CLOSING",
        "UNKNOWN", "7"
    ]

    # split entry based on presence of value in "State" column. The first five
    # columns never contain whitespace, so the state, if present, is the sixth
    # word. The PID/Program name column is free text and is not searched.
    words = entry.split(maxsplit=8)
    contains_state = len(words) > 5 and words[5] in LIST_OF_STATES

    # with the "User" and "Inode" columns (-e) the sixth word of a row without a
    # state is the user, so also require the numeric inode in the eighth word
    if contains_state and has_user:
        contains_state = len(words) > 7 and words[7].isdigit()

    split_modifier = 1 if contains_state else 2
    entry = entry.split(maxsplit=len(headers) - split_modifier)

    # Count words in header
    # if len of line is one less than len of header, then insert None in field 5
    if len(entry) == len(headers) - 1:
        entry.insert(5, None)

    output_line = dict(zip(headers, entry))
    output_line['kind'] = 'network'

    return output_line


def socket_columns(header_text):
    """Find the column positions in the header once, not for every row."""
    # get the column # of first letter of "state"
    state_col = header_text.find('state')
    # get the program name column area
    pn_start = header_text.find('program_name')
    pn_end = header_text.find('path') - 1

    return state_col, pn_start, pn_end


FLAGS_RE = re.compile(r'^([^ \t]+[ \t]+[^ \t]+[ \t]+)(\[[^\]]*\])')


def parse_socket(headers, entry, columns):
    state_col, pn_start, pn_end = columns

    # Only the Flags column (the third) is bracketed and has blanks in it.
    # Replace the brackets there, keeping the length so the column positions
    # still match. Brackets in the program name and path are left alone.
    m = FLAGS_RE.match(entry)
    if m:
        flags = m.group(2)
        if flags[1:-1].strip(' ') == '':
            flags = '-' * len(flags)
        else:
            flags = ' ' + flags[1:-1] + ' '
        entry = m.group(1) + flags + entry[m.end():]

    # find program_name column area and substitute whitespace with \u2063 there
    old_pn = ''
    new_pn = ''
    if pn_start >= 0:
        # the padding after the name stays a separator
        old_pn = entry[pn_start:pn_end].rstrip(' ')
        new_pn = re.sub(r'\s', '\u2063', old_pn)
        entry = entry[:pn_start] + new_pn + entry[pn_start + len(old_pn):]

    # check column # to see if state column is populated. Choose the split count
    # before splitting so the spare split does not land inside the path.
    has_state = entry[state_col] not in string.whitespace
    entry_list = entry.split(maxsplit=len(headers) - (1 if has_state else 2))
    if not has_state:
        entry_list.insert(4, None)

    output_line = dict(zip(headers, entry_list))
    output_line['kind'] = 'socket'

    # fix program_name field to restore the original column text
    if 'program_name' in output_line:
        if output_line['program_name']:
            old_d_pn = output_line['program_name']
            new_d_pn = old_d_pn.replace(new_pn, old_pn).replace('\u2063', ' ')
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

        List of Dictionaries. Raw structured data.
    """
    raw_output = []
    network = False
    socket = False
    bluetooth = False
    routing_table = False
    interface_table = False
    headers = None
    has_user = False
    columns = None

    for line in cleandata:

        # each section needs its own full header line
        if line.startswith(('Active Internet', 'Active UNIX', 'Active Bluetooth',
                            'Kernel IP routing table', 'Kernel Interface table')):
            headers = None

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
            new_headers = header_text.split()

            # only a full header line starts a new section header
            if not (is_network_header(new_headers) or is_socket_header(new_headers)):
                continue

            headers = new_headers
            has_user = 'user' in headers
            columns = socket_columns(header_text)
            continue

        if line.startswith('Destination '):
            header_text = normalize_route_headers(line)
            new_headers = header_text.split()

            if not is_route_header(new_headers):
                continue

            headers = new_headers
            has_user = 'user' in headers
            columns = socket_columns(header_text)
            continue

        if line.startswith('Iface '):
            header_text = normalize_interface_headers(line)
            new_headers = header_text.split()

            if not is_interface_header(new_headers):
                continue

            headers = new_headers
            has_user = 'user' in headers
            columns = socket_columns(header_text)
            continue

        # rows before any full header line are skipped
        if headers is None:
            continue

        # parse items
        if network:
            raw_output.append(parse_network(headers, line, has_user))
            continue

        if socket:
            raw_output.append(parse_socket(headers, line, columns))
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
