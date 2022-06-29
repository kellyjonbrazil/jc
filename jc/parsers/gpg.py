"""jc - JSON Convert `gpg --with-colons` command output parser

<<Short gpg description and caveats>>

Usage (cli):

    $ gpg --with-colons | jc --gpg

    or

    $ jc gpg --with-colons

Usage (module):

    import jc
    result = jc.parse('gpg', gpg_command_output)

Schema:

    [
      {
        "gpg":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ gpg | jc --gpg -p
    []

    $ gpg | jc --gpg -p -r
    []
"""
from typing import List, Dict, Optional
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`gpg --with-colons` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['gpg --with-colons']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return proc_data


def _list_get(my_list: List, index: int, default_val=None) -> Optional[str]:
    """get a list value or return None/default value if out of range."""
    if index <= len(my_list) - 1:
        return my_list[index] or None

    return default_val


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

        for line in filter(None, data.splitlines()):
            values = line.split(':')
            line_obj = {
                'type': _list_get(values, 0),
                'validity': _list_get(values, 1),
                'key_length': _list_get(values, 2),
                'pub_key_alg': _list_get(values, 3),
                'key_id': _list_get(values, 4),
                'creation_date': _list_get(values, 5),
                'expiration_date': _list_get(values, 6),
                'certsn_uidhash_trustinfo': _list_get(values, 7),
                'owner_trust': _list_get(values, 8),
                'user_id': _list_get(values, 9),
                'signature_class': _list_get(values, 10),
                'key_capabilities': _list_get(values, 11),
                'cert_fingerprint_other': _list_get(values, 12),
                'flag': _list_get(values, 13),
                'token_sn': _list_get(values, 14),
                'hash_alg': _list_get(values, 15),
                'curve_name': _list_get(values, 16),
                'compliance_flags': _list_get(values, 17),
                'last_update_date': _list_get(values, 18),
                'origin': _list_get(values, 19),
                'comment': _list_get(values, 20)
            }

            raw_output.append(line_obj)

    return raw_output if raw else _process(raw_output)
