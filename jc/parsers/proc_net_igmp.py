"""jc - JSON Convert `/proc/net/igmp` file parser

Usage (cli):

    $ cat /proc/net/igmp | jc --proc

or

    $ jc /proc/net/igmp

or

    $ cat /proc/net/igmp | jc --proc-net-igmp

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_igmp_file)

or

    import jc
    result = jc.parse('proc_net_igmp', proc_net_igmp_file)

Schema:

    [
      {
        "index":                      integer,
        "device":                     string,
        "count":                      integer,
        "querier":                    string,
        "groups": [
          {
            "address":                string,
            "users":                  integer,
            "timer":                  string,
            "reporter":               integer
          }
        ]
      }
    ]

Examples:

    $ cat /proc/net/igmp | jc --proc -p
    [
      {
        "index": 0,
        "device": "lo",
        "count": 0,
        "querier": "V3",
        "groups": [
          {
            "address": "010000E0",
            "users": 1,
            "timer": "0:00000000",
            "reporter": 0
          }
        ]
      },
      {
        "index": 2,
        "device": "eth0",
        "count": 26,
        "querier": "V2",
        "groups": [
          {
            "address": "260301E0",
            "users": 1,
            "timer": "0:00000000",
            "reporter": 1
          },
          {
            "address": "9B0101E0",
            "users": 1,
            "timer": "0:00000000",
            "reporter": 1
          },
        ]
      }
      ...
    ]

    $ cat /proc/net/igmp | jc --proc-net-igmp -p -r
    [
      {
        "index": "0",
        "device": "lo",
        "count": "0",
        "querier": "V3",
        "groups": [
          {
            "address": "010000E0",
            "users": "1",
            "timer": "0:00000000",
            "reporter": "0"
          }
        ]
      },
      {
        "index": "2",
        "device": "eth0",
        "count": "26",
        "querier": "V2",
        "groups": [
          {
            "address": "260301E0",
            "users": "1",
            "timer": "0:00000000",
            "reporter": "1"
          },
          {
            "address": "9B0101E0",
            "users": "1",
            "timer": "0:00000000",
            "reporter": "1"
          },
        ]
      }
      ...
    }
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/igmp` file parser'
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
    int_list = {'index', 'count', 'users', 'reporter'}

    for item in proc_data:
        for key, val in item.items():
            if key in int_list:
                item[key] = int(val)

        if 'groups' in item:
            for group in item['groups']:
                for key, val in group.items():
                    if key in int_list:
                        group[key] = int(val)

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
    output_line: Dict = {}
    groups: List = []
    group: Dict = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()[1:]):
            if not line.startswith('\t'):
                if output_line:
                    if groups:
                        output_line['groups'] = groups
                    raw_output.append(output_line)
                    output_line = {}
                    groups = []
                    group = {}

                index, device, _, count, querier = line.split()
                output_line = {
                    'index': index,
                    'device': device,
                    'count': count,
                    'querier': querier
                }
                continue

            address, users, timer, reporter = line.split()
            group = {
                'address': address,
                'users': users,
                'timer': timer,
                'reporter': reporter
            }
            groups.append(group)
            continue

        if output_line:
            if groups:
                output_line['groups'] = groups
            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
