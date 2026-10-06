r"""jc - JSON Convert `nmcli` command output parser

Supports the following `nmcli` subcommands:
- `nmcli general`
- `nmcli general permissions`
- `nmcli connection`
- `nmcli connection show <device_name>`
- `nmcli -t device wifi list`
- `nmcli device`
- `nmcli device show`
- `nmcli device show <device_name>`

Usage (cli):

    $ nmcli device show lo | jc --nmcli

or

    $ jc nmcli device show lo

Usage (module):

    import jc
    result = jc.parse('nmcli', nmcli_command_output)

Schema:

Because there are so many options, the schema is not strictly defined.
Integer and Float value conversions are attempted and the original
values are kept if they fail. If you don't want automatic conversion,
then use the `-r` or `raw=True` option to disable it.

The structure is flat, for the most part, but there are a couple of
"well-known" keys that are further parsed into objects for convenience.
These are documented below.

    [
      {
        "<key>":                  string/integer/float,   # [0]
        "team_config":            object/null,
        "team_port_config":       object/null,
        "dhcp4_option_x": {
          "name":                 string,
          "value":                string/integer/float,
        },
        "dhcp6_option_x": {
          "name":                 string,
          "value":                string/integer/float,
        },
        "ip4_route_x": {
          "dst":                  string,
          "nh":                   string,
          "mt":                   integer
        },
        "ip6_route_x": {
          "dst":                  string,
          "nh":                   string,
          "mt":                   integer,
          "table":                integer
        }
      }
    ]

    [0] all values of `---` are converted to null

For `nmcli -t device wifi list` output, the schema is:

    [
      {
        "in_use":                 string,
        "bssid":                  string,
        "ssid":                   string,
        "mode":                   string,
        "chan":                   integer,
        "rate":                   string,
        "signal":                 integer,
        "bars":                   string,
        "security":               string/null
      }
    ]

Examples:

    $ nmcli connection show ens33 | jc --nmcli -p
    [
      {
        "connection_id": "ens33",
        "connection_uuid": "d92ece08-9e02-47d5-b2d2-92c80e155744",
        "connection_stable_id": null,
        "connection_type": "802-3-ethernet",
        "connection_interface_name": "ens33",
        "connection_autoconnect": "yes",
        ...
        "ip4_address_1": "192.168.71.180/24",
        "ip4_gateway": "192.168.71.2",
        "ip4_route_1": {
          "dst": "0.0.0.0/0",
          "nh": "192.168.71.2",
          "mt": 100
        },
        "ip4_route_2": {
          "dst": "192.168.71.0/24",
          "nh": "0.0.0.0",
          "mt": 100
        },
        "ip4_dns_1": "192.168.71.2",
        "ip4_domain_1": "localdomain",
        "dhcp4_option_1": {
          "name": "broadcast_address",
          "value": "192.168.71.255"
        },
        ...
        "ip6_address_1": "fe80::c1cb:715d:bc3e:b8a0/64",
        "ip6_gateway": null,
        "ip6_route_1": {
          "dst": "fe80::/64",
          "nh": "::",
          "mt": 100
        }
      }
    ]

    $ nmcli connection show ens33 | jc --nmcli -p -r
    [
      {
        "connection_id": "ens33",
        "connection_uuid": "d92ece08-9e02-47d5-b2d2-92c80e155744",
        "connection_stable_id": null,
        "connection_type": "802-3-ethernet",
        "connection_interface_name": "ens33",
        "connection_autoconnect": "yes",
        ...
        "ip4_address_1": "192.168.71.180/24",
        "ip4_gateway": "192.168.71.2",
        "ip4_route_1": {
          "dst": "0.0.0.0/0",
          "nh": "192.168.71.2",
          "mt": "100"
        },
        "ip4_route_2": {
          "dst": "192.168.71.0/24",
          "nh": "0.0.0.0",
          "mt": "100"
        },
        "ip4_dns_1": "192.168.71.2",
        "ip4_domain_1": "localdomain",
        "dhcp4_option_1": {
          "name": "broadcast_address",
          "value": "192.168.71.255"
        },
        ...
        "ip6_address_1": "fe80::c1cb:715d:bc3e:b8a0/64",
        "ip6_gateway": null,
        "ip6_route_1": {
          "dst": "fe80::/64",
          "nh": "::",
          "mt": "100"
        }
      }
    ]
"""
import re
import json
from typing import List, Dict, Optional
import jc.utils
from jc.parsers.universal import sparse_table_parse
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`nmcli` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['nmcli']
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

    for entry in proc_data:
        for key in entry:
            # use normal int/float conversions since jc.utils.convert_to_int is too greedy
            try:
                if '.' in entry[key]:
                    entry[key] = float(entry[key])
                else:
                    entry[key] = int(entry[key])
            except Exception:
                pass

            if ('_option_' in key or '_route_' in key) and key[-1].isdigit():
                for k in entry[key]:
                    try:
                        if '.' in entry[key][k]:
                            entry[key][k] = float(entry[key][k])
                        else:
                            entry[key][k] = int(entry[key][k])
                    except Exception:
                        pass

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
    parenthesis at the end of a value. The value of the _text field will
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


