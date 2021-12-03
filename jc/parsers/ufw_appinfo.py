"""jc - JSON CLI output utility `ufw app info [application]` command output parser

Supports individual apps via `ufw app info [application]` and all apps list via `ufw app info all`.

Because `ufw` application definitions allow overlapping ports and port ranges, this parser preserves that behavior, but also provides `normalized` lists and ranges that remove duplicate ports and merge overlapping ranges.

Usage (cli):

    $ ufw app info OpenSSH | jc --ufw-appinfo

    or

    $ jc ufw app info OpenSSH

Usage (module):

    import jc.parsers.ufw_appinfo
    result = jc.parsers.ufw_appinfo.parse(ufw_appinfo_command_output)

Schema:

    [
      {
        "profile":                  string,
        "title":                    string,
        "description":              string,
        "tcp_list": [
                                    integer
        ],
        "tcp_ranges": [
          {
            "start":                integer,      # 'any' is converted to start/end: 0/65535
            "end":                  integer
          }
        ],
        "udp_list": [
                                    integer
        ],
        "udp_ranges": [
          {
            "start":                integer,      # 'any' is converted to start/end: 0/65535
            "end":                  integer
          }
        ],
        "normalized_tcp_list": [
                                    integers      # duplicates and overlapping are removed
        ],
        "normalized_tcp_ranges": [
          {
            "start":                integer,      # 'any' is converted to start/end: 0/65535
            "end":                  integers      # overlapping are merged
          }
        ],
        "normalized_udp_list": [
                                    integers      # duplicates and overlapping are removed
        ],
        "normalized_udp_ranges": [
          {
            "start":                integer,      # 'any' is converted to start/end: 0/65535
            "end":                  integers      # overlapping are merged
          }
        ]
      }
    ]

Examples:

    $ ufw app info MSN | jc --ufw-appinfo -p
    [
      {
        "profile": "MSN",
        "title": "MSN Chat",
        "description": "MSN chat protocol (with file transfer and voice)",
        "tcp_list": [
          1863,
          6901
        ],
        "udp_list": [
          1863,
          6901
        ],
        "tcp_ranges": [
          {
            "start": 6891,
            "end": 6900
          }
        ],
        "normalized_tcp_list": [
          1863,
          6901
        ],
        "normalized_tcp_ranges": [
          {
            "start": 6891,
            "end": 6900
          }
        ],
        "normalized_udp_list": [
          1863,
          6901
        ]
      }
    ]

    $ ufw app info MSN | jc --ufw-appinfo -p -r
    [
      {
        "profile": "MSN",
        "title": "MSN Chat",
        "description": "MSN chat protocol (with file transfer and voice)",
        "tcp_list": [
          "1863",
          "6901"
        ],
        "udp_list": [
          "1863",
          "6901"
        ],
        "tcp_ranges": [
          {
            "start": "6891",
            "end": "6900"
          }
        ]
      }
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`ufw app info [application]` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['ufw app']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for profile in proc_data:
        # convert to ints
        int_list = ['start', 'end']

        if 'tcp_list' in profile:
            profile['tcp_list'] = [int(p) for p in profile['tcp_list']]

        if 'udp_list' in profile:
            profile['udp_list'] = [int(p) for p in profile['udp_list']]

        for protocol in ['tcp', 'udp']:
            if protocol + '_ranges' in profile:
                for i, item in enumerate(profile[protocol + '_ranges']):
                    for key in item:
                        if key in int_list:
                            profile[protocol + '_ranges'][i][key] = int(profile[protocol + '_ranges'][i][key])

        # create normalized port lists and port ranges (remove duplicates and merge ranges)
        # dump ranges into a set of 0 - 65535
        # if items in the port list are in the set, then remove them
        # iterate through the set to find gaps and create new ranges based on them
        for protocol in ['tcp', 'udp']:
            port_set = set()
            if protocol + '_ranges' in profile:
                for item in profile[protocol + '_ranges']:
                    port_set.update(range(item['start'], item['end'] + 1))

            if protocol + '_list' in profile:
                new_port_list = sorted(set([p for p in profile[protocol + '_list'] if p not in port_set]))
                if new_port_list:
                    profile['normalized_' + protocol + '_list'] = new_port_list

            new_port_ranges = []
            state = 'findstart'                 # 'findstart' or 'findend'
            for port in range(0, 65535 + 2):
                if state == 'findstart':
                    port_range_obj = {}
                    if port in port_set:
                        port_range_obj['start'] = port
                        state = 'findend'
                        continue
                if state == 'findend':
                    if port not in port_set:
                        port_range_obj['end'] = port - 1
                        new_port_ranges.append(port_range_obj)
                        state = 'findstart'

            if new_port_ranges:
                profile['normalized_' + protocol + '_ranges'] = new_port_ranges

    return proc_data


def _parse_port_list(data, port_list=None):
    """return a list of port strings"""
    # 1,2,3,4,5,6,7,8,9,10,9,30,80:90,8080:8090
    # overlapping and repeated port numbers are allowed

    if port_list is None:
        port_list = []

    data = data.split(',')
    data_list = [p.strip() for p in data if ':' not in p and 'any' not in p]
    port_list.extend(data_list)

    return port_list


def _parse_port_range(data, range_list=None):
    """return a list of dictionaries"""
    # 1,2,3,4,5,6,7,8,9,10,9,30,80:90,8080:8090
    # overlapping port ranges are allowed

    if range_list is None:
        range_list = []

    data = data.strip().split(',')
    ranges = [p.strip() for p in data if ':' in p]
    range_obj = {}

    if 'any' in data:
        range_list.append(
            {
                'start': 0,
                'end': 65535
            }
        )

    for range_ in ranges:
        range_obj = {
            'start': range_.split(':')[0],
            'end': range_.split(':')[1]
        }
        range_list.append(range_obj)

    return range_list


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []
    item_obj = {}

    if jc.utils.has_data(data):

        ports = False

        for line in filter(None, data.splitlines()):

            if line.startswith('--'):
                if item_obj:
                    raw_output.append(item_obj)
                item_obj = {}
                continue

            if line.startswith('Profile:'):
                item_obj['profile'] = line.split(': ')[1]
                continue

            if line.startswith('Title:'):
                item_obj['title'] = line.split(': ')[1]
                continue

            if line.startswith('Description:'):
                item_obj['description'] = line.split(': ')[1]
                continue

            if line.startswith('Port'):
                ports = True
                continue

            if ports:
                line_list = line.rsplit('/', maxsplit=1)
                if len(line_list) == 2:
                    if line_list[1] == 'tcp':
                        tcp_prot_list = _parse_port_list(line_list[0])
                        if tcp_prot_list:
                            item_obj['tcp_list'] = tcp_prot_list

                        tcp_prot_range = _parse_port_range(line_list[0])
                        if tcp_prot_range:
                            item_obj['tcp_ranges'] = tcp_prot_range

                    elif line_list[1] == 'udp':
                        udp_prot_list = _parse_port_list(line_list[0])
                        if udp_prot_list:
                            item_obj['udp_list'] = udp_prot_list

                        udp_prot_range = _parse_port_range(line_list[0])
                        if udp_prot_range:
                            item_obj['udp_ranges'] = udp_prot_range

                # 'any' case
                else:
                    t_list = []
                    t_range = []
                    u_list = []
                    u_range = []

                    if 'tcp_list' in item_obj:
                        t_list = item_obj['tcp_list']

                    if 'tcp_ranges' in item_obj:
                        t_range = item_obj['tcp_ranges']

                    if 'udp_list' in item_obj:
                        u_list = item_obj['udp_list']

                    if 'udp_ranges' in item_obj:
                        u_range = item_obj['udp_ranges']

                    t_p_list = _parse_port_list(line, t_list)
                    if t_p_list:
                        item_obj['tcp_list'] = t_p_list

                    t_r_list = _parse_port_range(line, t_range)
                    if t_r_list:
                        item_obj['tcp_ranges'] = t_r_list

                    u_p_list = _parse_port_list(line, u_list)
                    if u_p_list:
                        item_obj['udp_list'] = u_p_list

                    u_r_list = _parse_port_range(line, u_range)
                    if u_r_list:
                        item_obj['udp_ranges'] = u_r_list

    if item_obj:
        raw_output.append(item_obj)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
