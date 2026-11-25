r"""jc - JSON Convert `findmnt` command output parser

Supports `-a`, `-l`, or no `findmnt` options.

> Note: Newer versions of `findmnt` have a JSON output option.

> Note: Names that contain wide (e.g. CJK) characters can misalign the
> columns. Use `findmnt -l` or `findmnt -J` for those.

Usage (cli):

    $ findmnt | jc --findmnt

or

    $ jc findmnt

Usage (module):

    import jc
    result = jc.parse('findmnt', findmnt_command_output)

Schema:

    [
      {
        "target":                   string,
        "source":                   string,
        "fstype":                   string,
        "options": [
                                    string
        ],
        "kv_options": {
          "<key_name>":             string
        }
    ]

Examples:

    $ findmnt | jc --findmnt -p
    [
      {
        "target": "/",
        "source": "/dev/mapper/centos-root",
        "fstype": "xfs",
        "options": [
          "rw",
          "relatime",
          "seclabel",
          "attr2",
          "inode64",
          "noquota"
        ]
      },
      {
        "target": "/sys/fs/cgroup",
        "source": "tmpfs",
        "fstype": "tmpfs",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "noexec",
          "seclabel"
        ],
        "kv_options": {
          "mode": "755"
        }
      },
      ...
    ]

    $ findmnt | jc --findmnt -p -r
    [
      {
        "target": "/",
        "source": "/dev/mapper/centos-root",
        "fstype": "xfs",
        "options": "rw,relatime,seclabel,attr2,inode64,noquota"
      },
      {
        "target": "/sys/fs/cgroup",
        "source": "tmpfs",
        "fstype": "tmpfs",
        "options": "ro,nosuid,nodev,noexec,seclabel,mode=755"
      },
      ...
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
from jc.parsers.universal import simple_table_parse, sparse_table_parse
from jc.parsers.mount import _split_options
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`findmnt` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['findmnt']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    # split normal options and k/v options
    for item in proc_data:
        reg_options = []
        kv_options = {}

        if item.get('options'):
            opt_list = _split_options(item['options'])

            for option in opt_list:
                if '=' in option:
                    k, v = option.split('=', maxsplit=1)

                    # remove one pair of quotes around the value
                    if len(v) > 1 and v.startswith('"') and v.endswith('"'):
                        v = v[1:-1]

                    kv_options[k] = v

                else:
                    reg_options.append(option)

            if reg_options:
                item['options'] = reg_options
            if kv_options:
                item['kv_options'] = kv_options

    return proc_data


def _replace(matchobj):
    if matchobj:
        matchlen = len(matchobj.group(1))
        return ' ' * matchlen + '/'
    return ''


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
    table: List[str] = []

    if jc.utils.has_data(data):

        for line in filter(None, jc.utils.splitlines(data)):
            # remove initial drawing characters
            line = re.sub(r'^([│ ├─└─|`-]+)/', _replace, line, count=1)
            table.append(line)

        table[0] = table[0].lower()

        # `findmnt -r` separates the columns with a single space and escapes
        # spaces in values. Otherwise the columns are aligned under the
        # header and values can contain spaces, so use the column positions.
        # Aligned headers can also be one space apart when no value is
        # wider than its column name: then a row with more space-separated
        # fields than the header has a value with spaces in it.
        header_count = len(table[0].split())
        if '  ' in table[0].strip() or any(
                len([x for x in row.split(' ') if x]) > header_count for row in table[1:]):
            raw_output = sparse_table_parse(table, delim='\x00')
        else:
            raw_output = simple_table_parse(table)

    return raw_output if raw else _process(raw_output)
