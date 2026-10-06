r"""jc - JSON Convert `ss` command output parser

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
          },
          "timer": {
            "timer_name":             string,
            "expire_time":            string,
            "retrans":                string
          },
          "inode_number":             string,
          "cookie":                   string,
          "cgroup":                   string,
          "v6only":                   string,
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

#: Stands in for a space inside a quoted process name while the row is split
#: on whitespace. Restored in _parse_opts. A NUL cannot occur in ss output.
_SPACE_HOLD = '\x00'

#: The whole `users:((...))` block, which may contain spaces inside a quoted
#: process name and so must be taken out before any space-based tokenizing.
_USERS_BLOCK_RE = re.compile(r'users:\(\(.*?\)\)(?=\s|$)')

#: One `("name",pid=N,fd=M)` record inside a `users:` block. The name is
#: non-greedy up to the quote that precedes `,pid=`, so spaces, colons and
#: parentheses inside it are preserved rather than rewritten.
_USERS_RE = re.compile(r'\("(?P<user>.*?)",pid=(?P<pid>\d+),fd=(?P<fd>\d+)\)')

#: Marks a field belonging to the headerless options region added by -e, -o
#: and -p. Used both to recognize that region and to find where it starts.
_OPTS_FIELD_RE = re.compile(r'ino:|uid:|sk:|users:|timer:|cgroup:|v6only:')
import string
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.9'
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
    proc_data = proc_data.replace(_SPACE_HOLD, ' ')
    opts = {}

    # `users:` is the only field here that can contain a space, because a
    # process name can. Lift it out before the naive space split below, which
    # would otherwise tear `users:(("my proc",pid=2,fd=3))` into two tokens and
    # lose the record entirely.
    users = _USERS_BLOCK_RE.search(proc_data)
    if users:
        opts['process_id'] = {
            pid: {'user': user, 'file_descriptor': fd}
            for user, pid, fd in _USERS_RE.findall(users.group(0))
        }
        proc_data = proc_data[:users.start()] + proc_data[users.end():]

    o_field = proc_data.split(' ')

    for item in o_field:
        # -e option:
        item = re.sub(
            'uid', 'uid_number',
            re.sub('sk', 'cookie', re.sub('ino', 'inode_number', item)))

        if ":" in item:
            # maxsplit=1: a process name can contain a colon, and splitting on
            # every one of them raises before the value is ever looked at.
            key, val = item.split(':', maxsplit=1)

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
    ONE_OR_MORE_SPACE_PATTERN = r'[ ]{1,}'
    TWO_OR_MORE_SPACES_PATTERN = r'[ ]{2,}'

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):
        header_text = cleandata[0].lower()

        # get the position of Recv-Q since sometimes it doesn't leave enough space
        # to parse. need at least two spaces between main fields to differentiate
        # from opt fields, which are only separated by one space
        recv_q_position = header_text.find('recv-q')

        header_text = header_text.replace('netidstate', 'netid state')
        header_text = header_text.replace('local address:port', 'local_address local_port')
        header_text = header_text.replace('peer address:port', 'peer_address peer_port')
        header_text = header_text.replace('portprocess', 'port')  # don't support process info today
        header_text = header_text.replace('-', '_')

        header_list = header_text.split()
        extra_opts = False

        for entry in cleandata[1:]:
            output_line = {}
            if entry[0] not in string.whitespace:
                # fix issue where recv-q can be too close to state
                entry = entry[:recv_q_position] + '  ' + entry[recv_q_position:]

                # fix weird ss bug where first two columns have no space between them sometimes
                entry = entry[:5] + '  ' + entry[5:]

                # A process name may contain spaces, and both splits below are
                # space-based, so the users: block is shielded first and put
                # back in _parse_opts. Without this the row splits mid-name and
                # dict(zip(...)) silently drops the overflow: the opts column
                # ends up holding the truncated `users:(("my` and the pid and
                # fd are lost with no error anywhere.
                users_here = _USERS_BLOCK_RE.search(entry)
                if users_here:
                    entry = (entry[:users_here.start()]
                             + users_here.group(0).replace(' ', _SPACE_HOLD)
                             + entry[users_here.end():])

                entry_list = re.split(ONE_OR_MORE_SPACE_PATTERN, entry.strip())

                if len(entry_list) > len(header_list) or extra_opts == True:
                    entry_list = re.split(TWO_OR_MORE_SPACES_PATTERN, entry.strip())
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

                # The options region is one logical field, but it can itself
                # contain runs of two or more spaces: newer iproute2 pads after
                # the users: block to align the column. The two-or-more split
                # above then scatters the region over several entries, and only
                # the last of them is parsed -- while dict(zip(...)) pairs
                # `opts` with an earlier one, so the caller gets a raw string
                # and the ino/sk/cgroup fields are dropped with no error.
                # Rejoin the tail so the whole region reaches _parse_opts.
                opts_start = (len(header_list) - 1
                              if header_list[-1] == 'opts' else len(header_list))
                if (len(entry_list) > opts_start
                        and _OPTS_FIELD_RE.search(entry_list[opts_start])):
                    entry_list[opts_start:] = [' '.join(entry_list[opts_start:])]

                if _OPTS_FIELD_RE.search(entry_list[-1]):
                    if header_list[-1] != 'opts':
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

    return raw_output if raw else _process(raw_output)
