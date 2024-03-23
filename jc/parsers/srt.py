r"""jc - JSON Convert `SRT` file parser

Usage (cli):

    $ cat foo.srt | jc --srt

Usage (module):

    import jc
    result = jc.parse('srt', srt_file_output)

Schema:

    [
      {
        "index":              int,
        "start": {
          "hours":            int,
          "minutes":          int,
          "seconds":          int,
          "milliseconds":     int,
          "timestamp":        string
        },
        "end": {
          "hours":            int,
          "minutes":          int,
          "seconds":          int,
          "milliseconds":     int,
          "timestamp":        string
        },
        "content":            string
      }
    ]

Examples:

    $ cat attack_of_the_clones.srt
    1
    00:02:16,612 --> 00:02:19,376
    Senator, we're making
    our final approach into Coruscant.

    2
    00:02:19,482 --> 00:02:21,609
    Very good, Lieutenant.
    ...

    $ cat attack_of_the_clones.srt | jc --srt
    [
        {
            "index": 1,
            "start": {
                "hours": 0,
                "minutes": 2,
                "seconds": 16,
                "milliseconds": 612,
                "timestamp": "00:02:16,612"
            },
            "end": {
                "hours": 0,
                "minutes": 2,
                "seconds": 19,
                "milliseconds": 376,
                "timestamp": "00:02:19,376"
            },
            "content": "Senator, we're making\nour final approach into Coruscant."
        },
        {
            "index": 2,
            "start": {
                "hours": 0,
                "minutes": 2,
                "seconds": 19,
                "milliseconds": 482,
                "timestamp": "00:02:19,482"
            },
            "end": {
                "hours": 0,
                "minutes": 2,
                "seconds": 21,
                "milliseconds": 609,
                "timestamp": "00:02:21,609"
            },
            "content": "Very good, Lieutenant."
        },
        ...
    ]
"""
import jc.utils
import re
from typing import List, Dict
from jc.jc_types import JSONDictType


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'SRT file parser'
    author = 'Mark Rotner'
    author_email = 'rotner.mr@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version

# Regex from https://github.com/cdown/srt/blob/434d0c1c9d5c26d5c3fb1ce979fc05b478e9253c/srt.py#LL16C1.

# The MIT License

# Copyright (c) 2014-present Christopher Down

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# The format: (int)index\n(timestamp)start --> (timestamp)end\n(str)content\n.
# Example:
# 1
# 00:02:16,612 --> 00:02:19,376
# Senator, we're making our final approach into Coruscant.

# Start & End timestamp format: hours:minutes:seconds,millisecond.
# "." is not technically valid as a delimiter, but many editors create SRT
# files with this delimiter for whatever reason. Many editors and players
# accept it, so we do too.
RGX_TIMESTAMP_MAGNITUDE_DELIM = r"[,.:，．。：]"
RGX_POSITIVE_INT = r"[0-9]+"
RGX_POSITIVE_INT_OPTIONAL = r"[0-9]*"
RGX_TIMESTAMP = '{field}{separator}{field}{separator}{field}{separator}?{optional_field}'.format(
    separator=RGX_TIMESTAMP_MAGNITUDE_DELIM,
    field=RGX_POSITIVE_INT,
    optional_field=RGX_POSITIVE_INT_OPTIONAL
)
RGX_INDEX = r"-?[0-9]+\.?[0-9]*"  # int\float\negative.
RGX_CONTENT = r".*?"  # Anything(except newline) but lazy.
RGX_NEWLINE = r"\r?\n"  # Newline(CRLF\LF).
SRT_REGEX = re.compile(
    r"\s*(?:({index})\s*{newline})?({ts}) *-[ -] *> *({ts}) ?(?:{newline}|\Z)({content})"
    # Many sub editors don't add a blank line to the end, and many editors and
    # players accept that. We allow it to be missing in input.
    #
    # We also allow subs that are missing a double blank newline. This often
    # happens on subs which were first created as a mixed language subtitle,
    # for example chs/eng, and then were stripped using naive methods (such as
    # ed/sed) that don't understand newline preservation rules in SRT files.
    #
    # This means that when you are, say, only keeping chs, and the line only
    # contains english, you end up with not only no content, but also all of
    # the content lines are stripped instead of retaining a newline.
    r"(?:{newline}|\Z)(?:{newline}|\Z|(?=(?:{index}\s*{newline}{ts})))"
    # Some SRT blocks, while this is technically invalid, have blank lines
    # inside the subtitle content. We look ahead a little to check that the
    # next lines look like an index and a timestamp as a best-effort
    # solution to work around these.
    r"(?=(?:(?:{index}\s*{newline})?{ts}|\Z))".format(
        index=RGX_INDEX,
        ts=RGX_TIMESTAMP,
        content=RGX_CONTENT,
        newline=RGX_NEWLINE,
    ),
    re.DOTALL,
)
TIMESTAMP_REGEX = re.compile(
    '^({field}){separator}({field}){separator}({field}){separator}?({optional_field})$'.format(
        separator=RGX_TIMESTAMP_MAGNITUDE_DELIM,
        field=RGX_POSITIVE_INT,
        optional_field=RGX_POSITIVE_INT_OPTIONAL
    )
)


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:  (Dictionary) raw structured data to process

    Returns:

        List of Dictionaries representing an SRT document.
    """

    int_list = {'index'}
    timestamp_list = {"start", "end"}
    timestamp_int_list = {"hours", "minutes", "seconds", "milliseconds"}

    for entry in proc_data:
        # Converting {"index"} to int.
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

            # Converting {"hours", "minutes", "seconds", "milliseconds"} to int.
            if key in timestamp_list:
                timestamp = entry[key]
                for timestamp_key in timestamp:
                    if timestamp_key in timestamp_int_list:
                        timestamp[timestamp_key] = jc.utils.convert_to_int(
                            timestamp[timestamp_key])

    return proc_data


def parse_timestamp(timestamp: str) -> Dict:
    """
    timestamp: "hours:minutes:seconds,milliseconds" --->
    {
        "hours": "hours",
        "minutes": "minutes",
        "seconds": "seconds",
        "milliseconds": "milliseconds",
        "timestamp": "hours:minutes:seconds,milliseconds"
    }
    """
    ts_match = TIMESTAMP_REGEX.match(timestamp)
    if ts_match:
        hours, minutes, seconds, milliseconds = ts_match.groups()
        return {
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "milliseconds": milliseconds,
            "timestamp": timestamp
        }
    return {}


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

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[Dict] = []
    if not jc.utils.has_data(data):
        return raw_output

    for subtitle in SRT_REGEX.finditer(data):
        index, start, end, content = subtitle.groups()
        raw_output.append(
            {
                "index": index,
                "start": parse_timestamp(start),
                "end": parse_timestamp(end),
                "content": content.replace("\r\n", "\n")
            }
        )

    return raw_output if raw else _process(raw_output)
