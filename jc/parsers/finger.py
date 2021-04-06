"""jc - JSON CLI output utility `finger` command output parser

<<Short finger description and caveats>>

Usage (cli):

    $ finger | jc --finger

    or

    $ jc finger

Usage (module):

    import jc.parsers.finger
    result = jc.parsers.finger.parse(finger_command_output)

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ finger | jc --finger -p
    [
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "*tty1",
        "idle": "13d",
        "login_time": "Mar 22 21:14"
      },
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "pts/0",
        "idle": null,
        "login_time": "Apr  5 15:33",
        "details": "(192.168.1.22)"
      }
    ]
"""
import re
import jc.utils
import jc.parsers.universal


class info():
    version = '1.0'
    description = '`finger` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['finger']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data with the following schema:

        [
          {
            "login": "kbrazil",
            "name": "Kelly Brazil",
            "tty": "*tty1",
            "idle": "13d",
            "login_time": "Mar 22 21:14"
          },
          {
            "login": "kbrazil",
            "name": "Kelly Brazil",
            "tty": "pts/0",
            "idle": null,
            "login_time": "Apr  5 15:33",
            "details": "(192.168.1.221)"
          }
        ]
    """

    # rebuild output for added semantic information
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
        # Finger output is an abomination that is nearly unparsable. But there is a way:
        # First find the location of the last character of 'Idle' in the table and cut
        # all lines at that spot. Data before that spot can use the unviversal.sparse_table_parse function.
        # All data after that spot can be run through regex to find the login datetime and possibly
        # other fields.

        data_lines = list(filter(None, data.splitlines()))
        sep_col = data_lines[0].find('Idle') + 4
        first_half = []
        second_half = []

        for line in data_lines:
            first_half.append(line[:sep_col])
            second_half.append(line[sep_col:])

        first_half[0] = first_half[0].lower()

        # parse the first half
        raw_output =  jc.parsers.universal.sparse_table_parse(first_half)

        # use regex to get login datetime and 'other' data
        pattern = re.compile(r'([A-Z][a-z]{2}\s+\d{1,2}\s+\d\d:\d\d)(\s+\S+)?')

        # remove header row from list
        second_half.pop(0)

        for index, line in enumerate(second_half):
            dt = re.search(pattern, line)
            if dt.group(1):
                raw_output[index]['login_time'] = dt.group(1).strip()
            if dt.group(2):
                raw_output[index]['details'] = dt.group(2).strip()

    if raw:
        return raw_output
    else:
        return process(raw_output)