def _split_options(value: str) -> Dict:
    # ip_address = 192.168.71.180
    # requested_broadcast_address = 1
    output_dict = {}
    k, v = value.split('=')
    output_dict['name'] = k.strip()
    output_dict['value'] = v.strip()

    return output_dict



_WIFI_HEADERS = (
    'in_use',
    'bssid',
    'ssid',
    'mode',
    'chan',
    'rate',
    'signal',
    'bars',
    'security'
)


def _split_terse_line(line: str) -> List[str]:
    """Split an nmcli terse-mode line while honoring escaped delimiters."""
    output = []
    field = []
    escape_character = chr(92)
    index = 0

    while index < len(line):
        character = line[index]

        if character == escape_character and index + 1 < len(line):
            next_character = line[index + 1]
            if next_character in (escape_character, ':'):
                field.append(next_character)
                index += 2
                continue

        if character == ':':
            output.append(''.join(field))
            field = []
        else:
            field.append(character)

        index += 1

    output.append(''.join(field))
    return output


def _is_wifi_list_line(line: str) -> bool:
    fields = _split_terse_line(line)
    return (
        len(fields) == len(_WIFI_HEADERS)
        and re.fullmatch(r'(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}', fields[1]) is not None
    )


def _wifi_list_parse(data: str) -> List[Dict]:
    raw_output = []

    for line in filter(None, data.splitlines()):
        values = _split_terse_line(line)
        if len(values) != len(_WIFI_HEADERS):
            raise ParseError(
                'Unexpected number of fields in nmcli terse WiFi list output.'
            )

        raw_output.append({
            key: _normalize_value(value)
            for key, value in zip(_WIFI_HEADERS, values)
        })

    return raw_output


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

        if '_option_' in key_n and key_n[-1].isdigit():
            item[key_n] = _split_options(item[key_n])

        if '_route_' in key_n and key_n[-1].isdigit():
            item[key_n] = _split_routes(item[key_n])

    # get final item
    if item:
        raw_output.append(item)

    return raw_output


def _connection_show_x_parse(data: str) -> List[Dict]:
    raw_output: List = []
    item: Dict = {}
    in_team_config: bool = False
    team_config_value: List = []

    for line in filter(None, data.splitlines()):

        # fix for team.config and team-port.config, which are multi-line JSON
        if line.startswith('team.config:') or line.startswith('team-port.config:'):
            key, value = line.split(':', maxsplit=1)
            key_team = _normalize_key(key)
            value_team = value.strip()

            if value_team == '--':
                team_config_value = []
                item[key_team] = None
                continue

            in_team_config = True
            team_config_value.append(value_team)
            item[key_team] = {}
            continue

        STARTSWITH_TEAM = line.startswith('team.') or line.startswith('team-port.')
        if not STARTSWITH_TEAM and in_team_config:
            team_config_value.append(line.strip())
            continue

        in_team_config = False

        if team_config_value:
            # team.config and team-port.config values should always be JSON
            item[key_team] = json.loads(''.join(team_config_value))
            team_config_value = []

        key, value = line.split(':', maxsplit=1)

        key_n = _normalize_key(key)
        value_n = _normalize_value(value)
        item.update({key_n: value_n})

        text_kv = _add_text_kv(key_n, value_n)
        if text_kv:
            item[key_n] = _remove_text_from_value(value_n)
            item.update(text_kv)

        if '_option_' in key_n and key_n[-1].isdigit():
            item[key_n] = _split_options(item[key_n])

        if '_route_' in key_n and key_n[-1].isdigit():
            item[key_n] = _split_routes(item[key_n])

    if item:
        raw_output.append(item)

    return raw_output


def _general_permissions_parse(data: str) -> List[Dict]:
    raw_output = []
    output_dict = {}
    for line in filter(None, data.splitlines()):
        key, value = line.split()
        key_n = _normalize_key(key)
        output_dict[key_n] = value

    output_dict.pop('permission')
    raw_output.append(output_dict)

    return raw_output


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

        data_lines = data.splitlines()
        first_line = next(line for line in data_lines if line.strip())

        # nmcli -t device wifi list
        if _is_wifi_list_line(first_line):
            raw_output = _wifi_list_parse(data)

        # nmcli (second line startswith \t)
        elif len(data_lines) > 1 and data_lines[1].startswith('\t'):
            raise ParseError('Use the device, connection, or general subcommand in nmcli.')

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
