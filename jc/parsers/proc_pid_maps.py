r"""jc - JSON Convert `/proc/<pid>/maps` file parser

Usage (cli):

    $ cat /proc/1/maps | jc --proc

or

    $ jc /proc/1/maps

or

    $ cat /proc/1/maps | jc --proc-pid-maps

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_maps_file)

or

    import jc
    result = jc.parse('proc_pid_maps', proc_pid_maps_file)

Schema:

    [
      {
        "start":                          string,
        "end":                            string,
        "perms": [
                                          string
        ],
        "offset":                         string,
        "inode":                          integer,
        "pathname":                       string,
        "maj":                            string,
        "min":                            string
      }
    ]

Examples:

    $ cat /proc/1/maps | jc --proc -p
    [
      {
        "perms": [
          "read",
          "private"
        ],
        "offset": "00000000",
        "inode": 798126,
        "pathname": "/usr/lib/systemd/systemd",
        "start": "55a9e753c000",
        "end": "55a9e7570000",
        "maj": "fd",
        "min": "00"
      },
      {
        "perms": [
          "read",
          "execute",
          "private"
        ],
        "offset": "00034000",
        "inode": 798126,
        "pathname": "/usr/lib/systemd/systemd",
        "start": "55a9e7570000",
        "end": "55a9e763a000",
        "maj": "fd",
        "min": "00"
      },
      ...
    ]

    $ cat /proc/1/maps | jc --proc-pid-maps -p -r
    [
      {
        "address": "55a9e753c000-55a9e7570000",
        "perms": "r--p",
        "offset": "00000000",
        "dev": "fd:00",
        "inode": "798126",
        "pathname": "/usr/lib/systemd/systemd"
      },
      {
        "address": "55a9e7570000-55a9e763a000",
        "perms": "r-xp",
        "offset": "00034000",
        "dev": "fd:00",
        "inode": "798126",
        "pathname": "/usr/lib/systemd/systemd"
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/<pid>/maps` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'inode'}

    perms_map = {
        'r': 'read',
        'w': 'write',
        'x': 'execute',
        's': 'shared',
        'p': 'private',
        '-': None
    }

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = int(entry[key])

        if 'address' in entry:
            start, end = entry['address'].split('-')
            entry['start'] = start
            entry['end'] = end
            del entry['address']

        if 'perms' in entry:
            perms_list = [perms_map[x] for x in entry['perms'] if perms_map[x]]
            entry['perms'] = perms_list

        if 'dev' in entry:
            maj, min = entry['dev'].split(':', maxsplit=1)
            entry['maj'] = maj
            entry['min'] = min
            del entry['dev']

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []

    if jc.utils.has_data(data):

        header = 'address           perms offset  dev   inode      pathname\n'
        data = header + data
        raw_output = simple_table_parse(data.splitlines())

    return raw_output if raw else _process(raw_output)
