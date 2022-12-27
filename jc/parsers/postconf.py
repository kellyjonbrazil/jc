"""jc - JSON Convert `postconf -M` command output parser

Usage (cli):

    $ postconf -M | jc --postconf

or

    $ jc postconf -M

Usage (module):

    import jc
    result = jc.parse('postconf', postconf_command_output)

Schema:

    [
      {
        "service_name":                     string,
        "service_type":                     string,
        "private":                          boolean/null,  # [0]
        "unprivileged":                     boolean/null,  # [0]
        "chroot":                           boolean/null,  # [0]
        "wake_up_time":                     integer/null,  # [0]
        "no_wake_up_before_first_use":      boolean/null,  # [1]
        "process_limit":                    integer/null,  # [0]
        "command":                          string
      }
    ]

    [0] '-' converted to null/None
    [1] null/None if `wake_up_time` is null/None

Examples:

    $ postconf -M | jc --postconf -p
    [
      {
        "service_name": "smtp",
        "service_type": "inet",
        "private": false,
        "unprivileged": null,
        "chroot": true,
        "wake_up_time": null,
        "process_limit": null,
        "command": "smtpd",
        "no_wake_up_before_first_use": null
      },
      {
        "service_name": "pickup",
        "service_type": "unix",
        "private": false,
        "unprivileged": null,
        "chroot": true,
        "wake_up_time": 60,
        "process_limit": 1,
        "command": "pickup",
        "no_wake_up_before_first_use": false
      }
    ]

    $ postconf -M | jc --postconf -p -r
    [
      {
        "service_name": "smtp",
        "service_type": "inet",
        "private": "n",
        "unprivileged": "-",
        "chroot": "y",
        "wake_up_time": "-",
        "process_limit": "-",
        "command": "smtpd"
      },
      {
        "service_name": "pickup",
        "service_type": "unix",
        "private": "n",
        "unprivileged": "-",
        "chroot": "y",
        "wake_up_time": "60",
        "process_limit": "1",
        "command": "pickup"
      }
    ]
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`postconf -M` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['postconf -M']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    keys = ['private', 'unprivileged', 'chroot', 'wake_up_time', 'process_limit']
    bools = ['private', 'unprivileged', 'chroot']
    integers = ['wake_up_time', 'process_limit']

    for item in proc_data:
        if item['wake_up_time'].endswith('?'):
            item['no_wake_up_before_first_use'] = True
        elif item['wake_up_time'] == '-':
            item['no_wake_up_before_first_use'] = None
        else:
            item['no_wake_up_before_first_use'] = False

        for key in keys:
            if item[key] == '-':
                item[key] = None

        for key in bools:
            if item[key] is not None:
                item[key] = jc.utils.convert_to_bool(item[key])

        for key in integers:
            if item[key] is not None:
                item[key] = jc.utils.convert_to_int(item[key])

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
        table = ['service_name service_type private unprivileged chroot wake_up_time process_limit command']
        data_list = list(filter(None, data.splitlines()))
        table.extend(data_list)
        raw_output = simple_table_parse(table)

    return raw_output if raw else _process(raw_output)
