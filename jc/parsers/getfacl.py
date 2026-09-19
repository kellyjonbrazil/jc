r"""jc - JSON Convert `getfacl` command output parser

Parses the default (non-tabular) `getfacl` output. The file name, owner, and
owning group from the comment header are included on every entry, along with
the setuid/setgid/sticky `# flags` value when `getfacl` prints that line.

Each ACL entry is returned as a separate item. The `effective` field is
populated from the `#effective` comment, which is only printed when the
effective rights differ from the entry's own rights unless `getfacl -e` is
used. `default` is `true` for entries in a directory's default ACL.

The `-t`/`--tabular` output format is not supported.

Usage (cli):

    $ getfacl file.txt | jc --getfacl

or

    $ jc getfacl file.txt

Usage (module):

    import jc
    result = jc.parse('getfacl', getfacl_command_output)

Schema:

    [
      {
        "file":         string/null,
        "owner":        string/null,
        "group":        string/null,
        "flags":        string/null,
        "type":         string,
        "name":         string/null,
        "permissions":  string,
        "effective":    string/null,
        "default":      boolean
      }
    ]

Examples:

    $ getfacl file.txt | jc --getfacl -p
    [
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "user",
        "name": null,
        "permissions": "rw-",
        "effective": null,
        "default": false
      },
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "user",
        "name": "root",
        "permissions": "rwx",
        "effective": "r--",
        "default": false
      },
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "group",
        "name": null,
        "permissions": "rw-",
        "effective": "r--",
        "default": false
      },
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "mask",
        "name": null,
        "permissions": "r--",
        "effective": null,
        "default": false
      },
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "other",
        "name": null,
        "permissions": "r--",
        "effective": null,
        "default": false
      }
    ]

    $ getfacl dir | jc --getfacl -p
    [
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "user",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "user",
        "name": "root",
        "permissions": "r-x",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "group",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "mask",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "other",
        "name": null,
        "permissions": "r-x",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "user",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": true
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "user",
        "name": "root",
        "permissions": "rwx",
        "effective": null,
        "default": true
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "group",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": true
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "mask",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": true
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "other",
        "name": null,
        "permissions": "r-x",
        "effective": null,
        "default": true
      }
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`getfacl` command parser'
    author = 'Tung Lam'
    author_email = '53996158+tunglambk@users.noreply.github.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['getfacl']


__version__ = info.version

# fields from the `# key: value` comment header. The `# file` line starts a
# new ACL block, so the remaining fields are reset when it is seen.
_header_fields = ('file', 'owner', 'group', 'flags')

_entry_re = re.compile(
    r'^(?P<default>default:)?'
    r'(?P<type>user|group|mask|other):'
    r'(?P<name>[^:]*):'
    r'(?P<permissions>[r-][w-][x-])$'
)
_effective_re = re.compile(r'^effective:(?P<effective>[r-][w-][x-])$')


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
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
        header: Dict = {field: None for field in _header_fields}

        for line in data.splitlines():
            line = line.strip()

            if not line:
                continue

            if line.startswith('#'):
                key, _, value = line.partition(':')
                field = key.lstrip('#').strip()

                if field in header:
                    if field == 'file':
                        header = {field: None for field in _header_fields}
                    header[field] = value.strip() or None

                continue

            entry, _, comment = line.partition('#')
            match = _entry_re.match(entry.rstrip())

            if not match:
                continue

            effective = None
            effective_match = _effective_re.match(comment.strip())

            if effective_match:
                effective = effective_match.group('effective')

            raw_output.append({
                'file': header['file'],
                'owner': header['owner'],
                'group': header['group'],
                'flags': header['flags'],
                'type': match.group('type'),
                'name': match.group('name') or None,
                'permissions': match.group('permissions'),
                'effective': effective,
                'default': bool(match.group('default')),
            })

    return raw_output if raw else _process(raw_output)
