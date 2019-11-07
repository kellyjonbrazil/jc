"""jc - JSON CLI output utility netstat Parser

Usage:
    Specify --netstat as the first argument if the piped input is coming from netstat

Limitations:
    incorrect parsing can occur when there is a space in the program_name field when using the -p option in netstat
"""
import string
import jc.utils


def process(proc_data):
    '''schema:
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
        "security_context":  string,           ",
        "refcnt":            integer,
        "flags":             string,
        "type":              stromg,
        "inode":             integer,
        "path":              string,
        "kind":              string
      }
    ]
    '''
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
    # get the column # of first letter of "state"
    # for each line check column # to see if state column is populated
    # remove [ and ] from each line
    output_line = {}
    state_col = header_text.find('state')

    entry = entry.replace('[ ]', '---')
    entry = entry.replace('[', ' ').replace(']', ' ')
    entry_list = entry.split(maxsplit=len(headers) - 1)
    if entry[state_col] in string.whitespace:
        entry_list.insert(4, None)

    output_line = dict(zip(headers, entry_list))
    output_line['kind'] = 'socket'

    return output_line


def parse_post(raw_data):
    # flags --- = null
    # post process to split pid and program name and ip addresses and ports

    for entry in raw_data:
        if 'flags' in entry:
            if entry['flags'] == '---':
                entry['flags'] = None
        if 'program_name' in entry:
            entry['program_name'] = entry['program_name'].rstrip()
            if entry['program_name'] == '-':
                entry['program_name'] = None

    return raw_data


def parse(data, raw=False, quiet=False):
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    cleandata = data.splitlines()
    cleandata = list(filter(None, cleandata))

    raw_output = []

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
