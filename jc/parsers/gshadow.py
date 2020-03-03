"""jc - JSON CLI output utility /etc/gshadow file Parser

Usage:

    specify --gshadow as the first argument if the piped input is coming from /etc/gshadow

Compatibility:

    'linux', 'aix', 'freebsd'

Examples:

    $ cat /etc/gshadow | jc --gshadow -p
    [
      {
        "group_name": "root",
        "password": "*",
        "administrators": [],
        "members": []
      },
      {
        "group_name": "adm",
        "password": "*",
        "administrators": [],
        "members": [
          "syslog",
          "joeuser"
        ]
      },
      ...
    ]

    $ cat /etc/gshadow | jc --gshadow -p -r
    [
      {
        "group_name": "root",
        "password": "*",
        "administrators": [
          ""
        ],
        "members": [
          ""
        ]
      },
      {
        "group_name": "adm",
        "password": "*",
        "administrators": [
          ""
        ],
        "members": [
          "syslog",
          "joeuser"
        ]
      },
      ...
    ]
"""
import jc.utils


class info():
    version = '1.0'
    description = '/etc/gshadow file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd']


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
            "group_name":       string,
            "password":         string,
            "administrators": [
                                string
            ],
            "members": [
                                string
            ]
          }
        ]
    """
    for entry in proc_data:
        if entry['administrators'] == ['']:
            entry['administrators'] = []

        if entry['members'] == ['']:
            entry['members'] = []

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
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if cleandata:
        for entry in cleandata:
            if entry.startswith('#'):
                continue

            output_line = {}
            fields = entry.split(':')

            output_line['group_name'] = fields[0]
            output_line['password'] = fields[1]
            output_line['administrators'] = fields[2].split(',')
            output_line['members'] = fields[3].split(',')

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
