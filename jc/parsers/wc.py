r"""jc - JSON Convert `wc` command output parser

Usage (cli):

    $ wc file.txt | jc --wc

or

    $ jc wc file.txt

Usage (module):

    import jc
    result = jc.parse('wc', wc_command_output)

Schema:

    [
      {
        "filename":     string,
        "lines":        integer,
        "words":        integer,
        "characters":   integer
      }
    ]

Examples:

    $ wc * | jc --wc -p
    [
      {
        "filename": "airport-I.json",
        "lines": 1,
        "words": 30,
        "characters": 307
      },
      {
        "filename": "airport-I.out",
        "lines": 15,
        "words": 33,
        "characters": 348
      },
      {
        "filename": "airport-s.json",
        "lines": 1,
        "words": 202,
        "characters": 2152
      },
      ...
    ]
"""
import re

import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`wc` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['wc']
    tags = ['command']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    int_list = {'lines', 'words', 'characters'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def parse(data, raw=False, quiet=False):
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

    raw_output = []

    if jc.utils.has_data(data):

        for line in filter(None, jc.utils.splitlines(data)):
            counts = re.split(r'[ \t]+', line.lstrip(' \t'), maxsplit=2)
            # Consume only the delimiter after the final count.
            characters, *filename = re.split(r'[ \t]', counts[2], maxsplit=1)
            item = {
                'filename': (filename[0] or None) if filename else None,
                'lines': counts[0],
                'words': counts[1],
                'characters': characters
            }
            raw_output.append(item)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
