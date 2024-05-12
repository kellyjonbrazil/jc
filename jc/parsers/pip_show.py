r"""jc - JSON Convert `pip-show` command output parser

Usage (cli):

    $ pip show | jc --pip-show

or

    $ jc pip show

Usage (module):

    import jc
    result = jc.parse('pip_show', pip_show_command_output)

Schema:

    [
      {
        "name":             string,
        "version":          string,
        "summary":          string,
        "home_page":        string,
        "author":           string,
        "author_email":     string,
        "license":          string,
        "location":         string,
        "requires":         string,
        "required_by":      string
      }
    ]

Examples:

    $ pip show wrapt jc wheel | jc --pip-show -p
    [
      {
        "name": "wrapt",
        "version": "1.11.2",
        "summary": "Module for decorators, wrappers and monkey patching.",
        "home_page": "https://github.com/GrahamDumpleton/wrapt",
        "author": "Graham Dumpleton",
        "author_email": "Graham.Dumpleton@gmail.com",
        "license": "BSD",
        "location": "/usr/local/lib/python3.7/site-packages",
        "requires": null,
        "required_by": "astroid"
      },
      {
        "name": "wheel",
        "version": "0.33.4",
        "summary": "A built-package format for Python.",
        "home_page": "https://github.com/pypa/wheel",
        "author": "Daniel Holth",
        "author_email": "dholth@fastmail.fm",
        "license": "MIT",
        "location": "/usr/local/lib/python3.7/site-packages",
        "requires": null,
        "required_by": null
      }
    ]
"""
from typing import List, Dict, Optional
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`pip show` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['pip show', 'pip3 show']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    # no further processing
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []
    package: Dict = {}
    last_key: str = ''
    last_key_data: List = []

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        for row in cleandata:
            if row.startswith('---'):
                if last_key_data:
                    package[last_key] = package[last_key] + '\n' + '\n'.join(last_key_data)

                raw_output.append(package)
                package = {}
                last_key = ''
                last_key_data = []
                continue

            if not row.startswith(' '):
                item_key = row.split(': ', maxsplit=1)[0].lower().replace('-', '_')
                item_value: Optional[str] = row.split(': ', maxsplit=1)[1]

                if item_value == '':
                    item_value = None

                if last_key_data and last_key != item_key:
                    if not isinstance(package[last_key], str):
                        package[last_key] = ''
                    package[last_key] = package[last_key] + '\n' + '\n'.join(last_key_data)
                    last_key_data = []

                package[item_key] = item_value
                last_key = item_key
                continue

            if row.startswith(' '):
                last_key_data.append(row.strip())
                continue

        if package:
            if last_key_data:
                package[last_key] = package[last_key] + '\n' + '\n'.join(last_key_data)

            raw_output.append(package)

    return raw_output if raw else _process(raw_output)
