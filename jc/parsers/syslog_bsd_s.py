"""jc - JSON Convert Syslog RFC 3164 string streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

This parser accepts a single syslog line string or multiple syslog lines
separated by newlines. A warning message to `STDERR` will be printed if an
unparsable line is found unless `--quiet` or `quiet=True` is used.

Usage (cli):

    $ echo '<34>Oct 11 22:14:15 mymachine su: su ro...' | jc --syslog-bsd-s

Usage (module):

    import jc

    result = jc.parse('syslog_bsd_s', syslog_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "priority":                   integer/null,
      "date":                       string,
      "hostname":                   string,
      "tag":                        string/null,
      "content":                    string,
      "unparsable":                 string,  # [0]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] this field exists if the syslog line is not parsable. The value
        is the original syslog line.

Examples:

    $ cat syslog.txt | jc --syslog-bsd-s -p
    {"priority":34,"date":"Oct 11 22:14:15","hostname":"mymachine","t...}
    {"priority":34,"date":"Oct 11 22:14:16","hostname":"mymachine","t...}
    ...

    $ cat syslog.txt | jc --syslog-bsd-s -p -r
    {"priority":"34","date":"Oct 11 22:14:15","hostname":"mymachine","...}
    {"priority":"34","date":"Oct 11 22:14:16","hostname":"mymachine","...}
    ...
"""
from typing import Dict, Iterable, Union
import re
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Syslog RFC 3164 string streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']
    streaming = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = {'priority'}

    for key in proc_data:
            if key in int_list:
                proc_data[key] = jc.utils.convert_to_int(proc_data[key])

    return proc_data


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Union[Iterable[Dict], tuple]:
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True


    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

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

    for line in data:
        try:
            streaming_line_input_type_check(line)
            output_line: Dict = {}

            #skip blank lines
            if not line.strip():
                continue

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

                output_line = {
                    'priority': priority,
                    'date': syslog_match.group('date'),
                    'hostname': hostname,
                    # 'raw_msg': syslog_match.group('msg'),
                    'tag': tag,
                    'content': content.lstrip(' :').rstrip()
                }

            else:
                output_line = {
                    'unparsable': line.rstrip()
                }

                if not quiet:
                    jc.utils.warning_message(
                        [f'Unparsable line found: {line.rstrip()}']
                    )

            if output_line:
                yield output_line if raw else _process(output_line)

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
