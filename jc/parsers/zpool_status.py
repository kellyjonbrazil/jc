"""jc - JSON Convert `zpool status` command output parser

<<Short zpool status description and caveats>>

Usage (cli):

    $ zpool status | jc --zpool_status

or

    $ jc zpool status

Usage (module):

    import jc
    result = jc.parse('zpool_status', zpool_status_command_output)

Schema:

    [
      {
        "zpool status":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ zpool status | jc --zpool status -p
    []

    $ zpool status | jc --zpool status -p -r
    []
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils
from jc.parsers.kv import parse as kv_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
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
    return proc_data


def _build_config_list(string: str) -> List[Dict]:
    config_list: List = []
    for line in filter(None, string.splitlines()):
        if line.strip().endswith('READ WRITE CKSUM'):
            continue

        line_list = line.strip().split(maxsplit=5)
        config_obj: Dict = {}
        config_obj['name'] = line_list[0]
        config_obj['state'] = line_list[1]
        config_obj['read'] = line_list[2]
        config_obj['write'] = line_list[3]
        config_obj['checksum'] = line_list[4]
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

            if line.startswith('        '):
                pool_str += line + '\n'
                continue

            pool_str += line.strip() + '\n'

    if pool_str:
        pool_obj = kv_parse(pool_str)
        if 'config' in pool_obj:
            pool_obj['config'] = _build_config_list(pool_obj['config'])
        raw_output.append(pool_obj)

    return raw_output if raw else _process(raw_output)
