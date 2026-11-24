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

#: Stands in for a space inside a quoted process name while the row is split
#: on whitespace. Restored in _parse_opts. A NUL cannot occur in ss output.
_SPACE_HOLD = '\x00'

#: The whole `users:((...))` block, which may contain spaces inside a quoted
#: process name and so must be taken out before any space-based tokenizing.
#: Applied with _match_first, as is _USERS_RE below.
_USERS_BLOCK_RE = re.compile(r'users:\(\(.*?\)\)(?=\s|$)')

#: The local field of a netlink row, `<proto>:<process name>/<pid>`. The name
#: is read from /proc/<pid>/stat, so it can contain spaces and slashes. The
#: field ends at the last `/<pid>` that is followed by the peer address,
#: which is always `*` for netlink sockets.
_NL_LOCAL_RE = re.compile(r'(nl\s+\S+\s+\d+\s+\d+\s+)([^\s:]+:.*/\d+)(?=\s+\*(?:\s|$))')

#: Netids whose local address can carry a `%<interface>` suffix. Unix socket
#: paths and netlink channels can contain a `%` that is not an interface.
_INTERFACE_NETIDS = {'tcp', 'udp', 'raw', 'icmp6', 'sctp', 'dccp', 'mptcp', 'udplite'}

#: Netids of packet sockets: the local field is `<link layer>:<interface>`
_PACKET_NETIDS = {'p_raw', 'p_dgr'}

#: One `("name",pid=N,fd=M)` record inside a `users:` block. The name is
#: non-greedy up to the quote that precedes `,pid=`, so spaces, colons and
#: parentheses inside it are preserved rather than rewritten. With -T and
#: -Z/-z the fields after the pid are `[tid=N,][proc_ctx=X,]fd=M[,sock_ctx=Y]`.
_USERS_RE = re.compile(r'\("(?P<user>.*?)",pid=(?P<pid>\d+),(?P<fields>[^()"]*)\)')

#: The `fd=M` field among the fields after the pid. SELinux contexts can
#: contain commas, so `fd=` must be followed by `,sock_ctx=` or the end.
_USERS_FD_RE = re.compile(r'(?:^|,)fd=(?P<fd>\d+)(?:,sock_ctx=|$)')

#: Marks a field belonging to the headerless options region added by -e, -o
#: and -p. Used both to recognize that region and to find where it starts.
_OPTS_FIELD_RE = re.compile(r'ino:|uid:|sk:|users:|timer:|cgroup:|v6only:')

#: The `cgroup:` key at the start of a token. Its value is a path of
#: directory names, which can contain spaces and colons.
_CGROUP_KEY_RE = re.compile(r'(?:^| )cgroup:')

#: Tokens that can follow the cgroup path: `v6only:N`, `fwmark:0x...` and the
#: shutdown marker (`<->`, `-->`, `<--` or `---`).
_AFTER_CGROUP_RE = re.compile(r'(?:v6only:\d+|fwmark:0x[0-9a-fA-F]+|[<-]-[>-])\Z')

#: The shutdown marker printed after the -e details.
_SHUTDOWN_RE = re.compile(r'[<-]-[>-]\Z')

#: Keys of the options region that ss prints before the shutdown marker. In
#: one-line mode (-O) other tokens, such as `skmem:` and the -i fields, are
#: printed after the marker.
_BEFORE_SHUTDOWN_KEYS = {'uid', 'ino', 'sk', 'fwmark', 'cgroup', 'v6only', 'users', 'timer', 'process_id'}

#: Keys printed by -e that are renamed to their schema names.
_OPTS_KEY_NAMES = {'uid': 'uid_number', 'ino': 'inode_number', 'sk': 'cookie'}
import string
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.10'
    description = '`ss` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['ss']
    tags = ['command']


__version__ = info.version


