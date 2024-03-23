r"""jc - JSON Convert Alpine Linux Package Index files

Usage (cli):

    $ cat APKINDEX | jc --pkg-index-apk

Usage (module):

    import jc
    result = jc.parse('pkg_index_apk', pkg_index_apk_output)

Schema:

    [
      {
        "checksum":             string,
        "package":              string,
        "version":              string,
        "architecture":         string,
        "package_size":         integer,
        "installed_size":       integer,
        "description":          string,
        "url":                  string,
        "license":              string,
        "origin":               string,
        "maintainer": {
          "name":               string,
          "email":              string,
        },
        "build_time":           integer,
        "commit":               string,
        "provider_priority":    string,
        "dependencies": [
                                string
        ],
        "provides": [
                                string
        ],
        "install_if": [
                                string
        ],
      }
    ]

Example:

    $ cat APKINDEX | jc --pkg-index-apk
    [
      {
        "checksum": "Q1znBl9k+RKgY6gl5Eg3iz73KZbLY=",
        "package": "yasm",
        "version": "1.3.0-r4",
        "architecture": "x86_64",
        "package_size": 772109,
        "installed_size": 1753088,
        "description": "A rewrite of NASM to allow for multiple synta...",
        "url": "http://www.tortall.net/projects/yasm/",
        "license": "BSD-2-Clause",
        "origin": "yasm",
        "maintainer": {
          "name": "Natanael Copa",
          "email": "ncopa@alpinelinux.org"
        },
        "build_time": 1681228881,
        "commit": "84a227baf001b6e0208e3352b294e4d7a40e93de",
        "dependencies": [
          "so:libc.musl-x86_64.so.1"
        ],
        "provides": [
          "cmd:vsyasm=1.3.0-r4",
          "cmd:yasm=1.3.0-r4",
          "cmd:ytasm=1.3.0-r4"
        ]
      }
    ]

    $ cat APKINDEX | jc --pkg-index-apk --raw
    [
      {
        "C": "Q1znBl9k+RKgY6gl5Eg3iz73KZbLY=",
        "P": "yasm",
        "V": "1.3.0-r4",
        "A": "x86_64",
        "S": "772109",
        "I": "1753088",
        "T": "A rewrite of NASM to allow for multiple syntax supported...",
        "U": "http://www.tortall.net/projects/yasm/",
        "L": "BSD-2-Clause",
        "o": "yasm",
        "m": "Natanael Copa <ncopa@alpinelinux.org>",
        "t": "1681228881",
        "c": "84a227baf001b6e0208e3352b294e4d7a40e93de",
        "D": "so:libc.musl-x86_64.so.1",
        "p": "cmd:vsyasm=1.3.0-r4 cmd:yasm=1.3.0-r4 cmd:ytasm=1.3.0-r4"
      },
    ]
"""
import re
from typing import List, Dict, Union
import jc.utils


class info:
    """Provides parser metadata (version, author, etc.)"""
    version = "1.0"
    description = "Alpine Linux Package Index file parser"
    author = "Roey Darwish Dror"
    author_email = "roey.ghost@gmail.com"
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


_KEY = {
    "C": "checksum",
    "P": "package",
    "V": "version",
    "A": "architecture",
    "S": "package_size",
    "I": "installed_size",
    "T": "description",
    "U": "url",
    "L": "license",
    "o": "origin",
    "m": "maintainer",
    "t": "build_time",
    "c": "commit",
    "k": "provider_priority",
    "D": "dependencies",
    "p": "provides",
    "i": "install_if"
}

def _value(key: str, value: str) -> Union[str, int, List[str], Dict[str, str]]:
    """
    Convert value to the appropriate type

    Parameters:

        key:         (string)  key name
        value:       (string)  value to convert

    Returns:

        Converted value
    """
    if key in ['S', 'I', 't', 'k']:
        return int(value)

    if key in ['D', 'p', 'i']:
        splitted = value.split(' ')
        return splitted

    if key == "m":
        m = re.match(r'(.*) <(.*)>', value)
        if m:
            return {'name': m.group(1), 'email': m.group(2)}
        else:
            return {'name': value}

    return value


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return [{_KEY.get(k, k): _value(k, v) for k, v in d.items()} for d in proc_data]


def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]:
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

    raw_output: List[dict] = []

    package: Dict = {}
    if jc.utils.has_data(data):
        lines = iter(data.splitlines())
        for line in lines:
            line = line.strip()
            if not line:
                if package:
                    raw_output.append(package)
                    package = {}

                continue

            key = line[0]
            value = line[2:].strip()
            assert key not in package
            package[key] = value

    if package:
        raw_output.append(package)

    return raw_output if raw else _process(raw_output)
