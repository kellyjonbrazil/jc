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
        "file":               string/null,
        "dependencies": [
          {
            "name":           string,
            "path":           string/null,  # [0]
            "address":        string/null   # [0]
          }
        ],
        "version_info": [
          {
            "for":            string,
            "requires": [
              {
                "name":       string,
                "version":    string,
                "path":       string
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
    version = '1.1'
    description = '`ldd` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['ldd']
    tags = ['command']


__version__ = info.version

_ADDRESS = re.compile(r'0x[0-9a-fA-F]+')
_VERSION_INFO_HEADER = 'Version information:'
_VERSION_OBJECT = re.compile(r'^(?P<obj>.+):$')
_FILE_HEADER = re.compile(r'^(?P<file>.+):$')


def _split_address(text):
    """
    Split `<text> (0x...)` into the text and the address. Returns None if
    `text` does not end with a parenthesized hex address or has nothing in
    front of it. The text may contain spaces. Only string methods are used
    so the cost is linear in the length of the line.
    """
    if not text.endswith(')'):
        return None

    idx = text.rfind('(')
    if idx < 1:
        return None

    address = text[idx + 1:-1]
    head = text[:idx].rstrip()
    if not head or not _ADDRESS.fullmatch(address):
        return None

    return head, address


def _split_requirement(text):
    """
    Split `<name> (<version>) => <path>` into name, version and path. The
    name and path may contain spaces. Returns None if the line is not a
    requirement.
    """
    left, arrow, path = text.partition('=>')
    left = left.rstrip()
    path = path.strip()

    # a `not found` requirement has no path to report and is skipped, as
    # it was when the path had to be a single token
    if not arrow or not path or path == 'not found' or not left.endswith(')'):
        return None

    idx = left.rfind('(')
    if idx < 1 or not left[idx - 1].isspace():
        return None

    name = left[:idx].rstrip()
    version = left[idx + 1:-1]
    if not name or not version or ')' in version:
        return None

    return name, version, path


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
        for line in jc.utils.splitlines(data):
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
                    requirement = _split_requirement(stripped)
                    if requirement:
                        current_object['requires'].append({
                            'name': requirement[0],
                            'version': requirement[1],
                            'path': requirement[2],
                        })
                continue

            name, arrow, rest = stripped.partition('=>')
            name = name.rstrip()
            if arrow and name:
                rest = rest.strip()

                if rest == 'not found':
                    ensure_current_file()['dependencies'].append({'name': name, 'path': None, 'address': None})
                    continue

                path_match = _split_address(rest)
                if path_match:
                    ensure_current_file()['dependencies'].append({
                        'name': name,
                        'path': path_match[0],
                        'address': path_match[1],
                    })
                continue

            name_match = _split_address(stripped)
            if name_match:
                ensure_current_file()['dependencies'].append({
                    'name': name_match[0],
                    'path': None,
                    'address': name_match[1],
                })

    return raw_output if raw else _process(raw_output)
