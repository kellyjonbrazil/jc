r"""jc - JSON Convert `/proc/version` file parser

> Note: This parser will parse `/proc/version` files that follow the
> common format used by most popular linux distributions.

Usage (cli):

    $ cat /proc/version | jc --proc

or

    $ jc /proc/version

or

    $ cat /proc/version | jc --proc-version

Usage (module):

    import jc
    result = jc.parse('proc', proc_version_file)

or

    import jc
    result = jc.parse('proc_version', proc_version_file)

Schema:

    {
      "version":                  string,
      "email":                    string,
      "gcc":                      string,
      "build":                    string,
      "flags":                    string/null,
      "date":                     string
    }

Examples:

    $ cat /proc/version | jc --proc -p
    {
      "version": "5.8.0-63-generic",
      "email": "buildd@lcy01-amd64-028",
      "gcc": "gcc (Ubuntu 10.3.0-1ubuntu1~20.10) 10.3.0, GNU ld (GNU Binutils for Ubuntu) 2.35.1",
      "build": "#71-Ubuntu",
      "flags": "SMP",
      "date": "Tue Jul 13 15:59:12 UTC 2021"
    }
"""
import re
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/version` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


# inspired by https://gist.github.com/ty2/ad61340e7a4067def2e3c709496bca9d
version_pattern = re.compile(r'''
    Linux\ version\ (?P<version>\S+)\s
    \((?P<email>\S+?)\)\s
    \((?P<gcc>gcc.+)\)\s
    (?P<build>\#\d+(\S+)?)\s
    (?P<flags>.*)?
    (?P<date>(Sun|Mon|Tue|Wed|Thu|Fri|Sat).+)
    ''', re.VERBOSE
)


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
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

    if jc.utils.has_data(data):
        version_match = version_pattern.match(data)

        if version_match:

            ver_dict = version_match.groupdict()
            raw_output = {x: y.strip() or None for x, y in ver_dict.items()}

    return raw_output if raw else _process(raw_output)
