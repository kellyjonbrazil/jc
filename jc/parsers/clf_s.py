"""jc - JSON Convert Common Log Format file streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

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

    $ cat file.log | jc --clf-s

Usage (module):

    import jc

    result = jc.parse('clf_s', common_log_file_output.splitlines())
    for item in result:
        # do something

Schema:

    Empty strings and `-` values are converted to `null`/`None`.

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

    [0] naive timestamp
    [1] timezone-aware timestamp. Only available if timezone field is UTC
    [2] exists if the line was not able to be parsed

Examples:

    $ cat file.log | jc --clf-s
    {"host":"127.0.0.1","ident":"user-identifier","authuser":"frank","...}
    {"host":"1.1.1.2","ident":null,"authuser":null,"date":"11/Nov/2016...}
    ...

    $ cat file.log | jc --clf-s -r
    {"host":"127.0.0.1","ident":"user-identifier","authuser":"frank","...}
    {"host":"1.1.1.2","ident":"-","authuser":"-","date":"11/Nov/2016:0...}
    ...
"""
import re
from typing import Dict, Iterable
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.jc_types import JSONDictType, StreamingOutputType
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Common and Combined Log Format file streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']
    streaming = True


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = {'day', 'year', 'hour', 'minute', 'second', 'status', 'bytes'}

    for key, val in proc_data.items():

        # integer conversions
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(val)

        # convert `-` and blank values to None
        if val == '-' or val == '':
            proc_data[key] = None

    # add unix timestamps
    if 'date' in proc_data:
        ts = jc.utils.timestamp(proc_data['date'], format_hint=(1800,))
        proc_data['epoch'] = ts.naive
        proc_data['epoch_utc'] = ts.utc

    return proc_data


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> StreamingOutputType:
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

    for line in data:
        try:
            streaming_line_input_type_check(line)
            output_line: Dict = {}

            if not line.strip():
                continue

            clf_match = re.match(clf_pattern, line)

            if clf_match:
                output_line = clf_match.groupdict()

                if output_line.get('request', None):
                    request_string = output_line['request']
                    request_match = re.match(request_pattern, request_string)
                    if request_match:
                         output_line.update(request_match.groupdict())

            else:
                output_line = {"unparsable": line.strip()}

            if output_line:
                yield output_line if raw else _process(output_line)
            else:
                raise ParseError('Not Common Log Format data')

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
