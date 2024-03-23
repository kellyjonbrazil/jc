r"""jc - JSON Convert Version string output parser

Best-effort attempt to parse various styles of version numbers. This parser
is based off of the version parser included in the CPython distutils
library.

If the version string conforms to some de facto-standard versioning rules
followed by many developers a `strict` key will be present in the output
with a value of `true` along with the named parsed components.

All other version strings will have a `strict` value of `false` and a
`components` key will contain a list of detected parts of the version
string.

See Also: `semver` parser.

Usage (cli):

    $ echo 1.2a1 | jc --ver

Usage (module):

    import jc
    result = jc.parse('ver', version_string_output)

Schema:

    {
      "major":                  integer,
      "minor":                  integer,
      "patch":                  integer,
      "prerelease":             string,
      "prerelease_num":         integer,
      "components": [
                                integer/string
      ],
      "strict":                 boolean
    }

Examples:

    $ echo 1.2a1 | jc --ver -p
    {
      "major": 1,
      "minor": 2,
      "patch": 0,
      "prerelease": "a",
      "prerelease_num": 1,
      "strict": true
    }

    $ echo 1.2a1 | jc --ver -p -r
    {
      "major": "1",
      "minor": "2",
      "patch": "0",
      "prerelease": "a",
      "prerelease_num": "1",
      "strict": true
    }

    $ echo 1.2beta3 | jc --ver -p
    {
      "components": [
        1,
        2,
        "beta",
        3
      ],
      "strict": false
    }

    $ echo 1.2beta3 | jc --ver -p -r
    {
      "components": [
        "1",
        "2",
        "beta",
        "3"
      ],
      "strict": false
    }
"""
import re
from typing import Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = 'Version string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Based on distutils/version.py from CPython 3.9.5.'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['generic', 'string', 'slurpable']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'major', 'minor', 'patch', 'prerelease', 'prerelease_num'}

    for k, v in proc_data.items():
        if k in int_list:
            try:
                proc_data[k] = int(v)
            except Exception:
                pass

    if 'components' in proc_data:
        for i, obj in enumerate(proc_data['components']):
            try:
                proc_data['components'][i] = int(obj)
            except Exception:
                pass

    return proc_data


def _strict_parse(vstring):
    version_re = re.compile(r'^(\d+) \. (\d+) (\. (\d+))? ([ab](\d+))?$', re.VERBOSE)
    match = version_re.match(vstring)
    if not match:
        raise ValueError("invalid version number '%s'" % vstring)

    (major, minor, patch, prerelease, prerelease_num) = \
        match.group(1, 2, 4, 5, 6)

    if not patch:
        patch = '0'

    if prerelease:
        prerelease = prerelease[0]
    else:
        prerelease = None

    return {
        'major': major,
        'minor': minor,
        'patch': patch,
        'prerelease': prerelease,
        'prerelease_num': prerelease_num
    }


def _loose_parse(vstring):
    component_re = re.compile(r'(\d+ | [a-z]+ | \.)', re.VERBOSE)
    components = [x for x in component_re.split(vstring) if x and x != '.']

    return components


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

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}
    strict = True

    if jc.utils.has_data(data):

        # based on distutils/version.py from CPython 3.9.5
        # PSF License (see https://opensource.org/licenses/Python-2.0)

        data = data.strip()

        try:
            raw_output = _strict_parse(data)

        except ValueError:
            raw_output['components'] = _loose_parse(data)
            strict = False

        if raw_output:
            raw_output['strict'] = strict

    return raw_output if raw else _process(raw_output)
