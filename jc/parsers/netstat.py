"""jc - JSON CLI output utility netstat Parser

Usage:

    Specify --netstat as the first argument if the piped input is coming from netstat

Compatibility:

    'linux'

Examples:

    $ sudo netstat -apee | jc --netstat -p
    [
      {
        "proto": "tcp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "localhost",
        "foreign_address": "0.0.0.0",
        "state": "LISTEN",
        "user": "systemd-resolve",
        "inode": 26958,
        "program_name": "systemd-resolve",
        "kind": "network",
        "pid": 887,
        "local_port": "domain",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "0.0.0.0",
        "foreign_address": "0.0.0.0",
        "state": "LISTEN",
        "user": "root",
        "inode": 30499,
        "program_name": "sshd",
        "kind": "network",
        "pid": 1186,
        "local_port": "ssh",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "localhost",
        "foreign_address": "localhost",
        "state": "ESTABLISHED",
        "user": "root",
        "inode": 46829,
        "program_name": "sshd: root",
        "kind": "network",
        "pid": 2242,
        "local_port": "ssh",
        "foreign_port": "52186",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4",
        "foreign_port_num": 52186
      },
      {
        "proto": "tcp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "localhost",
        "foreign_address": "localhost",
        "state": "ESTABLISHED",
        "user": "root",
        "inode": 46828,
        "program_name": "ssh",
        "kind": "network",
        "pid": 2241,
        "local_port": "52186",
        "foreign_port": "ssh",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4",
        "local_port_num": 52186
      },
      {
        "proto": "tcp6",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "[::]",
        "foreign_address": "[::]",
        "state": "LISTEN",
        "user": "root",
        "inode": 30510,
        "program_name": "sshd",
        "kind": "network",
        "pid": 1186,
        "local_port": "ssh",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv6"
      },
      {
        "proto": "udp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "localhost",
        "foreign_address": "0.0.0.0",
        "state": null,
        "user": "systemd-resolve",
        "inode": 26957,
        "program_name": "systemd-resolve",
        "kind": "network",
        "pid": 887,
        "local_port": "domain",
        "foreign_port": "*",
        "transport_protocol": "udp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "raw6",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "[::]",
        "foreign_address": "[::]",
        "state": "7",
        "user": "systemd-network",
        "inode": 27001,
        "program_name": "systemd-network",
        "kind": "network",
        "pid": 867,
        "local_port": "ipv6-icmp",
        "foreign_port": "*",
        "transport_protocol": null,
        "network_protocol": "ipv6"
      },
      {
        "proto": "unix",
        "refcnt": 2,
        "flags": null,
        "type": "DGRAM",
        "state": null,
        "inode": 33322,
        "program_name": "systemd",
        "path": "/run/user/1000/systemd/notify",
        "kind": "socket",
        "pid": 1607
      },
      {
        "proto": "unix",
        "refcnt": 2,
        "flags": "ACC",
        "type": "SEQPACKET",
        "state": "LISTENING",
        "inode": 20835,
        "program_name": "init",
        "path": "/run/udev/control",
        "kind": "socket",
        "pid": 1
      },
      ...
    ]

    $ sudo netstat -apee | jc --netstat -p -r
    [
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "localhost",
        "foreign_address": "0.0.0.0",
        "state": "LISTEN",
        "user": "systemd-resolve",
        "inode": "26958",
        "program_name": "systemd-resolve",
        "kind": "network",
        "pid": "887",
        "local_port": "domain",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "0.0.0.0",
        "foreign_address": "0.0.0.0",
        "state": "LISTEN",
        "user": "root",
        "inode": "30499",
        "program_name": "sshd",
        "kind": "network",
        "pid": "1186",
        "local_port": "ssh",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "localhost",
        "foreign_address": "localhost",
        "state": "ESTABLISHED",
        "user": "root",
        "inode": "46829",
        "program_name": "sshd: root",
        "kind": "network",
        "pid": "2242",
        "local_port": "ssh",
        "foreign_port": "52186",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "localhost",
        "foreign_address": "localhost",
        "state": "ESTABLISHED",
        "user": "root",
        "inode": "46828",
        "program_name": "ssh",
        "kind": "network",
        "pid": "2241",
        "local_port": "52186",
        "foreign_port": "ssh",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp6",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "[::]",
        "foreign_address": "[::]",
        "state": "LISTEN",
        "user": "root",
        "inode": "30510",
        "program_name": "sshd",
        "kind": "network",
        "pid": "1186",
        "local_port": "ssh",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv6"
      },
      {
        "proto": "udp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "localhost",
        "foreign_address": "0.0.0.0",
        "state": null,
        "user": "systemd-resolve",
        "inode": "26957",
        "program_name": "systemd-resolve",
        "kind": "network",
        "pid": "887",
        "local_port": "domain",
        "foreign_port": "*",
        "transport_protocol": "udp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "raw6",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "[::]",
        "foreign_address": "[::]",
        "state": "7",
        "user": "systemd-network",
        "inode": "27001",
        "program_name": "systemd-network",
        "kind": "network",
        "pid": "867",
        "local_port": "ipv6-icmp",
        "foreign_port": "*",
        "transport_protocol": null,
        "network_protocol": "ipv6"
      },
      {
        "proto": "unix",
        "refcnt": "2",
        "flags": null,
        "type": "DGRAM",
        "state": null,
        "inode": "33322",
        "program_name": "systemd",
        "path": "/run/user/1000/systemd/notify",
        "kind": "socket",
        "pid": " 1607"
      },
      {
        "proto": "unix",
        "refcnt": "2",
        "flags": "ACC",
        "type": "SEQPACKET",
        "state": "LISTENING",
        "inode": "20835",
        "program_name": "init",
        "path": "/run/udev/control",
        "kind": "socket",
        "pid": " 1"
      },
      ...
    ]
"""
import string
import jc.utils


