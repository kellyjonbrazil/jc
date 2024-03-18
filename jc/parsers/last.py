r"""jc - JSON Convert `last` and `lastb` command output parser

Supports `-w`, `-F`, and `-x` options.

Calculated epoch time fields are naive (i.e. based on the local time of the
system the parser is run on) since there is no timezone information in the
`last` command output.

Usage (cli):

    $ last | jc --last

or

    $ jc last

Usage (module):

    import jc
    result = jc.parse('last', last_command_output)

Schema:

    [
      {
        "user":             string,
        "tty":              string,
        "hostname":         string,
        "login":            string,
        "logout":           string,
        "duration":         string,
        "login_epoch":      integer,  # (naive) available w/last -F option
        "logout_epoch":     integer,  # (naive) available w/last -F option
        "duration_seconds": integer   # available w/last -F option
      }
    ]

Examples:

    $ last -F | jc --last -p
    [
      {
        "user": "kbrazil",
        "tty": "ttys002",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "still logged in"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "Mon Dec 28 17:25:01 2020",
        "duration": "00:00",
        "login_epoch": 1565891826,
        "logout_epoch": 1565895404,
        "duration_seconds": 3578
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "Mon Dec 28 17:25:01 2020",
        "duration": "00:00",
        "login_epoch": 1565891826,
        "logout_epoch": 1565895404,
        "duration_seconds": 3578
      },
      ...
    ]

    $ last | jc --last -p -r
    [
      {
        "user": "kbrazil",
        "tty": "ttys002",
        "hostname": "-",
        "login": "Thu Feb 27 14:31",
        "logout": "still_logged_in"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": "-",
        "login": "Thu Feb 27 10:38",
        "logout": "10:38",
        "duration": "00:00"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": "-",
        "login": "Thu Feb 27 10:18",
        "logout": "10:18",
        "duration": "00:00"
      },
      ...
    ]
"""
import re
import jc.utils

DATE_RE = re.compile(r'[MTWFS][ouerha][nedritnu] [JFMASOND][aepuco][nbrynlgptvc]')
LAST_F_DATE_RE = re.compile(r'\d\d:\d\d:\d\d \d\d\d\d')
LOGIN_LOGOUT_EPOCH_RE = re.compile(r'.*\d\d:\d\d:\d\d \d\d\d\d.*')
LOGOUT_IGNORED_EVENTS = ['down', 'crash']


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.9'
    description = '`last` and `lastb` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Enhancements by https://github.com/zerolagtime'
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    magic_commands = ['last', 'lastb']
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
    for entry in proc_data:
        if 'user' in entry and entry['user'] == 'boot_time':
            entry['user'] = 'boot time'

        if 'tty' in entry and entry['tty'] == '~':
            entry['tty'] = None

        if 'hostname' in entry and entry['hostname'] == '-':
            entry['hostname'] = None

        if 'hostname' in entry and entry['hostname'] is not None and entry['hostname'][0] == ":":
            entry['hostname'] = f'CONSOLE{entry["hostname"]}'

        if 'logout' in entry and entry['logout'] == 'still_logged_in':
            entry['logout'] = 'still logged in'

        if 'logout' in entry and entry['logout'] == 'gone_-_no_logout':
            entry['logout'] = 'gone - no logout'

        if 'login' in entry and LOGIN_LOGOUT_EPOCH_RE.match(entry['login']):
            timestamp = jc.utils.timestamp(entry['login'])
            entry['login_epoch'] = timestamp.naive

        if 'logout' in entry and LOGIN_LOGOUT_EPOCH_RE.match(entry['logout']):
            timestamp = jc.utils.timestamp(entry['logout'])
            entry['logout_epoch'] = timestamp.naive

        if 'login_epoch' in entry and 'logout_epoch' in entry:
            entry['duration_seconds'] = entry['logout_epoch'] - entry['login_epoch']

        if 'duration' in entry and re.match(r'^\d+\+', entry['duration']):
            m = re.match(r'^(?P<days>\d+)\+(?P<hours>\d\d):(?P<minutes>\d\d)', entry['duration'])
            days, hours, minutes = m.groups()
            entry['duration'] = f'{int(days)*24 + int(hours)}:{minutes}'

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

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if not jc.utils.has_data(data):
        return []

    for entry in cleandata:
        output_line = {}

        if any(
            entry.startswith(f'{prefix} begins ')
            for prefix in ['wtmp', 'btmp', 'utx.log']
        ):
            continue

        entry = entry.replace('boot time', 'boot_time')
        entry = entry.replace('  still logged in', '- still_logged_in')
        entry = entry.replace('  gone - no logout', '- gone_-_no_logout')

        linedata = entry.split()

        # Adding "-" before the date part.
        if DATE_RE.match(' '.join(linedata[2:4])):
            linedata.insert(2, '-')

        # freebsd fix
        if linedata[0] == 'boot_time':
            linedata.insert(1, '-')
            linedata.insert(1, '~')

        output_line['user'] = linedata[0]

        # Fix for last -x (runlevel).
        if output_line['user'] == 'runlevel' and  linedata[1] == '(to':
            linedata[1] += f' {linedata.pop(2)} {linedata.pop(2)}'
        elif output_line['user'] in ['reboot', 'shutdown'] and linedata[1] == 'system':  # system down\system boot
            linedata[1] += f' {linedata.pop(2)}'

        output_line['tty'] = linedata[1]
        output_line['hostname'] = linedata[2]

        # last -F support
        if LAST_F_DATE_RE.match(' '.join(linedata[6:8])):
            output_line['login'] = ' '.join(linedata[3:8])

            if len(linedata) > 9:
                if linedata[9] not in LOGOUT_IGNORED_EVENTS:
                    output_line['logout'] = ' '.join(linedata[9:14])
                else:
                    output_line['logout'] = linedata[9]
                    # add more items to the list to line up duration
                    for _ in range(4):
                        linedata.insert(10, '-')

            if len(linedata) > 14:
                output_line['duration'] = linedata[14].replace('(', '').replace(')', '')
        else: # normal last support
            output_line['login'] = ' '.join(linedata[3:7])

            if len(linedata) > 8:
                output_line['logout'] = linedata[8]

            if len(linedata) > 9:
                output_line['duration'] = linedata[9].replace('(', '').replace(')', '')

        raw_output.append(output_line)

    if raw:
        return raw_output

    return _process(raw_output)
