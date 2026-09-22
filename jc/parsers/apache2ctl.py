r"""jc - JSON Convert `apache2ctl -S` command output parser

Parses the virtual host summary and run configuration printed by
`apache2ctl -S`, which is a synonym for
`apache2ctl -t -D DUMP_VHOSTS -D DUMP_RUN_CFG`. The `apachectl -S`,
`apache2 -S`, and `httpd -S` forms print the same output.

The whole output becomes one object. `virtual_hosts` holds one entry per
virtual host. The command prints an IP-based virtual host as a single line,
and prints name-based virtual hosts grouped under an `is a NameVirtualHost`
line. Within a group the server named by the `default server` line has
`default` set to `true`, and the aliases and wild aliases printed after a
virtual host are collected on that entry. A wildcard port stays as the
string `*` in `port`, and `port_num` is left out for it, the same way
`jc --ss` handles a wildcard port. An IPv6 address is returned without the
brackets the command prints around it.

The run configuration that follows the virtual host list is returned as
top-level fields: `server_root`, `main_document_root`, `main_error_log`,
`scoreboard_file`, `mutexes`, `pid_file`, `defines`, `user`, `group`, and
`chroot_dir`. `Define:` lines keep the `name=value` text as printed. The
`not_used` marker the command appends to `User:` and `Group:` when it is not
running as root is kept as a boolean on those objects.

Only the `-S` output is parsed. `apache2ctl -t`, `-M`, and `-V` output and
the start/stop subcommands are not supported. A virtual host line whose shape
does not match any of the forms the command prints is skipped instead of
failing the whole parse, and so is any other unrecognized line.

Usage (cli):

    $ apache2ctl -S | jc --apache2ctl

or

    $ jc apache2ctl -S

Usage (module):

    import jc
    result = jc.parse('apache2ctl', apache2ctl_command_output)

Schema:

    {
      "server_root":                     string,
      "main_document_root":              string,
      "main_error_log":                  string,
      "scoreboard_file":                 string,     # omitted if not printed
      "mutexes": [
        {
          "name":                        string,
          "using_defaults":              boolean,
          "none":                        boolean,
          "directory":                   string,     # null unless configured
          "mechanism":                   string,     # null unless configured
          "omit_pid":                    boolean
        }
      ],
      "pid_file":                        string,
      "defines": [
                                         string
      ],
      "user": {
        "name":                          string,
        "id":                            integer,
        "not_used":                      boolean
      },
      "group": {
        "name":                          string,
        "id":                            integer,
        "not_used":                      boolean
      },
      "chroot_dir":                      string,     # omitted if not printed
      "virtual_hosts": [
        {
          "address":                     string,     # '*' for a wildcard address
          "port":                        string,     # '*' for a wildcard port
          "port_num":                    integer,    # omitted when port is '*'
          "name":                        string,
          "default":                     boolean,
          "aliases": [
                                         string
          ],
          "wild_aliases": [
                                         string
          ],
          "path":                        string,
          "line":                        integer
        }
      ]
    }

Examples:

    $ apache2ctl -S | jc --apache2ctl -p
    {
      "server_root": "/etc/apache2",
      "main_document_root": "/var/www/html",
      "main_error_log": "/var/log/apache2/error.log",
      "mutexes": [
        {
          "name": "fcgid-proctbl",
          "using_defaults": true,
          "none": false,
          "directory": null,
          "mechanism": null,
          "omit_pid": false
        },
        ...
      ],
      "pid_file": "/var/run/apache2/apache2.pid",
      "defines": [
        "DUMP_VHOSTS",
        "DUMP_RUN_CFG"
      ],
      "user": {
        "name": "www-data",
        "id": 33,
        "not_used": false
      },
      "group": {
        "name": "www-data",
        "id": 33,
        "not_used": false
      },
      "virtual_hosts": [
        {
          "address": "127.0.0.1",
          "port": "80",
          "port_num": 80,
          "name": "localhost",
          "default": false,
          "aliases": [],
          "wild_aliases": [],
          "path": "/etc/apache2/sites-enabled/localhost.conf",
          "line": 4
        },
        ...
      ]
    }
"""
import re
from typing import List, Optional, Tuple
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`apache2ctl -S` command parser'
    author = 'Tung Lam'
    author_email = '53996158+tunglambk@users.noreply.github.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']
    magic_commands = ['apache2ctl -S', 'apachectl -S', 'apache2 -S', 'httpd -S']


__version__ = info.version


_vhost_marker = re.compile(r'^VirtualHost configuration:\s*$')

