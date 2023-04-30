"""jc - JSON Convert `ip route` command output parser

Usage (cli):

    $ ip route | jc --ip_route

or

    $ jc ip_route

Usage (module):

    import jc
    result = jc.parse('ip route', ip_route_command_output)

Schema:

    [
      {
        "ip":        string,
        "via":       string,
        "dev":       string,
        "metric":    string,
        "proto":     string,
        "scope":     string,
        "src":       string,
        "via":       string,
        "status":    string
      }
    ]

Examples:

    $ ip route  | jc --ip_route
    [
      {
        "ip": "10.0.2.0/24",
        "dev": "enp0s3",
        "proto": "kernel",
        "scope": "link",
        "src": "10.0.2.15",
        "metric": "100"
        ]
      }
    ]


"""


class info:
    """Provides parser metadata (version, author, etc.)"""
    version = '1.8'
    description = '`ip route` command parser'
    author = 'Julian Jackson'
    author_email = 'jackson.julian55@yahoo.com'
    compatible = ['linux']
    magic_commands = ['ip route']
    tags = ['command']


__version__ = info.version


def parse(data, raw=False, quiet=False):
    if data == '':
        return []
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
    raw_data = data.split("\n")
    lines = data.split("\n")
    index = 0
    place = 0
    inc = 0
    for line in lines:
        temp = line.split(" ")
        for word in temp:
            match word:
                case 'via':
                    y = {'via': temp[place + 1]}
                    place += 1
                    structure.update(y)
                case 'dev':
                    y = {'dev': temp[place + 1]}
                    place += 1
                    structure.update(y)
                case 'metric':
                    y = {'metric': temp[place + 1]}
                    place += 1
                    structure.update(y)
                case 'proto':
                    y = {'proto': temp[place + 1]}
                    place += 1
                    structure.update(y)
                case 'scope':
                    y = {'scope': temp[place + 1]}
                    place += 1
                    structure.update(y)
                case 'src':
                    y = {'src': temp[place + 1]}
                    place += 1
                    structure.update(y)
                case 'status':
                    y = {'status': temp[place + 1]}
                    place += 1
                    structure.update(y)
                case 'default':
                    y = {'ip': 'default'}
                    place += 1
                    structure.update(y)
                case 'linkdown':
                    y = {'status': 'linkdown'}
                    place += 1
                    structure.update(y)
                case _:
                    y = {'ip': temp[0]}
                    place += 1
                    structure.update(y)
        if y.get("ip") != "":
            items.append(structure)
        structure = {}
        place = 0
        index += 1
        inc += 1

    if raw:
        return raw_data
    else:
        return items
