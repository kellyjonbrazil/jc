"""jc - JSON CLI output utility
JC lib module
"""

import sys
import os
import re
import importlib
from jc import appdirs

__version__ = '1.18.1'

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
    'ntpq',
    'passwd',
    'ping',
    'ping-s',
    'pip-list',
    'pip-show',
    'ps',
    'route',
    'rpm-qi',
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
    'yaml',
    'zipinfo'
]

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
            local_parsers.append(plugin_name)
            if plugin_name not in parsers:
                parsers.append(plugin_name)
    try:
        del name
    except Exception:
        pass


def _cliname_to_modname(parser_cli_name):
    """Return real module name (dashes converted to underscores)"""
    return parser_cli_name.replace('-', '_')

def _modname_to_cliname(parser_mod_name):
    """Return module's cli name (underscores converted to dashes)"""
    return parser_mod_name.replace('_', '-')

def _get_parser(parser_mod_name):
    """Return the parser module object"""
    parser_cli_name = _modname_to_cliname(parser_mod_name)
    modpath = 'jcparsers.' if parser_cli_name in local_parsers else 'jc.parsers.'
    return importlib.import_module(f'{modpath}{parser_mod_name}')

def parse(parser_mod_name, data,
          quiet=False, raw=False, ignore_exceptions=None, **kwargs):
    """
    Parse the string data using the supplied parser module.

    This function provides a high-level API to simplify parser use. This
    function will call built-in parsers and custom plugin parsers.

    Example:

        >>> import jc
        >>> jc.parse('date', 'Tue Jan 18 10:23:07 PST 2022')
        {'year': 2022, 'month': 'Jan', 'month_num': 1, 'day'...}

    To get a list of available parser module names, use `parser_mod_list()`
    or `plugin_parser_mod_list()`. `plugin_parser_mod_list()` is a subset
    of `parser_mod_list()`.

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

        parser_mod_name:    (string)     name of the parser module

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

def parser_mod_list():
    """Returns a list of all available parser module names."""
    return [_cliname_to_modname(p) for p in parsers]

def plugin_parser_mod_list():
    """
    Returns a list of plugin parser module names. This function is a
    subset of `parser_mod_list()`.
    """
    return [_cliname_to_modname(p) for p in local_parsers]

def get_help(parser_mod_name):
    """Show help screen for the selected parser."""
    help(_get_parser(parser_mod_name))
