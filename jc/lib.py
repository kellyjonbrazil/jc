"""jc - JSON Convert lib module"""
import sys
import os
import re
import importlib
from typing import List, Iterable, Optional, Union, Iterator
from types import ModuleType
from .jc_types import ParserInfoType, JSONDictType
from jc import appdirs


__version__ = '1.23.6'

parsers: List[str] = [
    'acpi',
    'airport',
    'airport-s',
    'arp',
    'asciitable',
    'asciitable-m',
    'blkid',
    'bluetoothctl',
    'cbt',
    'cef',
    'cef-s',
    'certbot',
    'chage',
    'cksum',
    'clf',
    'clf-s',
    'crontab',
    'crontab-u',
    'csv',
    'csv-s',
    'date',
    'datetime-iso',
    'df',
    'dig',
    'dir',
    'dmidecode',
    'dpkg-l',
    'du',
    'email-address',
    'env',
    'file',
    'find',
    'findmnt',
    'finger',
    'free',
    'fstab',
    'git-log',
    'git-log-s',
    'git-ls-remote',
    'gpg',
    'group',
    'gshadow',
    'hash',
    'hashsum',
    'hciconfig',
    'history',
    'host',
    'hosts',
    'id',
    'ifconfig',
    'ini',
    'ini-dup',
    'iostat',
    'iostat-s',
    'ip-address',
    'iptables',
    'ip-route',
    'iso-datetime',
    'iw-scan',
    'iwconfig',
    'jar-manifest',
    'jobs',
    'jwt',
    'kv',
    'last',
    'ls',
    'ls-s',
    'lsattr',
    'lsb-release',
    'lsblk',
    'lsmod',
    'lsof',
    'lspci',
    'lsusb',
    'm3u',
    'mdadm',
    'mount',
    'mpstat',
    'mpstat-s',
    'netstat',
    'nmcli',
    'nsd-control',
    'ntpq',
    'openvpn',
    'os-prober',
    'os-release',
    'passwd',
    'pci-ids',
    'pgpass',
    'pidstat',
    'pidstat-s',
    'ping',
    'ping-s',
    'pip-list',
    'pip-show',
    'plist',
    'postconf',
    'proc',
    'proc-buddyinfo',
    'proc-consoles',
    'proc-cpuinfo',
    'proc-crypto',
    'proc-devices',
    'proc-diskstats',
    'proc-filesystems',
    'proc-interrupts',
    'proc-iomem',
    'proc-ioports',
    'proc-loadavg',
    'proc-locks',
    'proc-meminfo',
    'proc-modules',
    'proc-mtrr',
    'proc-pagetypeinfo',
    'proc-partitions',
    'proc-slabinfo',
    'proc-softirqs',
    'proc-stat',
    'proc-swaps',
    'proc-uptime',
    'proc-version',
    'proc-vmallocinfo',
    'proc-vmstat',
    'proc-zoneinfo',
    'proc-driver-rtc',
    'proc-net-arp',
    'proc-net-dev',
    'proc-net-dev-mcast',
    'proc-net-if-inet6',
    'proc-net-igmp',
    'proc-net-igmp6',
    'proc-net-ipv6-route',
    'proc-net-netlink',
    'proc-net-netstat',
    'proc-net-packet',
    'proc-net-protocols',
    'proc-net-route',
    'proc-net-tcp',
    'proc-net-unix',
    'proc-pid-fdinfo',
    'proc-pid-io',
    'proc-pid-maps',
    'proc-pid-mountinfo',
    'proc-pid-numa-maps',
    'proc-pid-smaps',
    'proc-pid-stat',
    'proc-pid-statm',
    'proc-pid-status',
    'ps',
    'resolve-conf',
    'route',
    'rpm-qi',
    'rsync',
    'rsync-s',
    'semver',
    'sfdisk',
    'shadow',
    'srt',
    'ss',
    'ssh-conf',
    'sshd-conf',
    'stat',
    'stat-s',
    'sysctl',
    'syslog',
    'syslog-s',
    'syslog-bsd',
    'syslog-bsd-s',
    'systemctl',
    'systemctl-lj',
    'systemctl-ls',
    'systemctl-luf',
    'systeminfo',
    'time',
    'timedatectl',
    'timestamp',
    'toml',
    'top',
    'top-s',
    'tracepath',
    'traceroute',
    'udevadm',
    'ufw',
    'ufw-appinfo',
    'uname',
    'update-alt-gs',
    'update-alt-q',
    'upower',
    'uptime',
    'url',
    'ver',
    'veracrypt',
    'vmstat',
    'vmstat-s',
    'w',
    'wc',
    'who',
    'x509-cert',
    'x509-csr',
    'xml',
    'xrandr',
    'yaml',
    'zipinfo',
    'zpool-iostat',
    'zpool-status'
]

def _cliname_to_modname(parser_cli_name: str) -> str:
    """Return real module name (dashes converted to underscores)"""
    return parser_cli_name.replace('--', '').replace('-', '_')

def _modname_to_cliname(parser_mod_name: str) -> str:
    """Return module's cli name (underscores converted to dashes)"""
    return parser_mod_name.replace('_', '-')

