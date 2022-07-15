"""jc - JSON Convert `m3u` and `m3u8` file parser

Only standard extended info fields are supported.

Usage (cli):

    $ cat playlist.m3u | jc --m3u

Usage (module):

    import jc
    result = jc.parse('m3u', m3u_file_output)

Schema:

    [
      {
        "runtime":              integer,
        "display":              string,
        "path":                 string
      }
    ]

Examples:

    $ cat playlist.m3u | jc --m3u -p
    [
      {
        "runtime": 105,
        "display": "Example artist - Example title",
        "path": "C:\\Files\\My Music\\Example.mp3"
      },
      {
        "runtime": 321,
        "display": "Example Artist2 - Example title2",
        "path": "C:\\Files\\My Music\\Favorites\\Example2.ogg"
      }
    ]

    $ cat playlist.m3u | jc --m3u -p -r
    [
      {
        "runtime": "105",
        "display": "Example artist - Example title",
        "path": "C:\\Files\\My Music\\Example.mp3"
      },
      {
        "runtime": "321",
        "display": "Example Artist2 - Example title2",
        "path": "C:\\Files\\My Music\\Favorites\\Example2.ogg"
      }
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'M3U and M3U8 file parser'
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
    int_list = ['runtime']
    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

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
    output_line = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            # ignore any lines with only whitespace
            if not jc.utils.has_data(line):
                continue

            # standard extended info fields
            if line.lstrip().startswith('#EXTINF:'):
                output_line = {
                    'runtime': line.split(':')[1].split(',')[0].strip(),
                    'display': line.split(':')[1].split(',')[1].strip()
                }
                continue

            # ignore all other extension info (obsolete)
            if line.lstrip().startswith('#'):
                continue

            # any lines left over are paths
            output_line.update(
                {'path': line.strip()}
            )
            raw_output.append(output_line)
            output_line = {}

    return raw_output if raw else _process(raw_output)
