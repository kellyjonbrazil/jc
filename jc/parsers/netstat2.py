"""jc - JSON CLI output utility netstat Parser

Usage:
    Specify --netstat as the first argument if the piped input is coming from netstat

Limitations:
    -Z option may rarely cause incorrect parsing of the program_name, security_context, and path
       for lines with spaces in the program_name
"""
import string
from jc.utils import *


def process(proc_data):
    '''schema:
    [
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "0.0.0.0:22",
        "foreign_address": "0.0.0.0:*",
        "state": "LISTEN",
        "program_name": "1219/sshd",
        "security_context": "system_u:system_r:sshd_t:s0-s0:c0.c1023           ",
        "refcnt": "2",
        "flags": "ACC",
        "type": "STREAM",
        "inode": "20782",
        "path": "/var/run/NetworkManager/private-dhcp",
        "kind": "network"
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

    # post process to split pid and program name and ip addresses and ports

    return raw_data


def parse(data, raw=False, quiet=False):
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']

    if not quiet:
        compatibility(__name__, compatible)

    cleandata = data.splitlines()
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
