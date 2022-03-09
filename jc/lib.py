"""jc - JSON Convert
JC lib module
"""

import sys
import os
import re
import importlib
from typing import Dict, List, Iterable, Union, Iterator
from jc import appdirs

__version__ = '1.18.5'

parsers = [
    'acpi',
    'airport',
    'airport-s',
    'arp',
    'blkid',
    'cksum',
    'crontab',
    'crontab-u',
    'csv',
    'csv-s',
    'date',
    'df',
    'dig',
    'dir',
    'dmidecode',
    'dpkg-l',
    'du',
    'env',
    'file',
    'finger',
    'free',
    'fstab',
    'group',
    'gshadow',
    'hash',
    'hashsum',
    'hciconfig',
    'history',
    'hosts',
    'id',
    'ifconfig',
    'ini',
    'iostat',
    'iostat-s',
    'iptables',
    'iw-scan',
    'jar-manifest',
    'jobs',
    'kv',
    'last',
    'ls',
    'ls-s',
    'lsblk',
    'lsmod',
    'lsof',
    'lsusb',
    'mount',
    'netstat',
    'nmcli',
    'ntpq',
    'passwd',
    'ping',
    'ping-s',
    'pip-list',
    'pip-show',
    'ps',
    'route',
    'rpm-qi',
    'rsync',
    'rsync-s',
    'sfdisk',
    'shadow',
    'ss',
    'stat',
    'stat-s',
    'sysctl',
    'systemctl',
    'systemctl-lj',
    'systemctl-ls',
    'systemctl-luf',
    'systeminfo',
    'time',
    'timedatectl',
    'tracepath',
    'traceroute',
    'ufw',
    'ufw-appinfo',
    'uname',
    'upower',
    'uptime',
    'vmstat',
    'vmstat-s',
    'w',
    'wc',
    'who',
    'xml',
    'xrandr',
    'yaml',
    'zipinfo'
]

def _cliname_to_modname(parser_cli_name):
    """Return real module name (dashes converted to underscores)"""
    return parser_cli_name.replace('--', '').replace('-', '_')

def _modname_to_cliname(parser_mod_name):
    """Return module's cli name (underscores converted to dashes)"""
    return parser_mod_name.replace('_', '-')

# Create the local_parsers list. This is a list of custom or
# override parsers from <user_data_dir>/jc/jcparsers/*.py.
# Once this list is created, extend the parsers list with it.
local_parsers = []
data_dir = appdirs.user_data_dir('jc', 'jc')
local_parsers_dir = os.path.join(data_dir, 'jcparsers')
if os.path.isdir(local_parsers_dir):
    sys.path.append(data_dir)
    for name in os.listdir(local_parsers_dir):
        if re.match(r'\w+\.py$', name) and os.path.isfile(os.path.join(local_parsers_dir, name)):
            plugin_name = name[0:-3]
            local_parsers.append(_modname_to_cliname(plugin_name))
            if plugin_name not in parsers:
                parsers.append(_modname_to_cliname(plugin_name))
    try:
        del name
    except Exception:
        pass

def _parser_argument(parser_mod_name):
    """Return short name of the parser with dashes and with -- prefix"""
    parser = _modname_to_cliname(parser_mod_name)
    return f'--{parser}'

def _get_parser(parser_mod_name):
    """Return the parser module object"""
    # ensure parser_mod_name is a true module name and not a cli name
    parser_mod_name = _cliname_to_modname(parser_mod_name)

    parser_cli_name = _modname_to_cliname(parser_mod_name)
    modpath = 'jcparsers.' if parser_cli_name in local_parsers else 'jc.parsers.'
    return importlib.import_module(f'{modpath}{parser_mod_name}')

def _parser_is_streaming(parser):
    """
    Returns True if this is a streaming parser, else False

    parser is a parser module object.
    """
    if getattr(parser.info, 'streaming', None):
        return True

    return False

