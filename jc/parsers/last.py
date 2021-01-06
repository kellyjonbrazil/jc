"""jc - JSON CLI output utility `last` and `lastb` command output parser

Supports -w and -F options.

Usage (cli):

    $ last | jc --last

    or

    $ jc last

Usage (module):

    import jc.parsers.last
    result = jc.parsers.last.parse(last_command_output)

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

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
from datetime import datetime
import jc.utils


class info():
    version = '1.4'
    description = 'last and lastb command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Enhancements by https://github.com/zerolagtime'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    magic_commands = ['last', 'lastb']


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
            "user":             string,
            "tty":              string,
            "hostname":         string,
            "login":            string,
            "logout":           string,
            "duration":         string,
            "login_epoch":      integer,   # available with last -F option
            "logout_epoch":     integer,   # available with last -F option
            "duration_seconds": integer    # available with last -F option
          }
        ]
    """
    for entry in proc_data:
        if 'user' in entry and entry['user'] == 'boot_time':
            entry['user'] = 'boot time'

        if 'tty' in entry and entry['tty'] == '~':
            entry['tty'] = None

        if 'tty' in entry and entry['tty'] == 'system_boot':
            entry['tty'] = 'system boot'

        if 'hostname' in entry and entry['hostname'] == '-':
            entry['hostname'] = None

        if 'hostname' in entry and entry['hostname'] is not None and entry['hostname'][0] == ":":
            entry['hostname'] = f'CONSOLE{entry["hostname"]}'

        if 'logout' in entry and entry['logout'] == 'still_logged_in':
            entry['logout'] = 'still logged in'

        if 'logout' in entry and entry['logout'] == 'gone_-_no_logout':
            entry['logout'] = 'gone - no logout'

        if 'login' in entry and re.match(r'.*\d\d:\d\d:\d\d \d\d\d\d.*',entry['login']):
            entry['login_epoch'] = int(datetime.strptime(entry['login'], '%a %b %d %H:%M:%S %Y').strftime('%s'))

        if 'logout' in entry and re.match(r'.*\d\d:\d\d:\d\d \d\d\d\d.*',entry['logout']):
            entry['logout_epoch'] = int(datetime.strptime(entry['logout'], '%a %b %d %H:%M:%S %Y').strftime('%s'))

        if 'login_epoch' in entry and 'logout_epoch' in entry:
            entry['duration_seconds'] = int(entry['logout_epoch']) - int(entry['login_epoch'])

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
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        for entry in cleandata:
            output_line = {}

            if entry.startswith('wtmp begins ') or entry.startswith('btmp begins ') or entry.startswith('utx.log begins '):
                continue

            entry = entry.replace('system boot', 'system_boot')
            entry = entry.replace('boot time', 'boot_time')
            entry = entry.replace('  still logged in', '- still_logged_in')
            entry = entry.replace('  gone - no logout', '- gone_-_no_logout')

            linedata = entry.split()
            if re.match(r'[MTWFS][ouerha][nedritnu] [JFMASOND][aepuco][nbrynlgptvc]', ' '.join(linedata[2:4])):
                linedata.insert(2, '-')

            # freebsd fix
            if linedata[0] == 'boot_time':
                linedata.insert(1, '-')
                linedata.insert(1, '~')

            output_line['user'] = linedata[0]
            output_line['tty'] = linedata[1]
            output_line['hostname'] = linedata[2]

            # last -F support
            if re.match(r'\d\d:\d\d:\d\d \d\d\d\d', ' '.join(linedata[6:8])):
                output_line['login'] = ' '.join(linedata[3:8])

                if len(linedata) > 9 and linedata[9] != 'crash' and linedata[9] != 'down':
                    output_line['logout'] = ' '.join(linedata[9:14])

                if len(linedata) > 9 and (linedata[9] == 'crash' or linedata[9] == 'down'):
                    output_line['logout'] = linedata[9]
                    # add more items to the list to line up duration
                    linedata.insert(10, '-')
                    linedata.insert(10, '-')
                    linedata.insert(10, '-')
                    linedata.insert(10, '-')

                if len(linedata) > 14:
                    output_line['duration'] = linedata[14].replace('(', '').replace(')', '')

            # normal last support
            else:
                output_line['login'] = ' '.join(linedata[3:7])

                if len(linedata) > 8:
                    output_line['logout'] = linedata[8]

                if len(linedata) > 9:
                    output_line['duration'] = linedata[9].replace('(', '').replace(')', '')

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
