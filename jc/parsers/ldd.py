r"""jc - JSON Convert `ldd` command output parser

Supports the `-v` option or no options, and one or more `FILE`
arguments. `file` is `null` when only a single file was given, since
`ldd` doesn't echo the filename back in that case. `version_info` is
only populated when `-v` is used. Lines that aren't a recognized
dependency or version requirement (e.g. `not a dynamic executable`)
are skipped.

Usage (cli):

    $ ldd /bin/ls | jc --ldd

or

    $ jc ldd /bin/ls

Usage (module):

    import jc
    result = jc.parse('ldd', ldd_command_output)

Schema:

    [
      {
        "file":           string/null,
        "dependencies": [
          {
            "name":       string,
            "path":       string/null,  # [0]
            "address":    string/null   # [0]
          }
        ],
        "version_info": [
          {
            "for":        string,
            "requires": [
              {
                "name":     string,
                "version":  string,
                "path":     string
              }
            ]
          }
        ]
      }
    ]

    [0] null if the library was not found, or if `name` is itself the
        resolved path (e.g. the dynamic linker)

Examples:

    $ ldd /bin/ls | jc --ldd -p
    [
      {
        "file": null,
        "dependencies": [
          {
            "name": "linux-vdso.so.1",
            "path": null,
            "address": "0x00007fe5c22ef000"
          },
          {
            "name": "libselinux.so.1",
            "path": "/lib64/libselinux.so.1",
            "address": "0x00007fe5c2287000"
          },
          {
            "name": "libc.so.6",
            "path": "/lib64/libc.so.6",
            "address": "0x00007fe5c207f000"
          },
          {
            "name": "/lib64/ld-linux-x86-64.so.2",
            "path": null,
            "address": "0x00007fe5c22f1000"
          }
        ],
        "version_info": []
      }
    ]

    $ ldd -v /bin/ls /bin/cat | jc --ldd -p
    [
      {
        "file": "/bin/ls",
        "dependencies": [
          ...
        ],
        "version_info": [
          {
            "for": "/bin/ls",
            "requires": [
              {
                "name": "libselinux.so.1",
                "version": "LIBSELINUX_1.0",
                "path": "/lib64/libselinux.so.1"
              }
            ]
          }
        ]
      },
      {
        "file": "/bin/cat",
        "dependencies": [
          ...
        ],
        "version_info": [
          ...
        ]
      }
    ]
"""
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`ldd` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['ldd']
    tags = ['command']


__version__ = info.version

_ARROW_LINE = re.compile(r'^(?P<name>\S+)\s*=>\s*(?P<rest>.+)$')
_PATH_AND_ADDRESS = re.compile(r'^(?P<path>\S+)\s*\((?P<address>0x[0-9a-fA-F]+)\)$')
_NAME_AND_ADDRESS = re.compile(r'^(?P<name>\S+)\s*\((?P<address>0x[0-9a-fA-F]+)\)$')
_VERSION_INFO_HEADER = 'Version information:'
_VERSION_OBJECT = re.compile(r'^(?P<obj>\S+):$')
_VERSION_REQUIREMENT = re.compile(r'^(?P<name>\S+)\s*\((?P<version>[^)]+)\)\s*=>\s*(?P<path>\S+)$')
_FILE_HEADER = re.compile(r'^(?P<file>\S+):$')


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    # no additional processing needed
    return proc_data


def parse(data, raw=False, quiet=False):
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

    raw_output = []
    current_file = None
    current_object = None
    in_version_info = False

    def ensure_current_file():
        nonlocal current_file
        if current_file is None:
            current_file = {'file': None, 'dependencies': [], 'version_info': []}
            raw_output.append(current_file)
        return current_file

    if jc.utils.has_data(data):
        for line in data.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            # a file header (only present when multiple FILEs are given)
            # is the only content printed at zero indentation
            indented = line[:1] in (' ', '\t')
            if not indented:
                file_match = _FILE_HEADER.match(stripped)
                if file_match:
                    current_file = {
                        'file': file_match.group('file'),
                        'dependencies': [],
                        'version_info': [],
                    }
                    raw_output.append(current_file)
                    current_object = None
                    in_version_info = False
                    continue

            if stripped == _VERSION_INFO_HEADER:
                in_version_info = True
                continue

            if in_version_info:
                object_match = _VERSION_OBJECT.match(stripped)
                if object_match:
                    current_object = {'for': object_match.group('obj'), 'requires': []}
                    ensure_current_file()['version_info'].append(current_object)
                    continue

                if current_object is not None:
                    requirement_match = _VERSION_REQUIREMENT.match(stripped)
                    if requirement_match:
                        current_object['requires'].append({
                            'name': requirement_match.group('name'),
                            'version': requirement_match.group('version'),
                            'path': requirement_match.group('path'),
                        })
                continue

            arrow_match = _ARROW_LINE.match(stripped)
            if arrow_match:
                name = arrow_match.group('name')
                rest = arrow_match.group('rest').strip()

                if rest == 'not found':
                    ensure_current_file()['dependencies'].append({'name': name, 'path': None, 'address': None})
                    continue

                path_match = _PATH_AND_ADDRESS.match(rest)
                if path_match:
                    ensure_current_file()['dependencies'].append({
                        'name': name,
                        'path': path_match.group('path'),
                        'address': path_match.group('address'),
                    })
                continue

            name_match = _NAME_AND_ADDRESS.match(stripped)
            if name_match:
                ensure_current_file()['dependencies'].append({
                    'name': name_match.group('name'),
                    'path': None,
                    'address': name_match.group('address'),
                })

    return raw_output if raw else _process(raw_output)
