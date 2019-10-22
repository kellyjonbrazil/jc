"""jc - JSON CLI output utility netstat Parser

Usage:
    Specify --netstat as the first argument if the piped input is coming from netstat

    Supports -lnp netstat options

Limitations:
    Only supports TCP and UDP

Examples:

$ netstat -p | jc --netstat -p
[
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "localhost.localdo",
    "local_port": "34480",
    "foreign_address": "lb-192-30-255-113",
    "foreign_port": "https",
    "state": "ESTABLISHED",
    "pid": 53550,
    "program_name": "git-remote-ht",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "localhost.localdo",
    "local_port": "34478",
    "foreign_address": "lb-192-30-255-113",
    "foreign_port": "https",
    "state": "ESTABLISHED",
    "pid": 53550,
    "program_name": "git-remote-ht",
    "receive_q": 0,
    "send_q": 0
  }
]

$ netstat -lpn | jc --netstat -p
[
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "127.0.0.1",
    "local_port": "42351",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": 1112,
    "program_name": "containerd",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "127.0.0.53",
    "local_port": "53",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": 885,
    "program_name": "systemd-resolve",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "0.0.0.0",
    "local_port": "22",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": 1127,
    "program_name": "sshd",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv6",
    "local_address": "::",
    "local_port": "22",
    "foreign_address": "::",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": 1127,
    "program_name": "sshd",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "udp",
    "network_protocol": "ipv4",
    "local_address": "127.0.0.53",
    "local_port": "53",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "pid": 885,
    "program_name": "systemd-resolve",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "udp",
    "network_protocol": "ipv4",
    "local_address": "192.168.71.131",
    "local_port": "68",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "pid": 867,
    "program_name": "systemd-network",
    "receive_q": 0,
    "send_q": 0
  }
]
"""
import string

output = []


def parse_line(entry):
    output_line = {}

    if entry.find('tcp') == 0:
        output_line['transport_protocol'] = 'tcp'

        if entry.find('p6') == 2:
            output_line['network_protocol'] = 'ipv6'

        else:
            output_line['network_protocol'] = 'ipv4'

    elif entry.find('udp') == 0:
        output_line['transport_protocol'] = 'udp'

        if entry.find('p6') == 2:
            output_line['network_protocol'] = 'ipv6'

        else:
            output_line['network_protocol'] = 'ipv4'
    else:
        return

    parsed_line = entry.split()

    output_line['local_address'] = parsed_line[3].rsplit(':', 1)[0]
    output_line['local_port'] = parsed_line[3].rsplit(':', 1)[-1]
    output_line['foreign_address'] = parsed_line[4].rsplit(':', 1)[0]
    output_line['foreign_port'] = parsed_line[4].rsplit(':', 1)[-1]

    if len(parsed_line) > 5:

        if parsed_line[5][0] not in string.digits and parsed_line[5][0] != '-':
            output_line['state'] = parsed_line[5]

            if len(parsed_line) > 6 and parsed_line[6][0] in string.digits:
                output_line['pid'] = int(parsed_line[6].split('/')[0])
                output_line['program_name'] = parsed_line[6].split('/')[1]
        else:
            if parsed_line[5][0] in string.digits:
                output_line['pid'] = int(parsed_line[5].split('/')[0])
                output_line['program_name'] = parsed_line[5].split('/')[1]

    output_line['receive_q'] = int(parsed_line[1])
    output_line['send_q'] = int(parsed_line[2])

    return output_line


def parse(data):
    cleandata = data.splitlines()

    for line in cleandata:

        if line.find('Active Internet connections (w/o servers)') == 0:
            continue

        if line.find('Active Internet connections (only servers)') == 0:
            continue

        if line.find('Proto') == 0:
            continue

        if line.find('Active UNIX') == 0:
            break

        output.append(parse_line(line))

    clean_output = list(filter(None, output))
    return clean_output