_vhost_header = re.compile(
    r'^(?P<address>\S+)\s+'
    r'(?:is a NameVirtualHost|(?P<name>\S+)\s+\((?P<path>.+):(?P<line>\d+)\))\s*$'
)

_default_server = re.compile(
    r'^\s*default server\s+(?P<name>\S+)\s+\((?P<path>.+):(?P<line>\d+)\)\s*$'
)

_name_vhost = re.compile(
    r'^\s*port\s+(?P<port>\S+)\s+namevhost\s+(?P<name>\S+)\s+'
    r'\((?P<path>.+):(?P<line>\d+)\)\s*$'
)

_wild_alias = re.compile(r'^\s*wild alias\s+(?P<name>\S+)\s*$')
_alias = re.compile(r'^\s*alias\s+(?P<name>\S+)\s*$')

_quoted_value = re.compile(
    r'^[A-Za-z][A-Za-z ]*:\s*"(?P<value>[^"]*)"(?P<not_used>\s+not_used)?\s*$'
)

_user_group = re.compile(
    r'^[A-Za-z]+:\s+name="(?P<name>[^"]*)"\s+id=(?P<id>\d+)'
    r'(?P<not_used>\s+not_used)?\s*$'
)

_mutex = re.compile(r'^Mutex\s+(?P<name>\S+):\s+(?P<value>.*?)\s*$')
_mutex_directory = re.compile(r'dir="(?P<directory>[^"]*)"')
_mutex_mechanism = re.compile(r'mechanism=(?P<mechanism>\S+)')

_run_config_prefixes = (
    'ServerRoot:',
    'Main DocumentRoot:',
    'Main ErrorLog:',
    'ScoreBoardFile:',
    'Mutex ',
    'PidFile:',
    'Define:',
    'User:',
    'Group:',
    'ChrootDir:'
)


def _is_run_config(line: str) -> bool:
    """Return `True` when the line belongs to the run configuration block."""
    return line.startswith(_run_config_prefixes)


def _split_address_port(text: str) -> Optional[Tuple[str, str]]:
    """
    Split an `address:port` token from a virtual host line. IPv6 addresses
    are bracketed by the command, so the brackets are removed. Returns
    `None` when the token has no usable address or port.
    """
    if not text:
        return None

    if text.startswith('['):
        end = text.find(']')

        if end < 2 or end + 1 >= len(text) or text[end + 1] != ':':
            return None

        address = text[1:end]
        port = text[end + 2:]
    else:
        address, separator, port = text.rpartition(':')

        if not separator:
            return None

    if not address or not port:
        return None

    return address, port


def _new_vhost(address: str, port: str, name: str, path: str, line: str) -> JSONDictType:
    """Create a virtual host object."""
    return {
        'address': address,
        'port': port,
        'name': name,
        'default': False,
        'aliases': [],
        'wild_aliases': [],
        'path': path,
        'line': line
    }


def _mark_default(virtual_hosts: List[JSONDictType], default_key: Tuple[str, str, str]) -> None:
    """
    Mark the virtual host named by a `default server` line. A server can be
    the default in more than one address group, so every match is marked.
    """
    name, path, line = default_key

    for vhost in virtual_hosts:
        if vhost['name'] == name and vhost['path'] == path and vhost['line'] == line:
            vhost['default'] = True


def _parse_mutex(line: str) -> Optional[JSONDictType]:
    """
    Parse a `Mutex <name>: ...` line. The command prints one of
    `using_defaults`, `none`, or `dir="..." mechanism=... [OmitPid]`.
    Returns `None` for a line that matches none of those.
    """
    match = _mutex.match(line)

    if not match:
        return None

    value = match.group('value')
    mutex: JSONDictType = {
        'name': match.group('name'),
        'using_defaults': False,
        'none': False,
        'directory': None,
        'mechanism': None,
        'omit_pid': False
    }

    if value == 'using_defaults':
        mutex['using_defaults'] = True
        return mutex

    if value == 'none':
        mutex['none'] = True
        return mutex

    directory_match = _mutex_directory.search(value)
    mechanism_match = _mutex_mechanism.search(value)

    if not directory_match and not mechanism_match:
        return None

    if directory_match:
        mutex['directory'] = directory_match.group('directory')

    if mechanism_match:
        mutex['mechanism'] = mechanism_match.group('mechanism')

    mutex['omit_pid'] = '[OmitPid]' in value

    return mutex


