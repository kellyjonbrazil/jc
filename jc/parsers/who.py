"""jc - JSON CLI output utility who Parser

Usage:

    specify --who as the first argument if the piped input is coming from who

    accepts any of the following who options (or no options): -aTH

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ who -a | jc --who -p
    [
      {
        "event": "reboot",
        "time": "Feb 7 23:31",
        "pid": 1
      },
      {
        "user": "joeuser",
        "writeable_tty": "-",
        "tty": "console",
        "time": "Feb 7 23:32",
        "idle": "old",
        "pid": 105
      },
      {
        "user": "joeuser",
        "writeable_tty": "+",
        "tty": "ttys000",
        "time": "Feb 13 16:44",
        "idle": ".",
        "pid": 51217,
        "comment": "term=0 exit=0"
      },
      {
        "user": "joeuser",
        "writeable_tty": "?",
        "tty": "ttys003",
        "time": "Feb 28 08:59",
        "idle": "01:36",
        "pid": 41402
      },
      {
        "user": "joeuser",
        "writeable_tty": "+",
        "tty": "ttys004",
        "time": "Mar 1 16:35",
        "idle": ".",
        "pid": 15679,
        "from": "192.168.1.5"
      }
    ]

    $ who -a | jc --who -p -r
    [
      {
        "event": "reboot",
        "time": "Feb 7 23:31",
        "pid": "1"
      },
      {
        "user": "joeuser",
        "writeable_tty": "-",
        "tty": "console",
        "time": "Feb 7 23:32",
        "idle": "old",
        "pid": "105"
      },
      {
        "user": "joeuser",
        "writeable_tty": "+",
        "tty": "ttys000",
        "time": "Feb 13 16:44",
        "idle": ".",
        "pid": "51217",
        "comment": "term=0 exit=0"
      },
      {
        "user": "joeuser",
        "writeable_tty": "?",
        "tty": "ttys003",
        "time": "Feb 28 08:59",
        "idle": "01:36",
        "pid": "41402"
      },
      {
        "user": "joeuser",
        "writeable_tty": "+",
        "tty": "ttys004",
        "time": "Mar 1 16:35",
        "idle": ".",
        "pid": "15679",
        "from": "192.168.1.5"
      }
    ]
"""
import re
import jc.utils


class info():
    version = '1.1'
    description = 'who command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['who']


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
            "user":            string,
            "event":           string,
            "writeable_tty":   string,
            "tty":             string,
            "time":            string,
            "idle":            string,
            "pid":             integer,
            "from":            string,
            "comment":         string
          }
        ]
    """
    for entry in proc_data:
        int_list = ['pid']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

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

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        for line in cleandata:
            output_line = {}
            linedata = line.split()

            # clear headers, if they exist
            if ''.join(linedata[0:3]) == 'NAMELINETIME' \
               or ''.join(linedata[0:3]) == 'USERLINEWHEN':
                linedata.pop(0)
                continue

            # mac reboot line
            if linedata[0] == 'reboot':
                output_line['event'] = 'reboot'
                output_line['time'] = ' '.join(linedata[2:5])
                output_line['pid'] = linedata[6]
                raw_output.append(output_line)
                continue

            # linux reboot line
            if ''.join(linedata[0:2]) == 'systemboot':
                output_line['event'] = 'reboot'
                output_line['time'] = ' '.join(linedata[2:4])
                raw_output.append(output_line)
                continue

            # linux login line
            if linedata[0] == 'LOGIN':
                output_line['event'] = 'login'
                output_line['tty'] = linedata[1]
                output_line['time'] = ' '.join(linedata[2:4])
                output_line['pid'] = linedata[4]
                if len(linedata) > 5:
                    output_line['comment'] = ' '.join(linedata[5:])
                raw_output.append(output_line)
                continue

            # linux run-level
            if linedata[0] == 'run-level':
                output_line['event'] = ' '.join(linedata[0:2])
                output_line['time'] = ' '.join(linedata[2:4])
                raw_output.append(output_line)
                continue

            # mac run-level (ignore because not enough useful info)
            if linedata[1] == 'run-level':
                continue

            # pts lines with no user information
            if linedata[0].startswith('pts/'):
                output_line['tty'] = linedata[0]
                output_line['time'] = ' '.join(linedata[1:3])
                output_line['pid'] = linedata[3]
                output_line['comment'] = ' '.join(linedata[4:])
                raw_output.append(output_line)
                continue

            # user logins
            output_line['user'] = linedata.pop(0)

            if linedata[0] in '+-?':
                output_line['writeable_tty'] = linedata.pop(0)

            output_line['tty'] = linedata.pop(0)

            # mac
            if re.match(r'[JFMASOND][aepuco][nbrynlgptvc]', linedata[0]):
                output_line['time'] = ' '.join([linedata.pop(0),
                                                linedata.pop(0),
                                                linedata.pop(0)])
            # linux
            else:
                output_line['time'] = ' '.join([linedata.pop(0),
                                                linedata.pop(0)])

            # if just one more field, then it's the remote IP
            if len(linedata) == 1:
                output_line['from'] = linedata[0].replace('(', '').replace(')', '')
                raw_output.append(output_line)
                continue

            # extended info: idle
            if len(linedata) > 0:
                output_line['idle'] = linedata.pop(0)

            # extended info: pid
            if len(linedata) > 0:
                output_line['pid'] = linedata.pop(0)

            # extended info is from
            if len(linedata) > 0 and linedata[0].startswith('('):
                output_line['from'] = linedata[0].replace('(', '').replace(')', '')

            # else, extended info is comment
            elif len(linedata) > 0:
                output_line['comment'] = ' '.join(linedata)

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
