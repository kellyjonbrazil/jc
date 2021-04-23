"""jc - JSON CLI output utility `ufw app info [application]` command output parser

Because `ufw` application definitions allow overlapping ports and port ranges, this parser preserves that behavior, but also provides `normalized` lists and ranges that remove duplicate ports and merge overlapping ranges.

Usage (cli):

    $ ufw app info OpenSSH | jc --ufw-appinfo

    or

    $ jc ufw app info OpenSSH

Usage (module):

    import jc.parsers.ufw_appinfo
    result = jc.parsers.ufw_appinfo.parse(ufw_appinfo_command_output)

Schema:

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

Examples:

    $ ufw app info OpenSSH | jc --ufw-appinfo -p
    []

    $ ufw app info OpenSSH | jc --ufw-appinfo -p -r
    []
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`ufw app info [application]` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['ufw-appinfo']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    # convert to ints
    int_list = ['start', 'end']

    if 'tcp_list' in proc_data:
        proc_data['tcp_list'] = [int(p) for p in proc_data['tcp_list']]

    if 'udp_list' in proc_data:
        proc_data['udp_list'] = [int(p) for p in proc_data['udp_list']]

    for protocol in ['tcp', 'udp']:
        if protocol + '_ranges' in proc_data:
            for i, item in enumerate(proc_data[protocol + '_ranges']):
                for key in item:
                    if key in int_list:
                        proc_data[protocol + '_ranges'][i][key] = int(proc_data[protocol + '_ranges'][i][key])

    # create normalized port lists and port ranges (remove duplicates and merge ranges)
    # dump ranges into a set of 0 - 65535
    # if items in the port list are in the set, then remove them
    # iterate through the set to find gaps and create new ranges based on them
    for protocol in ['tcp', 'udp']:
        port_set = set()
        if protocol + '_ranges' in proc_data:
            for item in proc_data[protocol + '_ranges']:
                port_set.update(range(item['start'], item['end'] + 1))

        if protocol + '_list' in proc_data:
            proc_data['normalized_' + protocol + '_list'] = sorted(set([p for p in proc_data[protocol + '_list'] if p not in port_set]))

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
            proc_data['normalized_' + protocol + '_ranges'] = new_port_ranges

    return proc_data


def _parse_port_list(data, port_list=None):
    """return a list of integers"""
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

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):

        ports = False

        for line in filter(None, data.splitlines()):

            if line.startswith('Profile:'):
                raw_output['profile'] = line.split(': ')[1]
                continue

            if line.startswith('Title:'):
                raw_output['title'] = line.split(': ')[1]
                continue

            if line.startswith('Description:'):
                raw_output['description'] = line.split(': ')[1]
                continue

            if line.startswith('Port'):
                ports = True
                continue

            if ports:
                line_list = line.rsplit('/', maxsplit=1)
                if len(line_list) == 2:
                    if line_list[1] == 'tcp':
                        prot_list = _parse_port_list(line_list[0])
                        if prot_list:
                            raw_output['tcp_list'] = prot_list

                        prot_range = _parse_port_range(line_list[0])
                        if prot_range:
                            raw_output['tcp_ranges'] = prot_range

                    elif line_list[1] == 'udp':
                        prot_list = _parse_port_list(line_list[0])
                        if prot_list:
                            raw_output['udp_list'] = prot_list

                        prot_range = _parse_port_range(line_list[0])
                        if prot_range:
                            raw_output['udp_ranges'] = prot_range

                # 'any' case
                else:
                    t_list = []
                    t_range = []
                    u_list = []
                    u_range = []

                    if 'tcp_list' in raw_output:
                        t_list = raw_output['tcp_list']

                    if 'tcp_ranges' in raw_output:
                        t_range = raw_output['tcp_ranges']

                    if 'udp_list' in raw_output:
                        u_list = raw_output['udp_list']

                    if 'udp_ranges' in raw_output:
                        u_range = raw_output['udp_ranges']

                    raw_output['tcp_list'] = _parse_port_list(line, t_list)
                    raw_output['tcp_ranges'] = _parse_port_range(line, t_range)
                    raw_output['udp_list'] = _parse_port_list(line, u_list)
                    raw_output['udp_ranges'] = _parse_port_range(line, u_range)

        raw_output.update(raw_output)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
