"""jc - JSON CLI output utility netstat Parser

Usage:
    Specify --netstat as the first argument if the piped input is coming from netstat

    Supports -lnp netstat options

Limitations:
    Only supports TCP and UDP

Examples:

$ netstat -p | jc --netstat -p
{
  "client": {
    "tcp": {
      "ipv4": [
        {
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
    }
  }
}

$ netstat -lp | jc --netstat -p
{
  "server": {
    "tcp": {
      "ipv4": [
        {
          "local_address": "localhost",
          "local_port": "smtp",
          "foreign_address": "0.0.0.0",
          "foreign_port": "*",
          "state": "LISTEN",
          "pid": 1594,
          "program_name": "master",
          "receive_q": 0,
          "send_q": 0
        },
        {
          "local_address": "0.0.0.0",
          "local_port": "ssh",
          "foreign_address": "0.0.0.0",
          "foreign_port": "*",
          "state": "LISTEN",
          "pid": 21918,
          "program_name": "sshd",
          "receive_q": 0,
          "send_q": 0
        }
      ],
      "ipv6": [
        {
          "local_address": "localhost",
          "local_port": "smtp",
          "foreign_address": "[::]",
          "foreign_port": "*",
          "state": "LISTEN",
          "pid": 1594,
          "program_name": "master",
          "receive_q": 0,
          "send_q": 0
        },
        {
          "local_address": "[::]",
          "local_port": "ssh",
          "foreign_address": "[::]",
          "foreign_port": "*",
          "state": "LISTEN",
          "pid": 21918,
          "program_name": "sshd",
          "receive_q": 0,
          "send_q": 0
        }
      ]
    },
    "udp": {
      "ipv4": [
        {
          "local_address": "0.0.0.0",
          "local_port": "bootpc",
          "foreign_address": "0.0.0.0",
          "foreign_port": "*",
          "pid": 13903,
          "program_name": "dhclient",
          "receive_q": 0,
          "send_q": 0
        },
        {
          "local_address": "localhost",
          "local_port": "323",
          "foreign_address": "0.0.0.0",
          "foreign_port": "*",
          "pid": 30926,
          "program_name": "chronyd",
          "receive_q": 0,
          "send_q": 0
        }
      ],
      "ipv6": [
        {
          "local_address": "localhost",
          "local_port": "323",
          "foreign_address": "[::]",
          "foreign_port": "*",
          "pid": 30926,
          "program_name": "chronyd",
          "receive_q": 0,
          "send_q": 0
        }
      ]
    }
  }
}
"""
import string

output = []


class state():
    section = ''
    session = ''
    network = ''

    client_tcp_ip4 = []
    client_tcp_ip6 = []
    client_udp_ip4 = []
    client_udp_ip6 = []

    server_tcp_ip4 = []
    server_tcp_ip6 = []
    server_udp_ip4 = []
    server_udp_ip6 = []


def parse_line(entry):
    parsed_line = entry.split()
    output_line = {}

    if entry.find('tcp') == 0:
        output_line['session_protocol'] = 'tcp'

        if entry.find('p6') == 2:
            output_line['network_protocol'] = 'ipv6'

        else:
            output_line['network_protocol'] = 'ipv4'

    elif entry.find('udp') == 0:
        output_line['session_protocol'] = 'udp'

        if entry.find('p6') == 2:
            output_line['network_protocol'] = 'ipv6'

        else:
            output_line['network_protocol'] = 'ipv4'

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

    return output
