"""jc - JSON Convert ssh configuration file parser

Usage (cli):

    $ cat ssh_conf | jc --ssh-conf

Usage (module):

    import jc
    result = jc.parse('ssh_conf', ssh_conf_file_output)

Schema:

    [
      {
        "ssh_conf":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ cat ssh_conf | jc --ssh-conf -p
    []

    $ cat ssh_conf | jc --ssh-conf -p -r
    []
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils
from .paramiko.config import SSHConfig as sshconfig


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'ssh config file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using Paramiko library at https://github.com/paramiko/paramiko.'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


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

    if jc.utils.has_data(data):
        myconfig = sshconfig.from_text(data)
        hostnames = myconfig.get_hostnames()
        raw_output = [myconfig.lookup(x) for x in hostnames]

    return raw_output if raw else _process(raw_output)
