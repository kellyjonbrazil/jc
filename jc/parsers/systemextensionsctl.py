r"""jc - JSON Convert `systemextensionsctl list` command output parser

Usage (cli):

    $ systemextensionsctl list | jc --systemextensionsctl

or

    $ jc systemextensionsctl list

Usage (module):

    import jc
    result = jc.parse('systemextensionsctl', systemextensionsctl_command_output)

Schema:

    [
      {
        "category":                 string,
        "enabled":                  boolean,
        "active":                   boolean,
        "team_id":                  string/null,
        "bundle_id":                string,
        "version":                  string,
        "build":                    string,
        "name":                     string,
        "state":                    string
      }
    ]

Examples:

    $ systemextensionsctl list | jc --systemextensionsctl -p
    [
      {
        "category": "com.apple.system_extension.network_extension",
        "enabled": true,
        "active": true,
        "team_id": "TZ3UEPFYKD",
        "bundle_id": "com.checkpoint.fw.filter",
        "version": "871010711",
        "build": "6",
        "name": "Check Point Firewall",
        "state": "activated enabled"
      },
      {
        "category": "com.apple.system_extension.network_extension",
        "enabled": true,
        "active": true,
        "team_id": "UBF8T346G9",
        "bundle_id": "com.microsoft.wdav.netext",
        "version": "101.47.27",
        "build": "101.47.27",
        "name": "Microsoft Defender ATP Network Extension",
        "state": "activated enabled"
      },
      {
        "category": "com.apple.system_extension.endpoint_security",
        "enabled": true,
        "active": true,
        "team_id": "UBF8T346G9",
        "bundle_id": "com.microsoft.wdav.epsext",
        "version": "101.47.27",
        "build": "101.47.27",
        "name": "Microsoft Defender ATP Endpoint Security Extension",
        "state": "activated enabled"
      },
      {
        "category": "com.apple.system_extension.driver_extension",
        "enabled": true,
        "active": true,
        "team_id": "G43BCU2T37",
        "bundle_id": "org.pqrs.Karabiner-DriverKit-VirtualHIDDevice",
        "version": "1.0.0",
        "build": "1.0.0",
        "name": "org.pqrs.Karabiner-DriverKit-VirtualHIDDevice",
        "state": "activated enabled"
      }
    ]

    $ systemextensionsctl list | jc --systemextensionsctl -p -r
    [
      {
        "category": "com.apple.system_extension.network_extension",
        "enabled": "*",
        "active": "*",
        "team_id": "TZ3UEPFYKD",
        "bundle_id": "com.checkpoint.fw.filter",
        "version": "871010711",
        "build": "6",
        "name": "Check Point Firewall",
        "state": "activated enabled"
      },
      ...
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
from jc.exceptions import ParseError
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`systemextensionsctl list` command parser'
    author = 'Ron Green'
    author_email = '11993626+georgettica@users.noreply.github.com'
    compatible = ['darwin']
    magic_commands = ['systemextensionsctl list']
    tags = ['command']


__version__ = info.version


# `--- com.apple.system_extension.network_extension` and, on newer macOS, a
# description in parentheses after it
_CATEGORY_RE = re.compile(r'--- (?P<category>\S+)')
# `org.example.extension (1.2/3)`: the version and build number
_BUNDLE_RE = re.compile(r'(?P<bundle_id>.*\S) \((?P<version>[^/()]*)/(?P<build>[^/()]*)\)')


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for entry in proc_data:
        entry['enabled'] = entry['enabled'] == '*'
        entry['active'] = entry['active'] == '*'

        if entry['team_id'] == '-':
            entry['team_id'] = None

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
    category = None

    if jc.utils.has_data(data):

        for line in filter(None, jc.utils.splitlines(data)):
            # the `N extension(s)` total and the column header lines
            if line.endswith(' extension(s)') or line.startswith('enabled\tactive\t'):
                continue

            category_match = _CATEGORY_RE.match(line)
            if category_match:
                category = category_match.group('category')
                continue

            fields = line.split('\t')
            bundle = _BUNDLE_RE.fullmatch(fields[3]) if len(fields) == 6 else None
            if not category or not bundle:
                raise ParseError(f'Unexpected line: {line}')

            raw_output.append({
                'category': category,
                'enabled': fields[0],
                'active': fields[1],
                'team_id': fields[2],
                'bundle_id': bundle.group('bundle_id'),
                'version': bundle.group('version'),
                'build': bundle.group('build'),
                'name': fields[4],
                'state': fields[5].strip('[]')
            })

    return raw_output if raw else _process(raw_output)
