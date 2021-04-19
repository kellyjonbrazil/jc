"""jc - JSON CLI output utility `ipables` command output parser

Supports `-vLn` and `--line-numbers` for all tables.

Usage (cli):

    $ sudo iptables -L -t nat | jc --iptables

    or

    $ jc iptables -L -t nat

Usage (module):

    import jc.parsers.iptables
    result = jc.parsers.iptables.parse(iptables_command_output)

Schema:

    [
      {
        "chain":                string,
        "rules": [
          {
            "num"               integer,
            "pkts":             integer,
            "bytes":            integer,  # converted based on suffix
            "target":           string,
            "prot":             string,
            "opt":              string,   # "--" = Null
            "in":               string,
            "out":              string,
            "source":           string,
            "destination":      string,
            "options":          string
          }
        ]
      }
    ]

Examples:

    $ sudo iptables --line-numbers -v -L -t nat | jc --iptables -p
    [
      {
        "chain": "PREROUTING",
        "rules": [
          {
            "num": 1,
            "pkts": 2183,
            "bytes": 186000,
            "target": "PREROUTING_direct",
            "prot": "all",
            "opt": null,
            "in": "any",
            "out": "any",
            "source": "anywhere",
            "destination": "anywhere"
          },
          {
            "num": 2,
            "pkts": 2183,
            "bytes": 186000,
            "target": "PREROUTING_ZONES_SOURCE",
            "prot": "all",
            "opt": null,
            "in": "any",
            "out": "any",
            "source": "anywhere",
            "destination": "anywhere"
          },
          {
            "num": 3,
            "pkts": 2183,
            "bytes": 186000,
            "target": "PREROUTING_ZONES",
            "prot": "all",
            "opt": null,
            "in": "any",
            "out": "any",
            "source": "anywhere",
            "destination": "anywhere"
          },
          {
            "num": 4,
            "pkts": 0,
            "bytes": 0,
            "target": "DOCKER",
            "prot": "all",
            "opt": null,
            "in": "any",
            "out": "any",
            "source": "anywhere",
            "destination": "anywhere",
            "options": "ADDRTYPE match dst-type LOCAL"
          }
        ]
      },
      ...
    ]

    $ sudo iptables --line-numbers -v -L -t nat | jc --iptables -p -r
    [
      {
        "chain": "PREROUTING",
        "rules": [
          {
            "num": "1",
            "pkts": "2183",
            "bytes": "186K",
            "target": "PREROUTING_direct",
            "prot": "all",
            "opt": "--",
            "in": "any",
            "out": "any",
            "source": "anywhere",
            "destination": "anywhere"
          },
          {
            "num": "2",
            "pkts": "2183",
            "bytes": "186K",
            "target": "PREROUTING_ZONES_SOURCE",
            "prot": "all",
            "opt": "--",
            "in": "any",
            "out": "any",
            "source": "anywhere",
            "destination": "anywhere"
          },
          {
            "num": "3",
            "pkts": "2183",
            "bytes": "186K",
            "target": "PREROUTING_ZONES",
            "prot": "all",
            "opt": "--",
            "in": "any",
            "out": "any",
            "source": "anywhere",
            "destination": "anywhere"
          },
          {
            "num": "4",
            "pkts": "0",
            "bytes": "0",
            "target": "DOCKER",
            "prot": "all",
            "opt": "--",
            "in": "any",
            "out": "any",
            "source": "anywhere",
            "destination": "anywhere",
            "options": "ADDRTYPE match dst-type LOCAL"
          }
        ]
      },
      ...
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.6'
    description = '`iptables` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['iptables']


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
        for rule in entry['rules']:
            int_list = ['num', 'pkts']
            for key in rule:
                if key in int_list:
                    rule[key] = jc.utils.convert_to_int(rule[key])

            if 'bytes' in rule:
                multiplier = 1
                if rule['bytes'][-1] == 'K':
                    multiplier = 10 ** 3
                    rule['bytes'] = rule['bytes'].rstrip('K')
                elif rule['bytes'][-1] == 'M':
                    multiplier = 10 ** 6
                    rule['bytes'] = rule['bytes'].rstrip('M')
                elif rule['bytes'][-1] == 'G':
                    multiplier = 10 ** 9
                    rule['bytes'] = rule['bytes'].rstrip('G')
                elif rule['bytes'][-1] == 'T':
                    multiplier = 10 ** 12
                    rule['bytes'] = rule['bytes'].rstrip('T')
                elif rule['bytes'][-1] == 'P':
                    multiplier = 10 ** 15
                    rule['bytes'] = rule['bytes'].rstrip('P')

                try:
                    bytes_int = jc.utils.convert_to_int(rule['bytes'])
                    rule['bytes'] = bytes_int * multiplier
                except (ValueError):
                    rule['bytes'] = None

            if 'opt' in rule:
                if rule['opt'] == '--':
                    rule['opt'] = None

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

    raw_output = []
    chain = {}
    headers = []

    if jc.utils.has_data(data):

        for line in list(filter(None, data.splitlines())):

            if line.startswith('Chain'):
                if chain:
                    raw_output.append(chain)

                chain = {}
                headers = []

                parsed_line = line.split()

                chain['chain'] = parsed_line[1]
                chain['rules'] = []

                continue

            elif line.startswith('target') or line.find('pkts') == 1 or line.startswith('num'):
                headers = []
                headers = [h for h in ' '.join(line.lower().strip().split()).split() if h]
                headers.append("options")

                continue

            else:
                rule = line.split(maxsplit=len(headers) - 1)
                temp_rule = dict(zip(headers, rule))
                if temp_rule:
                    chain['rules'].append(temp_rule)

        if chain:
            raw_output.append(chain)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
