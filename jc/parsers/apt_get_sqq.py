r"""jc - JSON Convert `apt-get -sqq` command output parser

Requires the `-sqq` options in `apt-get`.

Usage (cli):

    $ apt-get -sqq upgrade | jc --apt-get-sqq

or

    $ jc apt-get -sqq full-upgrade

Usage (module):

    import jc
    result = jc.parse('apt_get_sqq', apt_get_sqq_command_output)

Schema:

    [
      {
        "operation":            string,       # configure, remove, or unpack
        "package":              string,
        "broken":               string/null,
        "proposed_pkg_ver":     string,
        "existing_pkg_ver":     string/null,
        "architecture":         string
      }
    ]

Examples:

    $ apt-get -sqq upgrade | jc --apt-get-sqq -p
    [
      {
        "operation": "unpack",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "unpack",
        "package": "dpkg",
        "broken": null,
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "configure",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "remove",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "unpack",
        "package": "base-files",
        "broken": "10.3+deb10u4",
        "proposed_pkg_ver": "10.3+deb10u13 Debian:10.13/oldstable",
        "existing_pkg_ver": null,
        "architecture": "amd64"
      },
      {
        "operation": "configure",
        "package": "base-files",
        "broken": null,
        "proposed_pkg_ver": "10.3+deb10u13 Debian:10.13/oldstable",
        "existing_pkg_ver": null,
        "architecture": "amd64"
      },
      {
        "operation": "unpack",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "configure",
        "package": "dpkg",
        "broken": null,
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      }
    ]

    $ apt-get -sqq upgrade | jc --apt-get-sqq -p -r
    [
      {
        "operation": "Inst",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Inst",
        "package": "dpkg",
        "broken": null,
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Conf",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Remv",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Inst",
        "package": "base-files",
        "broken": "10.3+deb10u4",
        "proposed_pkg_ver": "10.3+deb10u13 Debian:10.13/oldstable",
        "existing_pkg_ver": null,
        "architecture": "amd64"
      },
      {
        "operation": "Conf",
        "package": "base-files",
        "broken": null,
        "proposed_pkg_ver": "10.3+deb10u13 Debian:10.13/oldstable",
        "existing_pkg_ver": null,
        "architecture": "amd64"
      },
      {
        "operation": "Inst",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Conf",
        "package": "dpkg",
        "broken": null,
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      }
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`apt-get -sqq` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['apt-get -sqq']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    op_map = {
        'Conf': 'configure',
        'Remv': 'remove',
        'Inst': 'unpack'
    }

    for item in proc_data:
        if 'operation' in item and item['operation']:
            item['operation'] = op_map[item['operation']]

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

    if jc.utils.has_data(data):

        # Inst dpkg [1.19.7] (1.19.8 Debian:10.13/oldstable, Debian-Security:10/oldstable [amd64])
        #  |    |     |                       |                        |                    \architecture
        #  |    |     |                       |                         \existing_pkg_ver (optional)
        #  |    |     |                        \proposed_pkg_ver
        #  |    |      \broken (optional)
        #  |     \package
        #   \operation (configure, remove, or unpack)

        line_re = re.compile(r'(?P<operation>Inst|Conf|Remv)\s(?P<package>\S+)(?P<broken>\s+\[\S*?\])?\s\((?P<packages_pe>.*?)\[(?P<architecture>\w*)\]\)')

        for line in filter(None, data.splitlines()):
            broken_val = None
            packages_pe = None
            proposed_pkg_ver = None
            existing_pkg_ver = None
            parsed_line = line_re.match(line)

            if parsed_line:
                parsed_dict = parsed_line.groupdict()

                if parsed_dict['broken']:
                    broken_val = parsed_dict['broken'].strip()[1:-1]

                if parsed_dict['packages_pe']:
                    packages_pe = parsed_dict['packages_pe'].split(',')
                    proposed_pkg_ver = packages_pe[0].strip()
                    if len(packages_pe) == 2:
                        existing_pkg_ver = packages_pe[1].strip()

                output_line = {
                    'operation': parsed_dict['operation'],
                    'package': parsed_dict['package'],
                    'broken': broken_val,
                    'proposed_pkg_ver': proposed_pkg_ver,
                    'existing_pkg_ver': existing_pkg_ver,
                    'architecture': parsed_dict['architecture']
                }

                raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
