"""jc - JSON Convert `ss` command output parser

Usage (cli):

    $ ss | jc --ss

or

    $ jc ss

Usage (module):

    import jc
    result = jc.parse('ss', ss_command_output)

Schema:

Information from https://www.cyberciti.biz/files/ss.html used to define
field names

    [
      {
        "netid":                      string,
        "state":                      string,
        "recv_q":                     integer,
        "send_q":                     integer,
        "local_address":              string,
        "local_port":                 string,
        "local_port_num":             integer,
        "peer_address":               string,
        "peer_port":                  string,
        "peer_port_num":              integer,
        "interface":                  string,
        "link_layer"                  string,
        "channel":                    string,
        "path":                       string,
        "pid":                        integer,
        "opts": {
          "process_id": {
            "<process_id>": {
              "user":                 string,
              "file_descriptor":      string
            }
          }
        }
      }
    ]

Examples:

      $ sudo ss -a | jc --ss -p
      [
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "peer_address": "*",
          "channel": "rtnl:kernel"
        },
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "peer_address": "*",
          "pid": 893,
          "channel": "rtnl:systemd-resolve"
        },
        ...
        {
          "netid": "p_raw",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "peer_address": "*",
          "link_layer": "LLDP",
          "interface": "ens33"
        },
        {
          "netid": "u_dgr",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_port": "93066",
          "peer_address": "*",
          "peer_port": "0",
          "path": "/run/user/1000/systemd/notify"
        },
        {
          "netid": "u_seq",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_port": "20699",
          "peer_address": "*",
          "peer_port": "0",
          "path": "/run/udev/control"
        },
        ...
        {
          "netid": "icmp6",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "*",
          "local_port": "ipv6-icmp",
          "peer_address": "*",
          "peer_port": "*",
          "interface": "ens33"
        },
        {
          "netid": "udp",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "127.0.0.53",
          "local_port": "domain",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_address": "127.0.0.53",
          "local_port": "domain",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_address": "0.0.0.0",
          "local_port": "ssh",
          "peer_address": "0.0.0.0",
          "peer_port": "*"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_address": "[::]",
          "local_port": "ssh",
          "peer_address": "[::]",
          "peer_port": "*"
        },
        {
          "netid": "v_str",
          "state": "ESTAB",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "999900439",
          "local_port": "1023",
          "peer_address": "0",
          "peer_port": "976",
          "local_port_num": 1023,
          "peer_port_num": 976
        }
      ]

      $ sudo ss -a | jc --ss -p -r
      [
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "peer_address": "*",
          "channel": "rtnl:kernel"
        },
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "peer_address": "*",
          "pid": "893",
          "channel": "rtnl:systemd-resolve"
        },
        ...
        {
          "netid": "p_raw",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "peer_address": "*",
          "link_layer": "LLDP",
          "interface": "ens33"
        },
        {
          "netid": "u_dgr",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_port": "93066",
          "peer_address": "*",
          "peer_port": "0",
          "path": "/run/user/1000/systemd/notify"
        },
        {
          "netid": "u_seq",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_port": "20699",
          "peer_address": "*",
          "peer_port": "0",
          "path": "/run/udev/control"
        },
        ...
        {
          "netid": "icmp6",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "*",
          "local_port": "ipv6-icmp",
          "peer_address": "*",
          "peer_port": "*",
          "interface": "ens33"
        },
        {
          "netid": "udp",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "127.0.0.53",
          "local_port": "domain",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_address": "127.0.0.53",
          "local_port": "domain",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_address": "0.0.0.0",
          "local_port": "ssh",
          "peer_address": "0.0.0.0",
          "peer_port": "*"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_address": "[::]",
          "local_port": "ssh",
          "peer_address": "[::]",
          "peer_port": "*"
        },
        {
          "netid": "v_str",
          "state": "ESTAB",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "999900439",
          "local_port": "1023",
          "peer_address": "0",
          "peer_port": "976"
        }
      ]
"""
import re
import ast
import string
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = '`ss` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['ss']
    tags = ['command']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    int_list = {'recv_q', 'send_q', 'pid'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        if 'local_port' in entry:
            local_num = jc.utils.convert_to_int(entry['local_port'])
            if local_num is not None and local_num >= 0:
                entry['local_port_num'] = local_num

        if 'peer_port' in entry:
            peer_num = jc.utils.convert_to_int(entry['peer_port'])
            if peer_num is not None and peer_num >= 0:
                entry['peer_port_num'] = peer_num

    return proc_data

def _parse_opts(proc_data):
    """ Process extra options -e, -o, -p

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Structured data dictionary for extra/optional headerless options.
    """
    o_field = proc_data.split(' ')
    opts = {}
    for item in o_field:
        # -e option:
        item = re.sub(
            'uid', 'uid_number',
            re.sub('sk', 'cookie', re.sub('ino', 'inode_number', item)))
        if ":" in item:
            key, val = item.split(':')
            # -o option
            if key == "timer":
                val = val.replace('(', '[').replace(')', ']')
                val = ast.literal_eval(re.sub(r'([a-z0-9\.]+)', '"\\1"', val))
                val = {
                    'timer_name': val[0],
                    'expire_time': val[1],
                    'retrans': val[2]
                }
                opts[key] = val
            # -p option
            if key == "users":
                key = 'process_id'
                val = val.replace('(', '[').replace(')', ']')
                val = ast.literal_eval(re.sub(r'([a-z]+=[0-9]+)', '"\\1"', val))
                data = {}
                for rec in val:
                    params = {}
                    params['user'] = rec[0]
                    for i in [x for x in rec if '=' in x]:
                        k, v = i.split('=')
                        params[k] = v
                    data.update({
                        params['pid']: {
                            'user': params['user'],
                            'file_descriptor': params['fd']
                        }
                    })
                val = data
            opts[key] = val
    return opts

def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    contains_colon = ['nl', 'p_raw', 'raw', 'udp', 'tcp', 'v_str', 'icmp6']
    raw_output = []

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        header_text = cleandata[0].lower()
        header_text = header_text.replace('netidstate', 'netid state')
        header_text = header_text.replace('local address:port', 'local_address local_port')
        header_text = header_text.replace('peer address:port', 'peer_address peer_port')
        header_text = header_text.replace('-', '_')

        header_list = header_text.split()
        extra_opts = False

        for entry in cleandata[1:]:
            output_line = {}
            if entry[0] not in string.whitespace:

                # fix weird ss bug where first two columns have no space between them sometimes
                entry = entry[:5] + '  ' + entry[5:]

                entry_list = re.split(r'[ ]{1,}',entry.strip())

                if len(entry_list) > len(header_list) or extra_opts == True:
                    entry_list = re.split(r'[ ]{2,}',entry.strip())
                    extra_opts = True

                if entry_list[0] in contains_colon and ':' in entry_list[4]:
                    l_field = entry_list[4].rsplit(':', maxsplit=1)
                    l_address = l_field[0]
                    l_port = l_field[1]
                    entry_list[4] = l_address
                    entry_list.insert(5, l_port)

                if entry_list[0] in contains_colon and ':' in entry_list[6]:
                    p_field = entry_list[6].rsplit(':', maxsplit=1)
                    p_address = p_field[0]
                    p_port = p_field[1]
                    entry_list[6] = p_address
                    entry_list.insert(7, p_port)

                if re.search(r'ino:|uid:|sk:|users:|timer:',entry_list[-1]):
                    header_list.append('opts')
                    entry_list[-1] = _parse_opts(entry_list[-1])

            output_line = dict(zip(header_list, entry_list))

            # some post processing to pull out fields: interface, link_layer, path, pid, channel
            # Information from https://www.cyberciti.biz/files/ss.html used to define field names
            if '%' in output_line['local_address']:
                i_field = output_line['local_address'].rsplit('%', maxsplit=1)
                output_line['local_address'] = i_field[0]
                output_line['interface'] = i_field[1]

            if output_line['netid'] == 'nl':
                channel = output_line.pop('local_address')
                channel = channel + ':' + output_line.pop('local_port')
                if '/' in channel:
                    pid = channel.rsplit('/', maxsplit=1)[1]
                    channel = channel.rsplit('/', maxsplit=1)[0]
                    output_line['pid'] = pid

                output_line['channel'] = channel

            if output_line['netid'] == 'p_raw':
                output_line['link_layer'] = output_line.pop('local_address')
                output_line['interface'] = output_line.pop('local_port')

            if output_line['netid'] not in contains_colon:
                output_line['path'] = output_line.pop('local_address')

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
