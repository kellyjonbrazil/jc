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
    pool_obj: Dict = {}
    in_config: bool = False
    parent: str = ''
    config: List[Dict] = []
    config_obj: Dict = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            line_list = line.strip().split(maxsplit=1)

            if line.startswith('  pool: '):
                if pool_obj:
                    if config:
                        pool_obj['config'] = config
                    raw_output.append(pool_obj)

                config_obj = {}
                config = []
                parent = ''
                in_config = False
                pool_obj = {
                    "pool": line_list[1]
                }
                continue

            if line.startswith(' state: ') \
                or line.startswith('  scan: ') \
                or line.startswith('errors: '):
                pool_obj[line_list[0][:-1]] = line_list[1]
                in_config = False
                continue

            if line.startswith('config:'):
                in_config = True
                continue

            if in_config and line.strip().endswith('READ WRITE CKSUM'):
                continue

            if in_config:
                config_line = line.rstrip().split()
                config_obj = {}
                if line.startswith('          '):
                    config_obj['parent'] = parent
                    config_obj['name'] = config_line[0]
                else:
                    parent = config_line[0]
                    config_obj['name'] = parent

                config_obj['state'] = config_line[1]
                config_obj['read'] = config_line[2]
                config_obj['write'] = config_line[3]
                config_obj['checksum'] = config_line[4]

                config.append(config_obj)

    if pool_obj:
        if config:
            pool_obj['config'] = config
        raw_output.append(pool_obj)

    return raw_output if raw else _process(raw_output)
