"""jc - JSON Convert Syslog RFC 5424 string parser

<<Short syslog-5424 description and caveats>>

Usage (cli):

    $ syslog-5424 | jc --syslog-5424

    or

    $ jc syslog-5424

Usage (module):

    import jc
    result = jc.parse('syslog_5424', syslog_command_output)

Schema:

    [
      {
        "syslog-5424":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ syslog-5424 | jc --syslog-5424 -p
    []

    $ syslog-5424 | jc --syslog-5424 -p -r
    []
"""
import re
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Syslog RFC 5424 string parser'
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
    syslog_dict = {}

    # inspired by https://regex101.com/library/Wgbxn2
    syslog = re.compile(r'''
        (?P<priority><(\d|\d{2}|1[1-8]\d|19[01])>)?
        (?P<version>\d{1,2})?\s*
        (?P<timestamp>-|(?P<fullyear>[12]\d{3})-
            (?P<month>0\d|[1][012])-
            (?P<mday>[012]\d|3[01])T
            (?P<hour>[01]\d|2[0-4]):
            (?P<minute>[0-5]\d):
            (?P<second>[0-5]\d|60)(?#60seconds can be used for leap year!)(?:\.
            (?P<secfrac>\d{1,6}))?
            (?P<numoffset>Z|[+-]\d{2}:\d{2})(?#=timezone))\s
        (?P<hostname>[\S]{1,255})\s
        (?P<appname>[\S]{1,48})\s
        (?P<procid>[\S]{1,128})\s
        (?P<msgid>[\S]{1,32})\s
        (?P<structureddata>-|(?:\[.+?(?<!\\)\])+)
        (?:\s(?P<msg>.+))?
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
                    'version': syslog_match.group('version'),
                    'timestamp': syslog_match.group('timestamp'),
                    'hostname': syslog_match.group('hostname'),
                    'appname': syslog_match.group('appname'),
                    'proc_id': syslog_match.group('procid'),
                    'msg_id': syslog_match.group('msgid'),
                    'struct': syslog_match.group('structureddata'),
                    'message': syslog_match.group('msg')
                }

            if syslog_dict:
                raw_output.append(syslog_dict)

    return raw_output if raw else _process(raw_output)
