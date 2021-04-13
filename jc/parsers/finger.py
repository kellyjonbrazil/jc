"""jc - JSON CLI output utility `finger` command output parser

Supports `-s` output option. Does not support the `-l` detail option.

Usage (cli):

    $ finger | jc --finger

    or

    $ jc finger

Usage (module):

    import jc.parsers.finger
    result = jc.parsers.finger.parse(finger_command_output)

Schema:

    [
      {
        "login":                string,
        "name":                 string,
        "tty":                  string,
        "idle":                 string,     # null if empty
        "login_time":           string,
        "details":              string,
        "tty_writeable":        boolean,
        "idle_minutes":         integer,
        "idle_hours":           integer,
        "idle_days":            integer,
        "total_idle_minutes":   integer
      }
    ]

Examples:

    $ finger | jc --finger -p
    [
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "tty1",
        "idle": "14d",
        "login_time": "Mar 22 21:14",
        "tty_writeable": false,
        "idle_minutes": 0,
        "idle_hours": 0,
        "idle_days": 14,
        "total_idle_minutes": 20160
      },
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "pts/0",
        "idle": null,
        "login_time": "Apr  5 15:33",
        "details": "(192.168.1.22)",
        "tty_writeable": true,
        "idle_minutes": 0,
        "idle_hours": 0,
        "idle_days": 0,
        "total_idle_minutes": 0
      },
      ...
    ]

    $ finger | jc --finger -p -r
    [
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "*tty1",
        "idle": "14d",
        "login_time": "Mar 22 21:14"
      },
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "pts/0",
        "idle": null,
        "login_time": "Apr  5 15:33",
        "details": "(192.168.1.22)"
      },
      ...
    ]
"""
import re
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`finger` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'freebsd']
    magic_commands = ['finger']


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
        if 'tty' in entry:
            entry['tty_writeable'] = True
            if '*' in entry['tty']:
                entry['tty'] = entry['tty'].replace('*', '')
                entry['tty_writeable'] = False

        if 'idle' in entry:
            entry['idle_minutes'] = 0
            entry['idle_hours'] = 0
            entry['idle_days'] = 0

            if entry['idle'] == '-':
                entry['idle'] = None

            if entry['idle'] and entry['idle'].isnumeric():
                entry['idle_minutes'] = int(entry['idle'])

            if entry['idle'] and ':' in entry['idle']:
                entry['idle_hours'] = int(entry['idle'].split(':')[0])
                entry['idle_minutes'] = int(entry['idle'].split(':')[1])

            if entry['idle'] and 'd' in entry['idle']:
                entry['idle_days'] = int(entry['idle'].replace('d', ''))

            entry['total_idle_minutes'] = (entry['idle_days'] * 1440) + \
                                          (entry['idle_hours'] * 60) + \
                                          entry['idle_minutes']

        if 'details' in entry:
            if not entry['details']:
                del entry['details']

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
        pattern = re.compile(r'([A-Z][a-z]{2}\s+\d{1,2}\s+)(\d\d:\d\d|\d{4})(\s?.+)?$')

        # remove header row from list
        second_half.pop(0)

        for index, line in enumerate(second_half):
            dt = re.search(pattern, line)
            if dt:
                if dt.group(1) and dt.group(2):
                    raw_output[index]['login_time'] = dt.group(1).strip() + ' ' + dt.group(2).strip()
                if dt.group(3):
                    raw_output[index]['details'] = dt.group(3).strip()

    if raw:
        return raw_output
    else:
        return _process(raw_output)