def _is_valid_parser_plugin(name: str, local_parsers_dir: str) -> bool:
    if re.match(r'\w+\.py$', name) and os.path.isfile(os.path.join(local_parsers_dir, name)):
        try:
            parser_mod_name = _cliname_to_modname(name)[0:-3]
            modpath = 'jcparsers.'
            plugin =  importlib.import_module(f'{modpath}{parser_mod_name}')
            if hasattr(plugin, 'info') and hasattr(plugin, 'parse'):
                del plugin
                return True
        except Exception:
            return False
    return False

# Create the local_parsers list. This is a list of custom or
# override parsers from <user_data_dir>/jc/jcparsers/*.py.
# Once this list is created, extend the parsers list with it.
local_parsers: List[str] = []
data_dir = appdirs.user_data_dir('jc', 'jc')  # type: ignore
local_parsers_dir = os.path.join(data_dir, 'jcparsers')
if os.path.isdir(local_parsers_dir):
    sys.path.append(data_dir)
    for name in os.listdir(local_parsers_dir):
        if _is_valid_parser_plugin(name, local_parsers_dir):
            plugin_name = name[0:-3]
            local_parsers.append(_modname_to_cliname(plugin_name))
            if plugin_name not in parsers:
                parsers.append(_modname_to_cliname(plugin_name))
    try:
        del name
    except Exception:
        pass

def _parser_argument(parser_mod_name: str) -> str:
    """Return short name of the parser with dashes and with -- prefix"""
    parser = _modname_to_cliname(parser_mod_name)
    return f'--{parser}'

def _get_parser(parser_mod_name: str) -> ModuleType:
    """Return the parser module object"""
    # ensure parser_mod_name is a true module name and not a cli name
    parser_mod_name = _cliname_to_modname(parser_mod_name)
    parser_cli_name = _modname_to_cliname(parser_mod_name)
    modpath: str = 'jcparsers.' if parser_cli_name in local_parsers else 'jc.parsers.'
    return importlib.import_module(f'{modpath}{parser_mod_name}')

def _parser_is_streaming(parser: ModuleType) -> bool:
    """
    Returns True if this is a streaming parser, else False

    parser is a parser module object.
    """
    if getattr(parser.info, 'streaming', None):
        return True

    return False

def _parser_is_hidden(parser: ModuleType) -> bool:
    """
    Returns True if this is a hidden parser, else False

    parser is a parser module object.
    """
    if getattr(parser.info, 'hidden', None):
        return True

    return False

def _parser_is_deprecated(parser: ModuleType) -> bool:
    """
    Returns True if this is a deprecated parser, else False

    parser is a parser module object.
    """
    if getattr(parser.info, 'deprecated', None):
        return True

    return False

def parse(
    parser_mod_name: Union[str, ModuleType],
    data: Union[str, bytes, Iterable[str]],
    quiet: bool = False,
    raw: bool = False,
    ignore_exceptions: Optional[bool] = None,
    **kwargs
) -> Union[JSONDictType, List[JSONDictType], Iterator[JSONDictType]]:
    """
    Parse the data (string or bytes) using the supplied parser (string or
    module object).

    This function provides a high-level API to simplify parser use. This
    function will call built-in parsers and custom plugin parsers.

    Example (standard parsers):

        >>> import jc
        >>> date_obj = jc.parse('date', 'Tue Jan 18 10:23:07 PST 2022')
        >>> print(f'The year is: {date_obj["year"]}')
        The year is: 2022

    Example (streaming parsers):

        >>> import jc
        >>> ping_gen = jc.parse('ping_s', ping_output.splitlines())
        >>> for item in ping_gen:
        >>>     print(f'Response time: {item["time_ms"]} ms')
        Response time: 102 ms
        Response time: 109 ms
        ...

    To get a list of available parser module names, use `parser_mod_list()`.

    Alternatively, a parser module object can be supplied:

        >>> import jc
        >>> import jc.parsers.date as jc_date
        >>> date_obj = jc.parse(jc_date, 'Tue Jan 18 10:23:07 PST 2022')
        >>> print(f'The year is: {date_obj["year"]}')
        The year is: 2022

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

        parser_mod_name:    (string or   name of the parser module. This
                            Module)      function will accept module_name,
                                         cli-name, and --argument-name
                                         variants of the module name.

                                         A Module object can also be passed
                                         directly or via _get_parser()

        data:               (string or   data to parse (string or bytes for
                            bytes or     standard parsers, iterable of
                            iterable)    strings for streaming parsers)

        raw:                (boolean)    output preprocessed JSON if True

        quiet:              (boolean)    suppress warning messages if True

        ignore_exceptions:  (boolean)    ignore parsing exceptions if True
                                         (streaming parsers only)

    Returns:

        Standard Parsers:   Dictionary or List of Dictionaries
        Streaming Parsers:  Generator Object containing Dictionaries
    """
    if isinstance(parser_mod_name, ModuleType):
        jc_parser = parser_mod_name
    else:
        jc_parser = _get_parser(parser_mod_name)

    if ignore_exceptions is not None:
        return jc_parser.parse(
            data,
            quiet=quiet,
            raw=raw,
            ignore_exceptions=ignore_exceptions,
            **kwargs
        )

    return jc_parser.parse(data, quiet=quiet, raw=raw, **kwargs)

