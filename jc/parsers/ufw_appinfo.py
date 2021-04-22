"""jc - JSON CLI output utility `ufw app info [application]` command output parser


Usage (cli):

    $ ufw app info OpenSSH | jc --ufw-appinfo

    or

    $ jc ufw app info OpenSSH

Usage (module):

    import jc.parsers.ufw_appinfo
    result = jc.parsers.ufw_appinfo.parse(ufw_appinfo_command_output)

Schema:

    {
      "profile":            string,
      "title":              string,
      "description":        string,
      "ports": {
        "tcp_list": [
                            integer
        ],
        "tcp_ranges": [
          {
            "start":        integer,        # 'any' is converted to start/end: 0/65535
            "end":          integer
          }
        ],
        "udp_list": [
                            integer
        ],
        "upd_ranges": [
          {
            "start":        integer,        # 'any' is converted to start/end: 0/65535
            "end":          integer
          }
        ]
      }
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

    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool conversions and timestamps

    return proc_data


def _parse_port_list(data, port_list=None):
    """return a list of integers"""
    # 1,2,3,4,5,6,7,8,9,10,9,30,80:90,8080:8090
    # overlapping and repeated port numbers are allowed, so use a set to correct

    if port_list is None:
        port_list = []

    data = data.split(',')
    data_list = [int(p) for p in data if ':' not in p and 'any' not in p]
    port_list.extend(data_list)

    return sorted(list(set(port_list)))


def _parse_port_range(data, range_list=None):
    """return a list of dictionaries"""
    # 1,2,3,4,5,6,7,8,9,10,9,30,80:90,8080:8090
    # overlapping ports are allowed

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
            'start': int(range_.split(':')[0]),
            'end': int(range_.split(':')[1])
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

            if line.startswith('Ports:'):
                ports = True
                ports_obj = {'ports': {}}
                continue

            if ports:
                line_list = line.rsplit('/', maxsplit=1)
                if len(line_list) == 2:
                    if line_list[1] == 'tcp':
                        ports_obj['ports']['tcp_list'] = _parse_port_list(line_list[0])
                        ports_obj['ports']['tcp_ranges'] = _parse_port_range(line_list[0])
                    elif line_list[1] == 'udp':
                        ports_obj['ports']['udp_list'] = _parse_port_list(line_list[0])
                        ports_obj['ports']['udp_ranges'] = _parse_port_range(line_list[0])

                # 'any' case
                else:
                    t_list = []
                    t_range = []
                    u_list = []
                    u_range = []

                    if 'tcp_list' in ports_obj['ports']:
                        t_list = ports_obj['ports']['tcp_list']

                    if 'tcp_ranges' in ports_obj['ports']:
                        t_range = ports_obj['ports']['tcp_ranges']

                    if 'udp_list' in ports_obj['ports']:
                        u_list = ports_obj['ports']['udp_list']

                    if 'udp_ranges' in ports_obj['ports']:
                        u_range = ports_obj['ports']['udp_ranges']

                    ports_obj['ports']['tcp_list'] = _parse_port_list(line, t_list)
                    ports_obj['ports']['tcp_ranges'] = _parse_port_range(line, t_range)
                    ports_obj['ports']['udp_list'] = _parse_port_list(line, u_list)
                    ports_obj['ports']['udp_ranges'] = _parse_port_range(line, u_range)

        raw_output.update(ports_obj)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
