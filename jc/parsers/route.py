"""jc - JSON Convert `route` command output parser

Usage (cli):

    $ route | jc --route

or

    $ jc route

Usage (module):

    import jc
    result = jc.parse('route', route_command_output)

Schema:

    [
      {
        "interfaces": [
          {
            "id": string,
            "mac": string,
            "name": string,
          }
        ]
        "destination":        string,
        "gateway":            string,
        "genmask":            string,
        "flags":              string,
        "flags_pretty": [
                              string
        ]
        "metric":             integer,
        "ref":                integer,
        "use":                integer,
        "mss":                integer,
        "window":             integer,
        "irtt":               integer,
        "iface":              string
      }
    ]

Examples:

    $ route -ee | jc --route -p
    [
      {
        "destination": "default",
        "gateway": "_gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": 202,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "flags_pretty": [
          "UP",
          "GATEWAY"
        ]
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": 202,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "flags_pretty": [
          "UP"
        ]
      }
    ]

    $ route -ee | jc --route -p -r
    [
      {
        "destination": "default",
        "gateway": "_gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": "202",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": "202",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      }
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.9'
    description = '`route` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'win32']
    magic_commands = ['route']
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
    int_list = {'metric', 'ref', 'use', 'mss', 'window', 'irtt'}

    flag_map = {
        'U': 'UP',
        'H': 'HOST',
        'G': 'GATEWAY',
        'R': 'REINSTATE',
        'D': 'DYNAMIC',
        'M': 'MODIFIED',
        'A': 'ADDRCONF',
        'C': 'CACHE',
        '!': 'REJECT'
      }

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        if 'interfaces' in entry:
            interfaces = []
            for interface in entry["interfaces"]:
                # 00 ff 58 60 5f 61 -> 00:ff:58:60:5f:61
                interface['mac'] = interface['mac'].replace(' ', ':').replace('.', '')
                interfaces.append(interface)
            entry["interfaces"] = interfaces

        # add flags_pretty
        # Flag mapping from https://www.man7.org/linux/man-pages/man8/route.8.html
        if 'flags' in entry:
            pretty_flags = []

            for flag in entry['flags']:
                if flag in flag_map:
                    pretty_flags.append(flag_map[flag])

            entry['flags_pretty'] = pretty_flags

    return proc_data

def normalize_headers(headers: str):
    # fixup header row for ipv6
    if ' Next Hop ' in headers:
      headers = headers.replace(' If', ' Iface')

    headers = headers.replace(' Next Hop ', ' Next_Hop ')
    headers = headers.replace(' Flag ', ' Flags ')
    headers = headers.replace(' Met ', ' Metric ')
    headers = headers.lower()
    return headers

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
    import jc.utils
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)
    cleandata = data.splitlines()

    raw_output = []

    if jc.utils.has_data(data):
        import jc.parsers.route_windows
        if cleandata[0] in jc.parsers.route_windows.SEPARATORS:
           raw_output = jc.parsers.route_windows.parse(cleandata)
        else:
          cleandata.pop(0)  # Removing "Kernel IP routing table".
          cleandata[0] = normalize_headers(cleandata[0])
          import jc.parsers.universal
          raw_output = jc.parsers.universal.simple_table_parse(cleandata)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
