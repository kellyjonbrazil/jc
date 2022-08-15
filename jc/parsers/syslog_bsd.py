"""jc - JSON Convert Syslog RFC 3164 string parser

<<Short syslog-3164 description and caveats>>

Usage (cli):

    $ syslogstring | jc --syslog-bsd

or

    $ jc syslog-3164

Usage (module):

    import jc
    result = jc.parse('syslog_bsd', syslog_command_output)

Schema:

    [
      {
        "syslog-3164":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ syslog-3164 | jc --syslog-3164 -p
    []

    $ syslog-3164 | jc --syslog-3164 -p -r
    []
"""
import re
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Syslog RFC 3164 string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']

__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

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

    # inspired by https://gist.github.com/miticojo/b16bb13e78572c2d2fac82d9516d5c32
    syslog = re.compile(r'''
        (?P<priority><\d*>)?
        (?P<date>[A-Z][a-z][a-z]\s{1,2}\d{1,2}\s\d{2}?:\d{2}:\d{2})\s
        (?P<host>[\w][\w\d\.@-]*)\s
        (?P<tag>[\w\d\[\]\.@-]+):?\s
        (?P<message>.*)
        ''', re.VERBOSE
    )

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            syslog_match = syslog.match(line)
            if syslog_match:
                priority = None
                if syslog_match.group('priority'):
                    priority = syslog_match.group('priority')[1:-1]

                syslog_dict = {
                    'priority': priority,
                    'date': syslog_match.group('date'),
                    'hostname': syslog_match.group('host'),
                    'tag': syslog_match.group('tag'),
                    'message': syslog_match.group('message')
                }

            if syslog_dict:
                raw_output.append(syslog_dict)

    return raw_output if raw else _process(raw_output)
