r"""jc - JSON Convert Semantic Version string parser

This parser conforms to the specification at https://semver.org/

See Also: `ver` parser.

Usage (cli):

    $ echo 1.2.3-rc.1+44837 | jc --semver

Usage (module):

    import jc
    result = jc.parse('semver', semver_string)

Schema:

Strings that do not strictly conform to the specification will return an
empty object.

    {
      "major":                  integer,
      "minor":                  integer,
      "patch":                  integer,
      "prerelease":             string/null,
      "build":                  string/null
    }

Examples:

    $ echo 1.2.3-rc.1+44837 | jc --semver -p
    {
      "major": 1,
      "minor": 2,
      "patch": 3,
      "prerelease": "rc.1",
      "build": "44837"
    }

    $ echo 1.2.3-rc.1+44837 | jc --semver -p -r
    {
      "major": "1",
      "minor": "2",
      "patch": "3",
      "prerelease": "rc.1",
      "build": "44837"
    }
"""
import re
from typing import Set, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'Semantic Version string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'string', 'slurpable']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list: Set[str] = {'major', 'minor', 'patch'}

    for item in int_list:
        if item in proc_data:
            proc_data[item] = int(proc_data[item])

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

    raw_output: Dict = {}
    semver_pattern = re.compile(r'''
        ^(?P<major>0|[1-9]\d*)\.
        (?P<minor>0|[1-9]\d*)\.
        (?P<patch>0|[1-9]\d*)
        (?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?
        (?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$
    ''', re.VERBOSE)

    if jc.utils.has_data(data):
        semver_match = re.match(semver_pattern, data)
        if semver_match:
            raw_output = semver_match.groupdict()

    return raw_output if raw else _process(raw_output)
