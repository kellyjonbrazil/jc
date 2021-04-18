"""jc - JSON CLI output utility `route` command output parser

Usage (cli):

    $ route | jc --route

    or

    $ jc route

Usage (module):

    import jc.parsers.route
    result = jc.parsers.route.parse(route_command_output)

Schema:

    [
      {
        "destination":     string,
        "gateway":         string,
        "genmask":         string,
        "flags":           string,
        "flags_pretty": [
                           string,
        ]
        "metric":          integer,
        "ref":             integer,
        "use":             integer,
        "mss":             integer,
        "window":          integer,
        "irtt":            integer,
        "iface":           string
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
    version = '1.6'
    description = '`route` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['route']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        int_list = ['metric', 'ref', 'use', 'mss', 'window', 'irtt']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        # add flags_pretty
        # Flag mapping from https://www.man7.org/linux/man-pages/man8/route.8.html
        if 'flags' in entry:
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

            pretty_flags = []

            for flag in entry['flags']:
                if flag in flag_map:
                    pretty_flags.append(flag_map[flag])

            entry['flags_pretty'] = pretty_flags

    return proc_data


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
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    cleandata = data.splitlines()[1:]

    raw_output = []

    if jc.utils.has_data(data):

        # fixup header row for ipv6
        if ' Next Hop ' in cleandata[0]:
            cleandata[0] = cleandata[0].replace(' If', ' Iface')
        cleandata[0] = cleandata[0].replace(' Next Hop ', ' Next_Hop ').replace(' Flag ', ' Flags ').replace(' Met ', ' Metric ')

        cleandata[0] = cleandata[0].lower()
        raw_output = jc.parsers.universal.simple_table_parse(cleandata)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
