"""jc - JSON Convert `ip route` command output parser

Usage (cli):

    $ ip route | jc --ip-route

or

    $ jc ip-route

Usage (module):

    import jc
    result = jc.parse('ip_route', ip_route_command_output)

Schema:

    [
      {
        "ip":        string,
        "via":       string,
        "dev":       string,
        "metric":    integer,
        "proto":     string,
        "scope":     string,
        "src":       string,
        "via":       string,
        "status":    string
      }
    ]

Examples:

    $ ip route  | jc --ip-route -p
    [
      {
        "ip": "10.0.2.0/24",
        "dev": "enp0s3",
        "proto": "kernel",
        "scope": "link",
        "src": "10.0.2.15",
        "metric": 100
      }
    ]
"""
from typing import Dict

import jc.utils


class info:
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`ip route` command parser'
    author = 'Julian Jackson'
    author_email = 'jackson.julian55@yahoo.com'
    compatible = ['linux']
    magic_commands = ['ip route']
    tags = ['command']


__version__ = info.version


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Json objects if data is processed and Raw data if raw = true.
    """
    structure = {}
    items = []
    lines = data.splitlines()
    index = 0
    place = 0
    inc = 0

    for line in lines:
        temp = line.split()
        for word in temp:
            if word == 'via':
                y = {'via': temp[place + 1]}
                place += 1
                structure.update(y)
            elif word == 'dev':
                y = {'dev': temp[place + 1]}
                place += 1
                structure.update(y)
            elif word == 'metric':
                if raw:
                    y = {'metric': temp[place + 1]}
                else:
                    y = {'metric': jc.utils.convert_to_int(temp[place+1])}
                place += 1
                structure.update(y)
            elif word == 'proto':
                y = {'proto': temp[place + 1]}
                place += 1
                structure.update(y)
            elif word == 'scope':
                y = {'scope': temp[place + 1]}
                place += 1
                structure.update(y)
            elif word == 'src':
                y = {'src': temp[place + 1]}
                place += 1
                structure.update(y)
            elif word == 'status':
                y = {'status': temp[place + 1]}
                place += 1
                structure.update(y)
            elif word == 'default':
                y = {'ip': 'default'}
                place += 1
                structure.update(y)
            elif word == 'linkdown':
                y = {'status': 'linkdown'}
                place += 1
                structure.update(y)
            else:
                y = {'ip': temp[0]}
                place += 1
                structure.update(y)
        if y.get("ip") != "":
            items.append(structure)
        structure = {}
        place = 0
        index += 1
        inc += 1

    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    if not jc.utils.has_data(data):
        return []

    return items
