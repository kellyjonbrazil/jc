"""jc - JSON CLI output utility `wc` command output parser

Usage (cli):

    $ wc file.txt | jc --wc

    or

    $ jc wc file.txt

Usage (module):

    import jc.parsers.wc
    result = jc.parsers.wc.parse(wc_command_output)

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
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`wc` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['wc']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    for entry in proc_data:
        int_list = ['lines', 'words', 'characters']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            split_line = line.split(maxsplit=3)
            item = {
                'filename': split_line[3] if len(split_line) == 4 else None,
                'lines': split_line[0],
                'words': split_line[1],
                'characters': split_line[2]
            }
            raw_output.append(item)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
