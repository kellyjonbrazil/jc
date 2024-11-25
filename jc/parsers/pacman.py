r"""jc - JSON Convert `pacman` command output parser

Supports the following `pacman` arguments:

- `-Si`
- `-Sii`
- `-Qi`
- `-Qii`

Usage (cli):

    $ pacman -Si <package> | jc --pacman

or

    $ jc pacman -Si <package>

Usage (module):

    import jc
    result = jc.parse('pacman', pacman_command_output)

Schema:

    [
      {
        "repository":               string,
        "name":                     string,
        "version":                  string,
        "description":              string,
        "architecture":             string,
        "url":                      string,
        "licenses": [
                                    string
        ],
        "groups": [
                                    string
        ],
        "provides": [
                                    string
        ],
        "depends_on": [
                                    string
        ],
        "optional_deps": [
          {
            "name":                 string,
            "description":          string
          }
        ],
        "optional_for": [
                                    string
        ],
        "conflicts_with": [
                                    string
        ],
        "replaces": [
                                    string
        ],
        "download_size":            string,
        "installed_size":           string,
        "packager":                 string,
        "build_date":               string,
        "validated_by": [
                                    string
        ],
        "backup_files": [
                                    string
        ]
      }
    ]

Examples:

    $ pacman | jc --pacman -p
    []

    $ pacman | jc --pacman -p -r
    []
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`pacman` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command', 'file']
    magic_commands = ['pacman']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    split_fields = {
        'licenses', 'groups', 'provides', 'depends_on', 'conflicts_with',
        'replaces', 'optional_for'
    }

    space_split_fields = {
        'required_by', 'groups', 'provides', 'depends_on',
        'conflicts_with', 'replaces', 'validated_by'
    }

    two_space_fields = {'licenses', 'validated_by'}

    # initial split for field lists
    for item in proc_data:
        for key, val in item.items():
            if key in split_fields:
                if val is None:
                    item[key] = []
                else:
                    item[key] = val.split()

            # fixup for specific lists
            if key in space_split_fields and isinstance(val, List):
                val_list = [x.split() for x in val]
                item[key] = [x for xs in val_list for x in xs]  # flatten the list

            if key in two_space_fields and isinstance(val, str):
                item[key] = val.split('  ')

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
    entry_obj: Dict = {}
    multiline_fields = {'required_by', 'optional_deps', 'backup_files'}
    multiline_list: List = []
    multiline_key = ''

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            splitline = line.split(' : ', maxsplit=1)

            if len(splitline) == 2:
                # this is a key/value pair
                key, val = splitline
                key = key.strip()
                key = jc.utils.normalize_key(key)
                val = val.strip()

                # new entries can start with "Repository" or "Name"
                if (key == 'name' or key == 'repository') and len(entry_obj) > 2:
                    if multiline_list:
                        entry_obj[multiline_key] = multiline_list
                        multiline_list = []
                        multiline_key = ''
                    if entry_obj:
                        raw_output.append(entry_obj)
                    entry_obj = {}
                    entry_obj[key] = val
                    continue

                if key in multiline_fields:
                    multiline_list = []
                    if val != 'None':
                        multiline_list.append(val)
                    multiline_key = key
                    continue

                if key not in multiline_fields:
                    if multiline_list:
                        entry_obj[multiline_key] = multiline_list
                        multiline_list = []
                        multiline_key = ''
                    entry_obj[key] = val if val != 'None' else None
                    continue

            # multiline field continuation lines
            multiline_list.append(line.strip())
            continue

        # grab the last entry
        if entry_obj:
            if multiline_list:
                entry_obj[multiline_key] = multiline_list
                multiline_list = []
                multiline_key = ''
            raw_output.append(entry_obj)

    return raw_output if raw else _process(raw_output)
