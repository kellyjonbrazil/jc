r"""jc - JSON Convert Common Log Format file parser

This parser will handle the Common Log Format standard as specified at
https://www.w3.org/Daemon/User/Config/Logging.html#common-logfile-format.

Combined Log Format is also supported. (Referer and User Agent fields added)

Extra fields may be present and will be enclosed in the `extra` field as
a single string.

If a log line cannot be parsed, an object with an `unparsable` field will
be present with a value of the original line.

The `epoch` calculated timestamp field is naive. (i.e. based on the
local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is
only available if the timezone field is UTC.

Usage (cli):

    $ cat file.log | jc --clf

Usage (module):

    import jc
    result = jc.parse('clf', common_log_file_output)

Schema:

Empty strings and `-` values are converted to `null`/`None`.

    [
      {
        "host":                         string,
        "ident":                        string,
        "authuser":                     string,
        "date":                         string,
        "day":                          integer,
        "month":                        string,
        "year":                         integer,
        "hour":                         integer,
        "minute":                       integer,
        "second":                       integer,
        "tz":                           string,
        "request":                      string,
        "request_method":               string,
        "request_url":                  string,
        "request_version":              string,
        "status":                       integer,
        "bytes":                        integer,
        "referer":                      string,
        "user_agent":                   string,
        "extra":                        string,
        "epoch":                        integer,  # [0]
        "epoch_utc":                    integer,  # [1]
        "unparsable":                   string    # [2]
      }
    ]

    [0] naive timestamp
    [1] timezone-aware timestamp. Only available if timezone field is UTC
    [2] exists if the line was not able to be parsed

Examples:

    $ cat file.log | jc --clf -p
    [
      {
        "host": "127.0.0.1",
        "ident": "user-identifier",
        "authuser": "frank",
        "date": "10/Oct/2000:13:55:36 -0700",
        "day": 10,
        "month": "Oct",
        "year": 2000,
        "hour": 13,
        "minute": 55,
        "second": 36,
        "tz": "-0700",
        "request": "GET /apache_pb.gif HTTPS/1.0",
        "status": 200,
        "bytes": 2326,
        "referer": null,
        "user_agent": null,
        "extra": null,
        "request_method": "GET",
        "request_url": "/apache_pb.gif",
        "request_version": "HTTPS/1.0",
        "epoch": 971211336,
        "epoch_utc": null
      },
      {
        "host": "1.1.1.2",
        "ident": null,
        "authuser": null,
        "date": "11/Nov/2016:03:04:55 +0100",
        "day": 11,
        "month": "Nov",
        "year": 2016,
        "hour": 3,
        "minute": 4,
        "second": 55,
        "tz": "+0100",
        "request": "GET /",
        "status": 200,
        "bytes": 83,
        "referer": null,
        "user_agent": null,
        "extra": "- 9221 1.1.1.1",
        "request_method": "GET",
        "request_url": "/",
        "request_version": null,
        "epoch": 1478862295,
        "epoch_utc": null
      },
      ...
    ]

    $ cat file.log | jc --clf -p -r
    [
      {
        "host": "127.0.0.1",
        "ident": "user-identifier",
        "authuser": "frank",
        "date": "10/Oct/2000:13:55:36 -0700",
        "day": "10",
        "month": "Oct",
        "year": "2000",
        "hour": "13",
        "minute": "55",
        "second": "36",
        "tz": "-0700",
        "request": "GET /apache_pb.gif HTTPS/1.0",
        "status": "200",
        "bytes": "2326",
        "referer": null,
        "user_agent": null,
        "extra": "",
        "request_method": "GET",
        "request_url": "/apache_pb.gif",
        "request_version": "HTTPS/1.0"
      },
      {
        "host": "1.1.1.2",
        "ident": "-",
        "authuser": "-",
        "date": "11/Nov/2016:03:04:55 +0100",
        "day": "11",
        "month": "Nov",
        "year": "2016",
        "hour": "03",
        "minute": "04",
        "second": "55",
        "tz": "+0100",
        "request": "GET /",
        "status": "200",
        "bytes": "83",
        "referer": "-",
        "user_agent": "-",
        "extra": "- 9221 1.1.1.1",
        "request_method": "GET",
        "request_url": "/",
        "request_version": null
      },
      ...
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Common and Combined Log Format file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'day', 'year', 'hour', 'minute', 'second', 'status', 'bytes'}

    for log in proc_data:
        for key, val in log.items():

            # integer conversions
            if key in int_list:
                log[key] = jc.utils.convert_to_int(val)

            # convert `-` and blank values to None
            if val == '-' or val == '':
                log[key] = None

        # add unix timestamps
        if 'date' in log:
            ts = jc.utils.timestamp(log['date'], format_hint=(1800,))
            log['epoch'] = ts.naive
            log['epoch_utc'] = ts.utc

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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

    raw_output: List[Dict] = []
    output_line: Dict = {}

    clf_pattern = re.compile(r'''
        ^(?P<host>-|\S+)\s
        (?P<ident>-|\S+)\s
        (?P<authuser>-|\S+)\s
        \[
        (?P<date>
            (?P<day>\d+)/
            (?P<month>\S\S\S)/
            (?P<year>\d\d\d\d):
            (?P<hour>\d\d):
            (?P<minute>\d\d):
            (?P<second>\d\d)\s
            (?P<tz>\S+)
        )
        \]\s
        \"(?P<request>.*?)\"\s
        (?P<status>-|\d\d\d)\s
        (?P<bytes>-|\d+)\s?
        (?:\"(?P<referer>.*?)\"\s?)?
        (?:\"(?P<user_agent>.*?)\"\s?)?
        (?P<extra>.*)
        ''', re.VERBOSE
    )

    request_pattern = re.compile(r'''
        (?P<request_method>\S+)\s
        (?P<request_url>.*?(?=\sHTTPS?/|$))\s?  # positive lookahead for HTTP(S)/ or end of string
        (?P<request_version>HTTPS?/[\d\.]+)?
    ''', re.VERBOSE
    )

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            output_line = {}
            clf_match = re.match(clf_pattern, line)

            if clf_match:
                output_line = clf_match.groupdict()

                if output_line.get('request', None):
                    request_string = output_line['request']
                    request_match = re.match(request_pattern, request_string)
                    if request_match:
                         output_line.update(request_match.groupdict())

                raw_output.append(output_line)

            else:
                raw_output.append(
                    {"unparsable": line}
                )

    return raw_output if raw else _process(raw_output)