def parser_mod_list(
    show_hidden: bool = False,
    show_deprecated: bool = False
) -> List[str]:
    """Returns a list of all available parser module names."""
    plist: List[str] = []
    for p in parsers:
        parser = _get_parser(p)

        if not show_hidden and _parser_is_hidden(parser):
            continue

        if not show_deprecated and _parser_is_deprecated(parser):
            continue

        plist.append(_cliname_to_modname(p))

    return plist

def plugin_parser_mod_list(
    show_hidden: bool = False,
    show_deprecated: bool = False
) -> List[str]:
    """
    Returns a list of plugin parser module names. This function is a
    subset of `parser_mod_list()`.
    """
    plist: List[str] = []
    for p in local_parsers:
        parser = _get_parser(p)

        if not show_hidden and _parser_is_hidden(parser):
            continue

        if not show_deprecated and _parser_is_deprecated(parser):
            continue

        plist.append(_cliname_to_modname(p))

    return plist

def standard_parser_mod_list(
    show_hidden: bool = False,
    show_deprecated: bool = False
) -> List[str]:
    """
    Returns a list of standard parser module names. This function is a
    subset of `parser_mod_list()` and does not contain any streaming
    parsers.
    """
    plist: List[str] = []
    for p in parsers:
        parser = _get_parser(p)

        if not _parser_is_streaming(parser):

            if not show_hidden and _parser_is_hidden(parser):
                continue

            if not show_deprecated and _parser_is_deprecated(parser):
                continue

            plist.append(_cliname_to_modname(p))

    return plist

def streaming_parser_mod_list(
    show_hidden: bool = False,
    show_deprecated: bool = False
) -> List[str]:
    """
    Returns a list of streaming parser module names. This function is a
    subset of `parser_mod_list()`.
    """
    plist: List[str] = []
    for p in parsers:
        parser = _get_parser(p)

        if _parser_is_streaming(parser):

            if not show_hidden and _parser_is_hidden(parser):
                continue

            if not show_deprecated and _parser_is_deprecated(parser):
                continue

            plist.append(_cliname_to_modname(p))

    return plist

def parser_info(
    parser_mod_name: Union[str, ModuleType],
    documentation: bool = False
) -> ParserInfoType:
    """
    Returns a dictionary that includes the parser module metadata.

    Parameters:

        parser_mod_name:    (string or   name of the parser module. This
                            Module)      function will accept module_name,
                                         cli-name, and --argument-name
                                         variants of the module name as well
                                         as a parser module object.

        documentation:      (boolean)    include parser docstring if True
    """
    if isinstance(parser_mod_name, ModuleType):
        parser_mod = parser_mod_name
        parser_mod_name = parser_mod.__name__.split('.')[-1]
    else:
        # ensure parser_mod_name is a true module name and not a cli name
        parser_mod_name = _cliname_to_modname(parser_mod_name)
        parser_mod = _get_parser(parser_mod_name)

    info_dict: ParserInfoType = {}

    if hasattr(parser_mod, 'info'):
        info_dict['name'] = parser_mod_name
        info_dict['argument'] = _parser_argument(parser_mod_name)
        parser_entry = vars(parser_mod.info)

        for k, v in parser_entry.items():
            if not k.startswith('__'):
                info_dict[k] = v  # type: ignore

        if _modname_to_cliname(parser_mod_name) in local_parsers:
            info_dict['plugin'] = True

        if documentation:
            docs = parser_mod.__doc__
            if not docs:
                docs = 'No documentation available.\n'
            info_dict['documentation'] = docs

    return info_dict

def all_parser_info(
    documentation: bool = False,
    show_hidden: bool = False,
    show_deprecated: bool = False
) -> List[ParserInfoType]:
    """
    Returns a list of dictionaries that includes metadata for all parser
    modules. By default only non-hidden, non-deprecated parsers are
    returned.

    Parameters:

        documentation:      (boolean)    include parser docstrings if True
        show_hidden:        (boolean)    also show parsers marked as hidden
                                         in their info metadata.
        show_deprecated:    (boolean)    also show parsers marked as
                                         deprecated in their info metadata.
    """
    plist: List[str] = []
    for p in parsers:
        parser = _get_parser(p)

        if not show_hidden and _parser_is_hidden(parser):
            continue

        if not show_deprecated and _parser_is_deprecated(parser):
            continue

        plist.append(_cliname_to_modname(p))

    p_info_list: List[ParserInfoType] = [parser_info(p, documentation=documentation) for p in plist]

    return p_info_list

def get_help(parser_mod_name: Union[str, ModuleType]) -> None:
    """
    Show help screen for the selected parser.

    This function will accept **module_name**, **cli-name**, and
    **--argument-name** variants of the module name string as well as a
    parser module object.
    """
    if isinstance(parser_mod_name, ModuleType):
        jc_parser = parser_mod_name
    else:
        jc_parser = _get_parser(parser_mod_name)

    help(jc_parser)
