r"""jc - JSON Convert `needrestart -b` command output parser

Usage (cli):

    $ needrestart -b | jc --needrestart

or

    $ jc needrestart -b

Usage (module):

    import jc
    result = jc.parse('needrestart', needrestart_command_output)

Schema:

    {
      "version":                        string,
      "running_kernel_version":         string,
      "expected_kernel_version":        string,
      "kernel_status":                  integer,
      "container":                      string,
      "session": [
                                        string
      ],
      "service": [
                                        string
      ],
      "pid": [
                                        string
      ]
    }

Examples:

    $ needrestart -b | jc --needrestart -p
    {
      "version": "2.1",
      "running_kernel_version": "3.19.3-tl1+",
      "expected_kernel_version": "3.19.3-tl1+",
      "kernel_status": 1,
      "container": "LXC web1",
      "session": [
        "metabase @ user manager service",
        "root @ session #28017"
      ],
      "service": [
        "systemd-journald.service",
        "systemd-machined.service"
      ]
    }

    $ needrestart -b | jc --needrestart -p -r
    {
      "needrestart_ver": "2.1",
      "needrestart_kcur": "3.19.3-tl1+",
      "needrestart_kexp": "3.19.3-tl1+",
      "needrestart_ksta": "1",
      "needrestart_cont": "LXC web1",
      "needrestart_sess": [
        "metabase @ user manager service",
        "root @ session #28017"
      ],
      "needrestart_svc": [
        "systemd-journald.service",
        "systemd-machined.service"
      ]
    }
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`needrestart -b` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['needrestart -b']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    key_map = {
        'needrestart_ver': 'version',
        'needrestart_kcur': 'running_kernel_version',
        'needrestart_kexp': 'expected_kernel_version',
        'needrestart_ksta': 'kernel_status',
        'needrestart_svc': 'service',
        'needrestart_cont': 'container',
        'needrestart_sess': 'session',
        'needrestart_pid': 'pid'
    }

    for key, val in proc_data.copy().items():
        if key == 'needrestart_ksta':
            proc_data[key] = jc.utils.convert_to_int(val)

        if key in key_map:
            proc_data[key_map[key]] = proc_data[key]
            del proc_data[key]

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}
    sess_list: List[str] = []
    svc_list: List[str] = []
    pid_list: List[str] = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            if any([
                line.startswith('NEEDRESTART-VER'),
                line.startswith('NEEDRESTART-KCUR'),
                line.startswith('NEEDRESTART-KEXP'),
                line.startswith('NEEDRESTART-KSTA'),
                line.startswith('NEEDRESTART-CONT')
            ]):
                key, val = line.split(':', maxsplit=1)
                key = jc.utils.normalize_key(key)
                raw_output[key] = val.strip()
                continue

            if line.startswith('NEEDRESTART-SESS'):
                _, val = line.split(':', maxsplit=1)
                sess_list.append(val.strip())
                continue

            if line.startswith('NEEDRESTART-SVC'):
                _, val = line.split(':', maxsplit=1)
                svc_list.append(val.strip())
                continue

            if line.startswith('NEEDRESTART-PID'):
                _, val = line.split(':', maxsplit=1)
                pid_list.append(val.strip())
                continue

        if sess_list:
            raw_output['needrestart_sess'] = sess_list

        if svc_list:
            raw_output['needrestart_svc'] = svc_list

        if pid_list:
            raw_output['needrestart_pid'] = pid_list

    return raw_output if raw else _process(raw_output)
