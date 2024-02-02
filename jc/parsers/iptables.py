"""jc - JSON Convert `iptables` command output parser

Supports `-vLn` and `--line-numbers` for all tables.

Usage (cli):

    $ sudo iptables -L -t nat | jc --iptables

or

    $ jc iptables -L -t nat

Usage (module):

    import jc
    result = jc.parse('iptables', iptables_command_output)

Schema:

    [
      {
        "chain":                string,
        "rules": [
          {
            "num"               integer,
            "pkts":             integer,
            "bytes":            integer,  # converted based on suffix
            "target":           string,   # Null if blank
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
    version = '1.10'
    description = '`iptables` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['iptables']
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
    for entry in proc_data:
        for rule in entry['rules']:
            int_list = ['num', 'pkts']
            for key in rule:
                if key in int_list:
                    rule[key] = jc.utils.convert_to_int(rule[key])

            if 'bytes' in rule:
                rule['bytes'] = jc.utils.convert_size_to_int(rule['bytes'])

            if 'opt' in rule:
                if rule['opt'] == '--':
                    rule['opt'] = None

            if 'target' in rule:
                if rule['target'] == '':
                    rule['target'] = None

    return proc_data


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
                headers = [h for h in ' '.join(line.lower().strip().split()).split() if h]
                headers.append("options")

                continue

            else:
                # sometimes the "target" column is blank. Stuff in a dummy character
                if headers[0] == 'target' and line.startswith(' '):
                    line = '\u2063' + line

                rule = line.split(maxsplit=len(headers) - 1)
                temp_rule = dict(zip(headers, rule))
                if temp_rule:
                    if temp_rule.get('target') == '\u2063':
                        temp_rule['target'] = ''
                    chain['rules'].append(temp_rule)

        if chain:
            raw_output.append(chain)

    return raw_output if raw else _process(raw_output)
