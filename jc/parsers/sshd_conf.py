"""jc - JSON Convert `sshd -T` command output parser

<<Short sshd_conf description and caveats>>

Usage (cli):

    $ sshd -T | jc --sshd-conf

or

    $ jc sshd -T

Usage (module):

    import jc
    result = jc.parse('sshd_conf', sshd_command_output)

Schema:

    [
      {
        "sshd_conf":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ sshd_conf | jc --sshd_conf -p
    []

    $ sshd_conf | jc --sshd_conf -p -r
    []
"""
from typing import Set, List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`sshd -T` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['sshd -T']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    split_fields_space: Set[str] = {
        'authorizedkeysfile', 'include', 'ipqos', 'permitlisten', 'permitopen'
    }

    split_fields_comma: Set[str] = {
        'casignaturealgorithms', 'ciphers', 'gssapikexalgorithms', 'hostbasedacceptedalgorithms',
        'hostbasedacceptedkeytypes', 'hostkeyalgorithms', 'kexalgorithms', 'macs',
        'pubkeyacceptedalgorithms', 'pubkeyacceptedkeytypes'
    }

    int_list: Set[str] = {'clientalivecountmax', 'clientaliveinterval', 'logingracetime',
        'maxauthtries', 'maxsessions', 'maxstartups', 'maxstartups_rate', 'maxstartups_full',
        'rekeylimit', 'rekeylimit_time', 'x11displayoffset', 'x11maxdisplays'
    }

    dict_copy = proc_data.copy()
    for key, val in dict_copy.items():
        # this is a list value
        if key == 'acceptenv':
            new_list: List[str] = []
            for item in val:  # type: ignore
                new_list.extend(item.split())
            proc_data[key] = new_list
            continue

        if key == 'maxstartups':
            maxstart_split = val.split(':', maxsplit=2)  # type: ignore
            proc_data[key] = maxstart_split[0]
            if len(maxstart_split) > 1:
                proc_data[key + '_rate'] = maxstart_split[1]
            if len(maxstart_split) > 2:
                proc_data[key + '_full'] = maxstart_split[2]
            continue

        if key == 'port':
            port_list: List[int] = []
            for item in val:  # type: ignore
                port_list.append(int(item))
            proc_data[key] = port_list
            continue

        if key == 'rekeylimit':
            rekey_split = val.split(maxsplit=1)  # type: ignore
            proc_data[key] = rekey_split[0]
            if len(rekey_split) > 1:
                proc_data[key + '_time'] = rekey_split[1]
            continue

        if key == 'subsystem':
            rekey_split = val.split(maxsplit=1)  # type: ignore
            proc_data[key] = rekey_split[0]
            if len(rekey_split) > 1:
                proc_data[key + '_command'] = rekey_split[1]
            continue

        if key in split_fields_space:
            proc_data[key] = val.split()  # type: ignore
            continue

        if key in split_fields_comma:
            proc_data[key] = val.split(',')  # type: ignore
            continue

    for key, val in proc_data.items():
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(val)

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

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}
    multi_fields: Set[str] = {'acceptenv', 'hostkey', 'listenaddress', 'port'}
    modified_fields: Set[str] = {'casignaturealgorithms', 'ciphers', 'hostbasedacceptedalgorithms',
        'kexalgorithms', 'macs', 'pubkeyacceptedalgorithms'
    }
    modifiers: Set[str] = {'+', '-', '^'}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            # support configuration file by skipping commented lines
            if line.strip().startswith('#'):
                continue

            key, val = line.split(maxsplit=1)
            # support configuration file by converting to lower case
            key = key.lower()

            if key in multi_fields:
                if key not in raw_output:
                    raw_output[key] = []
                raw_output[key].append(val)
                continue

            if key in modified_fields and val[0] in modifiers:
                raw_output[key] = val[1:]
                raw_output[key + '_strategy'] = val[0]
                continue

            raw_output[key] = val
            continue

    return raw_output if raw else _process(raw_output)
