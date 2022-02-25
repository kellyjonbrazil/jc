"""jc - JSON CLI output utility `nmcli` command output parser

<<Short nmcli description and caveats>>

Usage (cli):

    $ nmcli | jc --nmcli

    or

    $ jc nmcli

Usage (module):

    import jc
    result = jc.parse('nmcli', nmcli_command_output)

    or

    import jc.parsers.nmcli
    result = jc.parsers.nmcli.parse(nmcli_command_output)

Schema:

    [
      {
        "nmcli":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ nmcli | jc --nmcli -p
    []

    $ nmcli | jc --nmcli -p -r
    []
"""
import re
from typing import List, Dict, Optional
import jc.utils
from jc.parsers.universal import sparse_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`nmcli` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['nmcli']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

    return proc_data

def _normalize_key(keyname: str) -> str:
    return keyname.replace(' ', '_')\
                  .replace('.', '_')\
                  .replace('[', '_')\
                  .replace(']', '')\
                  .replace('-', '_')\
                  .replace('GENERAL_', '')\
                  .lower()

def _normalize_value(value: str) -> Optional[str]:
    value = value.strip()

    if value == '--':
        return None

    if value.startswith('"') and value.endswith('"'):
        value = value.strip('"')

    return value


def _normalize_header(keyname: str) -> str:
    return keyname.replace('.', '_')\
                  .replace('[', '_')\
                  .replace(']', ' ')\
                  .replace('-', '_')\
                  .lower()


def _add_text_kv(key: str, value: Optional[str]) -> Optional[Dict]:
    """
    Add keys with _text suffix if there is a text description inside
    paranthesis at the end of a value. The value of the _text field will
    only be the text inside the parenthesis. This allows cleanup of the
    original field (convert to int/float/etc) without losing information.
    """
    if value and '(' in value and value.endswith(')'):
        new_val = re.search(r'\((\w+)\)$', value)
        if new_val:
            return ({key + '_text': new_val.group(1)})

    return None


def _remove_text_from_value(value: Optional[str]) -> Optional[str]:
    """
    Remove the text summary part of a value. Used when an extra text
    summary k/v pair are added.
    """
    if value:
        return re.sub(r"\s+\((\w+)\)$", '', value)

    return None


def _split_routes(value: str) -> Dict:
    # dst = 192.168.71.0/24, nh = 0.0.0.0, mt = 100
    # dst = ff00::/8, nh = ::, mt = 256, table=255
    output_dict = {}
    val_list = value.split(',')
    for val in val_list:
        k, v = val.split('=')
        output_dict[k.strip()] = v.strip()

    return output_dict


def _device_show_parse(data: str) -> List[Dict]:
    raw_output: List = []
    item: Dict = {}
    current_item = ''

    for line in filter(None, data.splitlines()):
        key, value = line.split(':', maxsplit=1)
        key_n = _normalize_key(key)
        value_n = _normalize_value(value)

        if item and 'device' in key_n and value_n != current_item:
            raw_output.append(item)
            item = {}
            current_item = value

        item.update({key_n: value_n})

        text_kv = _add_text_kv(key_n, value_n)
        if text_kv:
            item[key_n] = _remove_text_from_value(value_n)
            item.update(text_kv)

    # get final item
    if item:
        raw_output.append(item)

    return raw_output


def _connection_show_x_parse(data: str) -> List[Dict]:
    raw_output: List = []
    item: Dict = {}

    for line in filter(None, data.splitlines()):
        key, value = line.split(':', maxsplit=1)

        key_n = _normalize_key(key)
        value_n = _normalize_value(value)
        item.update({key_n: value_n})

        text_kv = _add_text_kv(key_n, value_n)
        if text_kv:
            item[key_n] = _remove_text_from_value(value_n)
            item.update(text_kv)

        if '_route_' in key_n and key_n[-1].isdigit():
            item[key_n] = _split_routes(item[key_n])


    if item:
        raw_output.append(item)

    return raw_output


def _general_permissions_parse(data: str) -> List[Dict]:
    print('general permissions')


def _table_parse(data: str) -> List[Dict]:
    data_list = list(filter(None, data.splitlines()))
    data_list[0] = _normalize_header(data_list[0])
    raw_output = sparse_table_parse(data_list)

    for item in raw_output:
        for key in item:
            item[key] = _normalize_value(item[key])

    return raw_output


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

        # nmcli (second line startswith \t)
        if data.splitlines()[1].startswith('\t'):
            print('nmcli only')

        # nmcli device show
        # nmcli device show lo
        elif data.startswith('GENERAL.DEVICE'):
            raw_output = _device_show_parse(data)

        # nmcli connection show lo
        elif data.startswith('connection.id:'):
            raw_output = _connection_show_x_parse(data)

        # nmcli general permissions (k/v pairs)
        elif data.startswith('PERMISSION '):
            raw_output = _general_permissions_parse(data)

        # nmcli general
        # nmcli connection
        # nmcli device
        else:
            raw_output = _table_parse(data)

    return raw_output if raw else _process(raw_output)