class info():
    version = '1.2'
    description = 'netstat command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['netstat']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "proto":             string,
            "recv_q":            integer,
            "send_q":            integer,
            "transport_protocol" string,
            "network_protocol":  string,
            "local_address":     string,
            "local_port":        string,
            "local_port_num":    integer,
            "foreign_address":   string,
            "foreign_port":      string,
            "foreign_port_num":  integer,
            "state":             string,
            "program_name":      string,
            "pid":               integer,
            "user":              string,
            "security_context":  string,
            "refcnt":            integer,
            "flags":             string,
            "type":              string,
            "inode":             integer,
            "path":              string,
            "kind":              string
          }
        ]
    """
    for entry in proc_data:
        # integer changes
        int_list = ['recv_q', 'send_q', 'pid', 'refcnt', 'inode']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

        if 'local_port' in entry:
            try:
                entry['local_port_num'] = int(entry['local_port'])
            except (ValueError):
                pass

        if 'foreign_port' in entry:
            try:
                entry['foreign_port_num'] = int(entry['foreign_port'])
            except (ValueError):
                pass

    return proc_data


def normalize_headers(header):
    header = header.lower()
    header = header.replace('local address', 'local_address')
    header = header.replace('foreign address', 'foreign_address')
    header = header.replace('pid/program name', 'program_name')
    header = header.replace('security context', 'security_context')
    header = header.replace('i-node', 'inode')
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
    output_line = {}
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
                if entry['proto'].find('tcp') != -1:
                    entry['transport_protocol'] = 'tcp'
                elif entry['proto'].find('udp') != -1:
                    entry['transport_protocol'] = 'udp'
                else:
                    entry['transport_protocol'] = None

                if entry['proto'].find('6') != -1:
                    entry['network_protocol'] = 'ipv6'
                else:
                    entry['network_protocol'] = 'ipv4'

    return raw_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    cleandata = data.splitlines()
    cleandata = list(filter(None, cleandata))

    raw_output = []
    network = False
    socket = False
    headers = ''
    network_list = []
    socket_list = []

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
            header_text = normalize_headers(line)
            headers = header_text.split()
            continue

        if network:
            network_list.append(parse_network(headers, line))
            continue

        if socket:
            socket_list.append(parse_socket(header_text, headers, line))
            continue

    for item in [network_list, socket_list]:
        for entry in item:
            raw_output.append(entry)

    raw_output = parse_post(raw_output)

    if raw:
        return raw_output
    else:
        return process(raw_output)