def _is_port_number(value):
    """Return True if the port value consists only of ASCII digits."""
    return isinstance(value, str) and re.fullmatch(r'[0-9]+', value) is not None


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

        # only a port written as digits is a number: a service name such as
        # `x11` or `pop3` contains digits but is not a port number
        if 'local_port' in entry and _is_port_number(entry['local_port']):
            local_num = jc.utils.convert_to_int(entry['local_port'])
            if local_num is not None and local_num >= 0:
                entry['local_port_num'] = local_num

        if 'peer_port' in entry and _is_port_number(entry['peer_port']):
            peer_num = jc.utils.convert_to_int(entry['peer_port'])
            if peer_num is not None and peer_num >= 0:
                entry['peer_port_num'] = peer_num

    return proc_data

def _match_first(pattern, opener, text, pos=0):
    """
    Same result as `pattern.search(text, pos)` for a pattern that starts with
    the literal `opener` and then scans lazily for its closing text. Only the
    first `opener` needs to be tried: closing text that would complete a later
    `opener` would also complete the first one.

    Parameters:

        pattern:     (Pattern) compiled regex that starts with `opener`
        opener:      (string)  literal text the pattern starts with
        text:        (string)  text to search
        pos:         (integer) index to start searching from

    Returns:

        Match object or None
    """
    start = text.find(opener, pos)
    return pattern.match(text, start) if start != -1 else None

def _unix_columns(entry, tokens, local_sep, peer_sep):
    """
    Split a unix socket row into its eight main columns, followed by the
    options region when the row has one. The socket name can contain spaces,
    so the row is split at the header's `:` columns when the row lines up
    with them, else around the `<inode> * <peer inode>` tokens.

    Parameters:

        entry:       (string)  row text
        tokens:      (list)    row text split on spaces
        local_sep:   (integer) column of the `:` in `Local Address:Port`
        peer_sep:    (integer) column of the `:` in `Peer Address:Port`

    Returns:

        List of strings, or None if the row does not have the unix layout
    """
    columns = None
    opts = ''

    if (0 < local_sep < peer_sep < len(entry) - 1
            and entry[local_sep] == ' ' and entry[peer_sep] == ' '
            and entry[local_sep - 1] != ' ' and entry[peer_sep - 1] != ' '
            and entry[local_sep + 1] != ' ' and entry[peer_sep + 1] != ' '):
        front = re.split(r'[ ]+', entry[:local_sep].strip(), maxsplit=4)
        local_port, _, peer_address = entry[local_sep + 1:peer_sep].partition(' ')
        peer_address = peer_address.strip()
        peer_port, _, opts = entry[peer_sep + 1:].partition(' ')
        if (len(front) == 5 and peer_address
                and _is_port_number(local_port) and _is_port_number(peer_port)):
            columns = front + [local_port, peer_address, peer_port]

    if columns is None:
        # the name ends before the last `<inode> * <peer inode>` tokens
        for i in range(len(tokens) - 3, 4, -1):
            if (tokens[i + 1] == '*' and _is_port_number(tokens[i])
                    and _is_port_number(tokens[i + 2])):
                columns = tokens[:4] + [' '.join(tokens[4:i]), tokens[i], '*', tokens[i + 2]]
                opts = ' '.join(tokens[i + 3:])
                break

    if columns is None:
        return None

    columns[4] = columns[4].replace(_SPACE_HOLD, ' ')
    opts = ' '.join(re.split(r'[ ]{2,}', opts.strip()))
    if _OPTS_FIELD_RE.search(opts):
        columns.append(opts)

    return columns

