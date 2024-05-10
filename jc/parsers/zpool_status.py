r"""jc - JSON Convert `zpool status` command output parser

Works with or without the `-v` option.

Usage (cli):

    $ zpool status | jc --zpool-status

or

    $ jc zpool status

Usage (module):

    import jc
    result = jc.parse('zpool_status', zpool_status_command_output)

Schema:

    [
      {
        "pool":                               string,
        "state":                              string,
        "status":                             string,
        "action":                             string,
        "see":                                string,
        "scan":                               string,
        "scrub":                              string,
        "config": [
          {
            "name":                           string,
            "state":                          string/null,
            "read":                           integer/null,
            "write":                          integer/null,
            "checksum":                       integer/null,
            "errors":                         string/null,
          }
        ],
        "errors":                             string
      }
    ]

Examples:

    $ zpool status -v | jc --zpool-status -p
    [
      {
        "pool": "tank",
        "state": "DEGRADED",
        "status": "One or more devices could not be opened.  Suffic...",
        "action": "Attach the missing device and online it using 'zpool...",
        "see": "http://www.sun.com/msg/ZFS-8000-2Q",
        "scrub": "none requested",
        "config": [
          {
            "name": "tank",
            "state": "DEGRADED",
            "read": 0,
            "write": 0,
            "checksum": 0
          },
          {
            "name": "mirror-0",
            "state": "DEGRADED",
            "read": 0,
            "write": 0,
            "checksum": 0
          },
          {
            "name": "c1t0d0",
            "state": "ONLINE",
            "read": 0,
            "write": 0,
            "checksum": 0
          },
          {
            "name": "c1t1d0",
            "state": "UNAVAIL",
            "read": 0,
            "write": 0,
            "checksum": 0,
            "errors": "cannot open"
          }
        ],
        "errors": "No known data errors"
      }
    ]

    $ zpool status -v | jc --zpool-status -p -r
    [
      {
        "pool": "tank",
        "state": "DEGRADED",
        "status": "One or more devices could not be opened.  Sufficient...",
        "action": "Attach the missing device and online it using 'zpool...",
        "see": "http://www.sun.com/msg/ZFS-8000-2Q",
        "scrub": "none requested",
        "config": [
          {
            "name": "tank",
            "state": "DEGRADED",
            "read": "0",
            "write": "0",
            "checksum": "0"
          },
          {
            "name": "mirror-0",
            "state": "DEGRADED",
            "read": "0",
            "write": "0",
            "checksum": "0"
          },
          {
            "name": "c1t0d0",
            "state": "ONLINE",
            "read": "0",
            "write": "0",
            "checksum": "0"
          },
          {
            "name": "c1t1d0",
            "state": "UNAVAIL",
            "read": "0",
            "write": "0",
            "checksum": "0",
            "errors": "cannot open"
          }
        ],
        "errors": "No known data errors"
      }
    ]
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils
from jc.parsers.kv import parse as kv_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`zpool status` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    tags = ['command']
    magic_commands = ['zpool status']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'read', 'write', 'checksum'}

    for obj in proc_data:
        if 'config' in obj:
            for conf in obj['config']:
                for k, v in conf.items():
                    if k in int_list:
                        conf[k] = jc.utils.convert_to_int(v)

    return proc_data


def _build_config_list(string: str) -> List[Dict]:
    config_list: List = []
    for line in filter(None, string.splitlines()):
        if line.strip().endswith('READ WRITE CKSUM'):
            continue

        line_list = line.strip().split(maxsplit=5)
        config_obj: Dict = {}
        config_obj['name'] = line_list[0] if len(line_list) > 0 else None
        config_obj['state'] = line_list[1] if len(line_list) > 1 else None
        config_obj['read'] = line_list[2] if len(line_list) > 2 else None
        config_obj['write'] = line_list[3] if len(line_list) > 3 else None
        config_obj['checksum'] = line_list[4] if len(line_list) > 4 else None
        if len(line_list) == 6:
            config_obj['errors'] = line_list[5]
        config_list.append(config_obj)

    return config_list

def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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

    raw_output: List[Dict] = []
    pool_str: str = ''
    pool_obj: Dict = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            if line.lstrip().startswith('pool: '):
                if pool_str:
                    pool_obj = kv_parse(pool_str)
                    if 'config' in pool_obj:
                        pool_obj['config'] = _build_config_list(pool_obj['config'])
                    raw_output.append(pool_obj)
                pool_str = ''
                pool_str += line + '\n'
                continue

            # preserve indentation in continuation lines
            if line.startswith('        ') or line.startswith('\t'):
                pool_str += line + '\n'
                continue

            # indent path lines for errors field
            if line.startswith('/'):
                pool_str += '  ' + line + '\n'
                continue

            # remove initial spaces from field start lines so we don't confuse line continuation
            pool_str += line.strip() + '\n'

    if pool_str:
        pool_obj = kv_parse(pool_str)
        if 'config' in pool_obj:
            pool_obj['config'] = _build_config_list(pool_obj['config'])
        raw_output.append(pool_obj)

    return raw_output if raw else _process(raw_output)
