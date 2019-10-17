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

output = {}

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

    output_line['local_address'] = parsed_line[3].rsplit(':', 1)[0]
    output_line['local_port'] = parsed_line[3].rsplit(':', 1)[-1]
    output_line['foreign_address'] = parsed_line[4].rsplit(':', 1)[0]
    output_line['foreign_port'] = parsed_line[4].rsplit(':', 1)[-1]

    if len(parsed_line) > 5:

        if parsed_line[5][0] not in string.digits:
            output_line['state'] = parsed_line[5]
            
            if len(parsed_line) > 6:
                output_line['pid'] = int(parsed_line[6].split('/')[0])
                output_line['program_name'] = parsed_line[6].split('/')[1]
        else:
            output_line['pid'] = int(parsed_line[5].split('/')[0])
            output_line['program_name'] = parsed_line[5].split('/')[1]

    output_line['receive_q'] = int(parsed_line[1])
    output_line['send_q'] = int(parsed_line[2])

    return output_line

def parse(data):
    cleandata = data.splitlines()

    for line in cleandata:

        if line.find('Active Internet connections (w/o servers)') == 0:
            state.section = "client"
            continue

        if line.find('Active Internet connections (only servers)') == 0:
            state.section = "server"
            continue
        
        if line.find('Proto') == 0:
            continue

        if line.find('Active UNIX') == 0:
            break
        
        if state.section == 'client':
            if line.find('tcp') == 0:
                state.session = 'tcp'
                if line.find('p6') == 2:
                    state.network = 'ipv6'
                else:
                    state.network = 'ipv4'
            elif line.find('udp') == 0:
                state.session = 'udp'
                if line.find('p6') == 2:
                    state.network = 'ipv6'
                else:
                    state.network = 'ipv4'
        elif state.section == 'server':
            if line.find('tcp') == 0:
                state.session = 'tcp'
                if line.find('p6') == 2:
                    state.network = 'ipv6'
                else:
                    state.network = 'ipv4'
            elif line.find('udp') == 0:
                state.session = 'udp'
                if line.find('p6') == 2:
                    state.network = 'ipv6'
                else:
                    state.network = 'ipv4'

        if state.section == 'client' and state.session == 'tcp' and state.network == 'ipv4':
            state.client_tcp_ip4.append(parse_line(line))

        if state.section == 'client' and state.session == 'tcp' and state.network == 'ipv6':
            state.client_tcp_ip6.append(parse_line(line))

        if state.section == 'client' and state.session == 'udp' and state.network == 'ipv4':
            state.client_udp_ip4.append(parse_line(line))

        if state.section == 'client' and state.session == 'udp' and state.network == 'ipv6':
            state.client_udp_ip6.append(parse_line(line))


        if state.section == 'server' and state.session == 'tcp' and state.network == 'ipv4':
            state.server_tcp_ip4.append(parse_line(line))

        if state.section == 'server' and state.session == 'tcp' and state.network == 'ipv6':
            state.server_tcp_ip6.append(parse_line(line))

        if state.section == 'server' and state.session == 'udp' and state.network == 'ipv4':
            state.server_udp_ip4.append(parse_line(line))

        if state.section == 'server' and state.session == 'udp' and state.network == 'ipv6':
            state.server_udp_ip6.append(parse_line(line))

        state.session = ''
        state.network = ''

    # build dictionary
    if state.client_tcp_ip4:
        if 'client' not in output:
            output['client'] = {}
        if 'tcp' not in output['client']:
            output['client']['tcp'] = {}
        output['client']['tcp']['ipv4'] = state.client_tcp_ip4

    if state.client_tcp_ip6:
        if 'client' not in output:
            output['client'] = {}
        if 'tcp' not in output['client']:
            output['client']['tcp'] = {}
        output['client']['tcp']['ipv6'] = state.client_tcp_ip6

    if state.client_udp_ip4:
        if 'client' not in output:
            output['client'] = {}
        if 'udp' not in output['client']:
            output['client']['udp'] = {}
        output['client']['udp']['ipv4'] = state.client_udp_ip4

    if state.client_udp_ip6:
        if 'client' not in output:
            output['client'] = {}
        if 'udp' not in output['client']:
            output['client']['udp'] = {}
        output['client']['udp']['ipv6'] = state.client_udp_ip6
    
    
    if state.server_tcp_ip4:
        if 'server' not in output:
            output['server'] = {}
        if 'tcp' not in output['server']:
            output['server']['tcp'] = {}
        output['server']['tcp']['ipv4'] = state.server_tcp_ip4

    if state.server_tcp_ip6:
        if 'server' not in output:
            output['server'] = {}
        if 'tcp' not in output['server']:
            output['server']['tcp'] = {}
        output['server']['tcp']['ipv6'] = state.server_tcp_ip6

    if state.server_udp_ip4:
        if 'server' not in output:
            output['server'] = {}
        if 'udp' not in output['server']:
            output['server']['udp'] = {}
        output['server']['udp']['ipv4'] = state.server_udp_ip4
    
    if state.server_udp_ip6:
        if 'server' not in output:
            output['server'] = {}
        if 'udp' not in output['server']:
            output['server']['udp'] = {}
        output['server']['udp']['ipv6'] = state.server_udp_ip6

    return output