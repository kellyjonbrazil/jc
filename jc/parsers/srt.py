"""jc - JSON Convert `SRT` file parser

Usage (cli):

    $ cat foo.srt | jc --srt

Usage (module):

    import jc
    result = jc.parse('srt', srt_file_output)

Schema:
    [
        {
            "index": int,
            "start": {
                "hours": int,
                "minutes": int,
                "seconds": int,
                "milliseconds": int,
                "timestamp": string
            },
            "end": {
                "hours": int,
                "minutes": int,
                "seconds": int,
                "milliseconds": int,
                "timestamp": string
            },
            "text": string
        },
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
            "text": "Senator, we're making\nour final approach into Coruscant.\n"
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
            "text": "Very good, Lieutenant.\n"
        },
        ...
    ]
"""

import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'SRT file parser'
    author = 'Mark Rotner'
    author_email = 'rotner.mr@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


def _process(proc_data):
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
                        timestamp[timestamp_key] = jc.utils.convert_to_int(timestamp[timestamp_key])

    return proc_data


def parse_timestamp(timestamp: str):
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

    hours, minutes, seconds_milliseconds = timestamp.split(':')
    seconds, milliseconds = seconds_milliseconds.split(',')
    return {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "milliseconds": milliseconds,
        "timestamp": timestamp
    }


def parse(data: str, raw: bool = False, quiet: bool = False):
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

    raw_output = []
    if not jc.utils.has_data(data):
        return raw_output

    subtitle = {}
    lines = list(filter(None, data.splitlines()))
    for line in lines:
        line = line.strip()
        if line.isdigit():  # Reached a new subtitle.
            if subtitle:
                raw_output.append(subtitle)
                subtitle = {}
            subtitle['index'] = line
            continue

        if '-->' in line:  # Start and end time of the subtitle separated by –> characters.
            start, end = line.split('-->')
            subtitle['start'] = parse_timestamp(start.strip())
            subtitle['end'] = parse_timestamp(end.strip())
            continue

        subtitle.setdefault('text', '')
        subtitle['text'] += line + '\n'

    if subtitle:
        raw_output.append(subtitle)

    return raw_output if raw else _process(raw_output)