def _parse_opts(proc_data):
    """ Process extra options -e, -o, -p

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Structured data dictionary for extra/optional headerless options.
    """
    proc_data = proc_data.replace(_SPACE_HOLD, ' ')
    opts = {}

    # `users:` and `cgroup:` are the fields here that can contain a space,
    # because a process name and a cgroup directory name can. Lift `users:`
    # out before the space split below, which would otherwise tear
    # `users:(("my proc",pid=2,fd=3))` into two tokens and lose the record
    # entirely. ss prints `users:` before `cgroup:`, so a block that starts
    # after `cgroup:` is part of the cgroup path.
    users = _match_first(_USERS_BLOCK_RE, 'users:((', proc_data)
    cgroup = _CGROUP_KEY_RE.search(proc_data)
    if users and cgroup and cgroup.start() < users.start():
        users = None

    if users:
        opts['process_id'] = {}
        block = users.group(0)
        record = _match_first(_USERS_RE, '("', block)
        while record:
            fd = _USERS_FD_RE.search(record.group('fields'))
            if fd:
                opts['process_id'][record.group('pid')] = {
                    'user': record.group('user'),
                    'file_descriptor': fd.group('fd')
                }
            record = _match_first(_USERS_RE, '("', block, record.end())
        proc_data = proc_data[:users.start()] + proc_data[users.end():]

    # The cgroup path runs to the end of the region, apart from the tokens
    # ss prints after it, so text inside of the path is not read as more
    # fields.
    cgroup = _CGROUP_KEY_RE.search(proc_data)
    if cgroup:
        o_field = proc_data[:cgroup.start()].split(' ')
        cgroup_field = proc_data[cgroup.start():].strip(' ').split(' ')
        trailing = []

        # one-line mode: the tokens after the last shutdown marker are not
        # part of the path, unless one of them is a key that ss prints before
        # the marker (then that marker is part of the path).
        marker = len(cgroup_field) - 1
        while marker > 0 and not _SHUTDOWN_RE.match(cgroup_field[marker]):
            if cgroup_field[marker].split(':', 1)[0] in _BEFORE_SHUTDOWN_KEYS:
                marker = 0
            else:
                marker -= 1
        if marker > 0:
            trailing = cgroup_field[:marker:-1]
            del cgroup_field[marker + 1:]

        while len(cgroup_field) > 1 and _AFTER_CGROUP_RE.match(cgroup_field[-1]):
            trailing.append(cgroup_field.pop())
        o_field.append(' '.join(cgroup_field))
        o_field.extend(reversed(trailing))
    else:
        o_field = proc_data.split(' ')

    for item in o_field:
        if ":" in item:
            # maxsplit=1: a process name can contain a colon, and splitting on
            # every one of them raises before the value is ever looked at.
            key, val = item.split(':', maxsplit=1)

            # -e option
            key = _OPTS_KEY_NAMES.get(key, key)

            # -o option
            if key == "timer":
                # the expire time can be empty, as in `timer:(keepalive,,0)`
                timer = val.strip('()').split(',')
                if len(timer) == 3:
                    val = {
                        'timer_name': timer[0],
                        'expire_time': timer[1],
                        'retrans': timer[2]
                    }

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

    contains_colon = ['nl', 'p_raw', 'p_dgr', 'raw', 'udp', 'tcp', 'v_str', 'icmp6']
    raw_output = []
    ONE_OR_MORE_SPACE_PATTERN = r'[ ]{1,}'
    TWO_OR_MORE_SPACES_PATTERN = r'[ ]{2,}'

    # Clear any blank lines
    cleandata = list(filter(None, jc.utils.splitlines(data)))

    if jc.utils.has_data(data):
        header_text = cleandata[0].lower()

        # get the position of Recv-Q since sometimes it doesn't leave enough space
        # to parse. need at least two spaces between main fields to differentiate
        # from opt fields, which are only separated by one space
        recv_q_position = header_text.find('recv-q')

        # the `:` between address and port in the header lines up with the
        # space between a unix socket name and its inode in the rows
        local_sep = header_text.find('local address:port')
        peer_sep = header_text.find('peer address:port')
        if local_sep != -1 and peer_sep != -1 and 0 <= recv_q_position < local_sep:
            # two spaces are added twice to each row before these columns
            local_sep += len('local address') + 4
            peer_sep += len('peer address') + 4
        else:
            local_sep = peer_sep = -1

        header_text = header_text.replace('netidstate', 'netid state')
        header_text = header_text.replace('local address:port', 'local_address local_port')
        header_text = header_text.replace('peer address:port', 'peer_address peer_port')
        header_text = re.sub(r'port *process', 'port', header_text)  # don't support process info today
        header_text = header_text.replace('-', '_')

        header_list = header_text.split()

        for entry in cleandata[1:]:
            output_line = {}
            row_header = list(header_list)
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
                users_here = _match_first(_USERS_BLOCK_RE, 'users:((', entry)
                if users_here:
                    entry = (entry[:users_here.start()]
                             + users_here.group(0).replace(' ', _SPACE_HOLD)
                             + entry[users_here.end():])

                # Same for the netlink local field, `<proto>:<name>/<pid>`: a
                # space in the name would move the pid and the rest of the
                # name into the peer columns.
                nl_local = _NL_LOCAL_RE.match(entry.lstrip())
                if nl_local:
                    entry = (nl_local.group(1)
                             + nl_local.group(2).replace(' ', _SPACE_HOLD)
                             + entry.lstrip()[nl_local.end():])

                entry_list = re.split(ONE_OR_MORE_SPACE_PATTERN, entry.strip())
                main_columns = None

                if header_list[0] == 'netid' and len(entry_list) > 8:
                    if entry_list[0].startswith('u_'):
                        main_columns = _unix_columns(entry, entry_list, local_sep, peer_sep)

                    elif (entry_list[0] in contains_colon and entry_list[0] != 'nl'
                            and ':' in entry_list[4] and ':' in entry_list[5]):
                        # the address columns have no spaces, so the options
                        # region starts at the seventh token, even when a full
                        # column leaves only one space before the next one
                        main_columns = re.split(ONE_OR_MORE_SPACE_PATTERN, entry.strip(), maxsplit=6)
                        main_columns[6] = ' '.join(re.split(TWO_OR_MORE_SPACES_PATTERN, main_columns[6]))

                # each row is split on its own: a row with more fields than
                # the header does not change how the rows after it are split
                if main_columns:
                    entry_list = main_columns
                elif len(entry_list) > len(row_header):
                    entry_list = re.split(TWO_OR_MORE_SPACES_PATTERN, entry.strip())

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

                # packet sockets print only '*' for the peer, without a port
                elif entry_list[0] in _PACKET_NETIDS and 'peer_port' in row_header:
                    row_header.remove('peer_port')

                # The options region is one logical field, but it can itself
                # contain runs of two or more spaces: newer iproute2 pads after
                # the users: block to align the column. The two-or-more split
                # above then scatters the region over several entries, and only
                # the last of them is parsed -- while dict(zip(...)) pairs
                # `opts` with an earlier one, so the caller gets a raw string
                # and the ino/sk/cgroup fields are dropped with no error.
                # Rejoin the tail so the whole region reaches _parse_opts.
                opts_start = (len(row_header) - 1
                              if row_header[-1] == 'opts' else len(row_header))
                if (len(entry_list) > opts_start
                        and _OPTS_FIELD_RE.search(entry_list[opts_start])):
                    entry_list[opts_start:] = [' '.join(entry_list[opts_start:])]

                if _OPTS_FIELD_RE.search(entry_list[-1]):
                    if row_header[-1] != 'opts':
                        row_header.append('opts')
                    entry_list[-1] = _parse_opts(entry_list[-1])

            else:
                # -e, -i and -m print socket details on indented lines below
                # each row. They are not rows and are not parsed.
                continue

            output_line = dict(zip(row_header, entry_list))

            # some post processing to pull out fields: interface, link_layer, path, pid, channel
            # Information from https://www.cyberciti.biz/files/ss.html used to define field names
            if output_line['netid'] in _INTERFACE_NETIDS and '%' in output_line['local_address']:
                i_field = output_line['local_address'].rsplit('%', maxsplit=1)
                output_line['local_address'] = i_field[0]
                output_line['interface'] = i_field[1]

            if output_line['netid'] == 'nl':
                channel = output_line.pop('local_address')
                channel = channel + ':' + output_line.pop('local_port')
                channel = channel.replace(_SPACE_HOLD, ' ')
                if '/' in channel:
                    pid = channel.rsplit('/', maxsplit=1)[1]
                    channel = channel.rsplit('/', maxsplit=1)[0]
                    output_line['pid'] = pid

                output_line['channel'] = channel

            if output_line['netid'] in _PACKET_NETIDS:
                output_line['link_layer'] = output_line.pop('local_address')
                output_line['interface'] = output_line.pop('local_port')

            if output_line['netid'] not in contains_colon:
                output_line['path'] = output_line.pop('local_address')

            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
