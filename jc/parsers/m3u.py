r"""jc - JSON Convert M3U and M3U8 file parser

This parser will make a best-effort to parse extended field information. If
the extended fields cannot be successfully parsed, then an `unparsed_info`
field will be added to the object. If not using `--quiet`, then a warning
message also will be printed to `STDERR`.

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
        "path":                 string,
        <extended fields>:      string,  # [0]
        "unparsed_info":        string,  # [1]
      }
    ]

    [0] Field names are pulled directly from the #EXTINF: line
    [1] Only added if the extended information cannot be parsed

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
import shlex
from typing import List, Dict, Tuple
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'M3U and M3U8 file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'runtime'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def _split_extinf(info_str: str) -> Tuple[str, str]:
    """
    Split the text after '#EXTINF:' at the first comma that is not inside
    a double-quoted attribute value. Returns the duration/attributes part
    and the title part. The title is empty if there is no such comma.
    """
    in_quote = False
    index = 0

    while index < len(info_str):
        character = info_str[index]

        if character == '\\':
            # match shlex escapes: any character outside quotes, only
            # a double quote or backslash inside quotes
            if not in_quote or info_str[index + 1:index + 2] in ('"', '\\'):
                index += 2
                continue

        elif character == '"':
            in_quote = not in_quote

        elif character == ',' and not in_quote:
            return info_str[:index], info_str[index + 1:].strip()

        index += 1

    return info_str, ''


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
        for line in filter(None, jc.utils.splitlines(data, split_cr=True)):
            # ignore any lines with only whitespace
            if not jc.utils.has_data(line):
                continue

            # extended info fields
            if line.lstrip().startswith('#EXTINF:'):
                splitline = line.strip().split(':', maxsplit=1)

                # each #EXTINF: line starts a new entry. Drop the fields of
                # a previous #EXTINF: line that had no path line
                output_line = {}

                # best-effort to parse additional extended fields
                # if a parsing error occurs, a warning message will be
                # printed to STDERR and `unparsed_info` added
                try:
                    attributes, title = _split_extinf(splitline[1])
                    extline = shlex.shlex(attributes, posix=True)
                    extline.whitespace_split = True
                    extline.whitespace = ', '  # add comma to whitespace detection
                    extline.quotes = '"'  # remove single quotes
                    extline_list = list(extline)
                    runtime = extline_list.pop(0) if extline_list else ''
                    display_list = []

                    for item in extline_list:
                        if '=' in item:
                            k, v = item.split('=', maxsplit=1)
                            output_line.update({k: v})

                        else:
                            display_list.append(item)

                    # the title is everything after the first comma, as-is
                    if title:
                        display_list.append(title)

                    display = ' '.join(display_list)
                    output_line.update({
                        'runtime': runtime,
                        'display': display
                    })

                except Exception:
                    if not quiet:
                        jc.utils.warning_message([
                            'Not able to parse non-standard extensions in the following line:',
                            line
                        ])
                    output_line = {'unparsed_info': line}

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
