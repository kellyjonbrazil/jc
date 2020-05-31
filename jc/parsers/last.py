"""jc - JSON CLI output utility last Parser

Usage:

    specify --last as the first argument if the piped input is coming from last or lastb

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

Examples:

    $ last | jc --last -p
    [
      {
        "user": "kbrazil",
        "tty": "ttys002",
        "hostname": null,
        "login": "Thu Feb 27 14:31",
        "logout": "still logged in"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Thu Feb 27 10:38",
        "logout": "10:38",
        "duration": "00:00"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Thu Feb 27 10:18",
        "logout": "10:18",
        "duration": "00:00"
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


class info():
    version = '1.2'
    description = 'last and lastb command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    magic_commands = ['last', 'lastb']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "user":       string,
            "tty":        string,
            "hostname":   string,
            "login":      string,
            "logout":     string,
            "duration":   string
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

        if 'logout' in entry and entry['logout'] == 'still_logged_in':
            entry['logout'] = 'still logged in'

        if 'logout' in entry and entry['logout'] == 'gone_-_no_logout':
            entry['logout'] = 'gone - no logout'

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if cleandata:
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