def _parse_user_group(line: str) -> Optional[JSONDictType]:
    """Parse a `User:` or `Group:` line."""
    match = _user_group.match(line)

    if not match:
        return None

    return {
        'name': match.group('name'),
        'id': match.group('id'),
        'not_used': bool(match.group('not_used'))
    }


def _parse_quoted_value(line: str) -> Optional[str]:
    """Return the quoted value from a run configuration line."""
    match = _quoted_value.match(line)

    if not match:
        return None

    return match.group('value')


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    for vhost in proc_data.get('virtual_hosts', []):
        vhost['line'] = jc.utils.convert_to_int(vhost['line'])
        port_num = jc.utils.convert_to_int(vhost['port'])

        if port_num is not None:
            vhost['port_num'] = port_num

    for key in ('user', 'group'):
        if key in proc_data:
            proc_data[key]['id'] = jc.utils.convert_to_int(proc_data[key]['id'])

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

    raw_output: JSONDictType = {}
    virtual_hosts: List[JSONDictType] = []
    mutexes: List[JSONDictType] = []
    defines: List[str] = []

    if jc.utils.has_data(data):
        in_vhosts = False
        address: Optional[str] = None
        current_vhost: Optional[JSONDictType] = None
        default_key: Optional[Tuple[str, str, str]] = None

        for line in data.splitlines():
            if _vhost_marker.match(line):
                in_vhosts = True
                address = None
                current_vhost = None
                default_key = None
                continue

            if not line.strip():
                continue

            if in_vhosts and not _is_run_config(line):
                default_match = _default_server.match(line)

                if default_match:
                    default_key = (
                        default_match.group('name'),
                        default_match.group('path'),
                        default_match.group('line')
                    )
                    _mark_default(virtual_hosts, default_key)
                    continue

                name_vhost_match = _name_vhost.match(line)

                if name_vhost_match:
                    if address is None:
                        # namevhost without a group header
                        current_vhost = None
                        continue

                    vhost = _new_vhost(
                        address,
                        name_vhost_match.group('port'),
                        name_vhost_match.group('name'),
                        name_vhost_match.group('path'),
                        name_vhost_match.group('line')
                    )
                    virtual_hosts.append(vhost)
                    current_vhost = vhost

                    if default_key:
                        _mark_default(virtual_hosts, default_key)

                    continue

                wild_alias_match = _wild_alias.match(line)

                if wild_alias_match:
                    if current_vhost is not None:
                        current_vhost['wild_aliases'].append(wild_alias_match.group('name'))
                    continue

                alias_match = _alias.match(line)

                if alias_match:
                    if current_vhost is not None:
                        current_vhost['aliases'].append(alias_match.group('name'))
                    continue

                header_match = _vhost_header.match(line)

                if header_match:
                    split = _split_address_port(header_match.group('address'))
                    current_vhost = None
                    default_key = None

                    if split is None:
                        continue

                    if header_match.group('name') is None:
                        # NameVirtualHost group: the address applies to the
                        # `namevhost` lines that follow
                        address = split[0]
                    else:
                        address = None
                        virtual_hosts.append(_new_vhost(
                            split[0],
                            split[1],
                            header_match.group('name'),
                            header_match.group('path'),
                            header_match.group('line')
                        ))

                    continue

                # a virtual host line we cannot parse
                current_vhost = None
                continue

            in_vhosts = False

            if line.startswith('Mutex '):
                mutex = _parse_mutex(line)

                if mutex is not None:
                    mutexes.append(mutex)

            elif line.startswith('Define:'):
                defines.append(line.split(':', 1)[1].strip())

            elif line.startswith('User:') or line.startswith('Group:'):
                user_group = _parse_user_group(line)

                if user_group is not None:
                    raw_output['user' if line.startswith('User:') else 'group'] = user_group

            else:
                quoted_value = _parse_quoted_value(line)

                if quoted_value is None:
                    continue

                if line.startswith('ServerRoot:'):
                    raw_output['server_root'] = quoted_value

                elif line.startswith('Main DocumentRoot:'):
                    raw_output['main_document_root'] = quoted_value

                elif line.startswith('Main ErrorLog:'):
                    raw_output['main_error_log'] = quoted_value

                elif line.startswith('ScoreBoardFile:'):
                    raw_output['scoreboard_file'] = quoted_value

                elif line.startswith('PidFile:'):
                    raw_output['pid_file'] = quoted_value

                elif line.startswith('ChrootDir:'):
                    raw_output['chroot_dir'] = quoted_value

        raw_output['virtual_hosts'] = virtual_hosts
        raw_output['mutexes'] = mutexes
        raw_output['defines'] = defines

    return raw_output if raw else _process(raw_output)