def parse(
    parser_mod_name: str,
    data: Union[str, Iterable[str]],
    quiet: bool = False,
    raw: bool = False,
    ignore_exceptions: bool = None,
    **kwargs
) -> Union[Dict, List[Dict], Iterator[Dict]]:
    """
    Parse the string data using the supplied parser module.

    This function provides a high-level API to simplify parser use. This
    function will call built-in parsers and custom plugin parsers.

    Example:

        >>> import jc
        >>> jc.parse('date', 'Tue Jan 18 10:23:07 PST 2022')
        {'year': 2022, 'month': 'Jan', 'month_num': 1, 'day'...}

    To get a list of available parser module names, use `parser_mod_list()`.

    You can also use the lower-level parser modules directly:

        >>> import jc.parsers.date
        >>> jc.parsers.date.parse('Tue Jan 18 10:23:07 PST 2022')

    Though, accessing plugin parsers directly is a bit more cumbersome, so
    this higher-level API is recommended. Here is how you can access plugin
    parsers without this API:

        >>> import os
        >>> import sys
        >>> import jc.appdirs
        >>> data_dir = jc.appdirs.user_data_dir('jc', 'jc')
        >>> local_parsers_dir = os.path.join(data_dir, 'jcparsers')
        >>> sys.path.append(local_parsers_dir)
        >>> import my_custom_parser
        >>> my_custom_parser.parse('command_data')

    Parameters:

        parser_mod_name:    (string)     name of the parser module. This
                                         function will accept module_name,
                                         cli-name, and --argument-name
                                         variants of the module name.

        data:               (string or   data to parse (string for normal
                            iterator)    parsers, iterator of strings for
                                         streaming parsers)

        raw:                (boolean)    output preprocessed JSON if True

        quiet:              (boolean)    suppress warning messages if True

        ignore_exceptions:  (boolean)    ignore parsing exceptions if True
                                         (streaming parsers only)

    Returns:

        Standard Parsers:   Dictionary or List of Dictionaries
        Streaming Parsers:  Generator Object containing Dictionaries
    """
    jc_parser = _get_parser(parser_mod_name)

    if ignore_exceptions is not None:
        return jc_parser.parse(data, quiet=quiet, raw=raw,
                               ignore_exceptions=ignore_exceptions, **kwargs)

    return jc_parser.parse(data, quiet=quiet, raw=raw, **kwargs)

def parser_mod_list() -> List[str]:
    """Returns a list of all available parser module names."""
    return [_cliname_to_modname(p) for p in parsers]

def plugin_parser_mod_list() -> List[str]:
    """
    Returns a list of plugin parser module names. This function is a
    subset of `parser_mod_list()`.
    """
    return [_cliname_to_modname(p) for p in local_parsers]

def standard_parser_mod_list() -> List[str]:
    """
    Returns a list of standard parser module names. This function is a
    subset of `parser_mod_list()` and does not contain any streaming
    parsers.
    """
    plist = []
    for p in parsers:
        parser = _get_parser(p)
        if not _parser_is_streaming(parser):
            plist.append(_cliname_to_modname(p))
    return plist

def streaming_parser_mod_list() -> List[str]:
    """
    Returns a list of streaming parser module names. This function is a
    subset of `parser_mod_list()`.
    """
    plist = []
    for p in parsers:
        parser = _get_parser(p)
        if _parser_is_streaming(parser):
            plist.append(_cliname_to_modname(p))
    return plist

def parser_info(parser_mod_name: str) -> Dict:
    """
    Returns a dictionary that includes the module metadata.

    This function will accept **module_name**, **cli-name**, and
    **--argument-name** variants of the module name string.
    """
    # ensure parser_mod_name is a true module name and not a cli name
    parser_mod_name = _cliname_to_modname(parser_mod_name)

    parser_mod = _get_parser(parser_mod_name)
    info_dict: Dict = {}

    if hasattr(parser_mod, 'info'):
        info_dict['name'] = parser_mod_name
        info_dict['argument'] = _parser_argument(parser_mod_name)
        parser_entry = vars(parser_mod.info)

        for k, v in parser_entry.items():
            if not k.startswith('__'):
                info_dict[k] = v

        if _modname_to_cliname(parser_mod_name) in local_parsers:
            info_dict['plugin'] = True

    return info_dict

def all_parser_info() -> List[Dict]:
    """
    Returns a list of dictionaries that includes metadata for all modules.
    """
    return [parser_info(p) for p in parsers]

def get_help(parser_mod_name: str) -> None:
    """
    Show help screen for the selected parser.

    This function will accept **module_name**, **cli-name**, and
    **--argument-name** variants of the module name string.
    """
    help(_get_parser(parser_mod_name))
