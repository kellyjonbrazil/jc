"""jc - JSON CLI output utility ipables Parser

Usage:

    Specify --iptables as the first argument if the piped input is coming from iptables

    Supports -vLn and --line-numbers for all tables

Compatibility:

    'linux'

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
    version = '1.2'
    description = 'iptables command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['iptables']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

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
    """
    for entry in proc_data:
        for rule in entry['rules']:
            int_list = ['num', 'pkts']
            for key in int_list:
                if key in rule:
                    try:
                        key_int = int(rule[key])
                        rule[key] = key_int
                    except (ValueError):
                        rule[key] = None

            if 'bytes' in rule:
                multiplier = 1
                if rule['bytes'][-1] == 'K':
                    multiplier = 1000
                    rule['bytes'] = rule['bytes'].rstrip('K')
                elif rule['bytes'][-1] == 'M':
                    multiplier = 1000000
                    rule['bytes'] = rule['bytes'].rstrip('M')
                elif rule['bytes'][-1] == 'G':
                    multiplier = 1000000000
                    rule['bytes'] = rule['bytes'].rstrip('G')
                elif rule['bytes'][-1] == 'T':
                    multiplier = 1000000000000
                    rule['bytes'] = rule['bytes'].rstrip('T')
                elif rule['bytes'][-1] == 'P':
                    multiplier = 1000000000000000
                    rule['bytes'] = rule['bytes'].rstrip('P')

                try:
                    bytes_int = int(rule['bytes'])
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

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    chain = {}
    headers = []

    cleandata = data.splitlines()

    for line in cleandata:

        if line.startswith('Chain'):
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

    raw_output = list(filter(None, raw_output))

    if raw:
        return raw_output
    else:
        return process(raw_output)
