r"""jc - JSON Convert Syslog RFC 3164 string parser

This parser accepts a single syslog line string or multiple syslog lines
separated by newlines. A warning message to `STDERR` will be printed if an
unparsable line is found unless `--quiet` or `quiet=True` is used.

Usage (cli):

    $ echo '<34>Oct 11 22:14:15 mymachine su: su root...' | jc --syslog-bsd

Usage (module):

    import jc
    result = jc.parse('syslog_bsd', syslog_command_output)

Schema:

    [
      {
        "priority":                   integer/null,
        "date":                       string,
        "hostname":                   string,
        "tag":                        string/null,
        "content":                    string,
        "unparsable":                 string,  # [0]
      }
    ]

    [0] this field exists if the syslog line is not parsable. The value
        is the original syslog line.

Examples:

    $ cat syslog.txt | jc --syslog-bsd -p
    [
      {
        "priority": 34,
        "date": "Oct 11 22:14:15",
        "hostname": "mymachine",
        "tag": "su",
        "content": "'su root' failed for lonvick on /dev/pts/8"
      }
    ]

    $ cat syslog.txt | jc --syslog-bsd -p -r
    [
      {
        "priority": "34",
        "date": "Oct 11 22:14:15",
        "hostname": "mymachine",
        "tag": "su",
        "content": "'su root' failed for lonvick on /dev/pts/8"
      }
    ]
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
    tags = ['standard', 'file', 'string']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'priority'}

    for item in proc_data:
        for key in item:
                if key in int_list:
                    item[key] = jc.utils.convert_to_int(item[key])

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

    # inspired by https://gist.github.com/miticojo/b16bb13e78572c2d2fac82d9516d5c32
    syslog = re.compile(r'''
        (?P<priority><\d{1,3}>)?
        (?P<header>
            (?P<date>[A-Z][a-z][a-z]\s{1,2}\d{1,2}\s\d{2}?:\d{2}:\d{2})?\s
            (?P<host>[\w][\w\d\.:@-]*)?\s
        )
        (?P<msg>
            (?P<tag>\w+)?
            (?P<content>.*)
        )
        ''', re.VERBOSE
    )

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            syslog_match = syslog.match(line)
            if syslog_match:
                priority = None
                if syslog_match.group('priority'):
                    priority = syslog_match.group('priority')[1:-1]

                # check for missing tag
                hostname = syslog_match.group('host')
                tag = syslog_match.group('tag')
                content = syslog_match.group('content')
                if hostname:
                    if hostname.endswith(':'):
                        content = tag + content
                        tag = None
                        hostname = hostname[:-1]

                syslog_dict = {
                    'priority': priority,
                    'date': syslog_match.group('date'),
                    'hostname': hostname,
                    # 'raw_msg': syslog_match.group('msg'),
                    'tag': tag,
                    'content': content.lstrip(' :').rstrip()
                }

            else:
                syslog_dict = {
                    'unparsable': line
                }

                if not quiet:
                    jc.utils.warning_message(
                        [f'Unparsable line found: {line}']
                    )

            if syslog_dict:
                raw_output.append(syslog_dict)

    return raw_output if raw else _process(raw_output)
