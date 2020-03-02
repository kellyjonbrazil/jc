"""jc - JSON CLI output utility who Parser

Usage:

    specify --who as the first argument if the piped input is coming from who

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ who | jc --who -p
    []

    $ who | jc --who -p -r
    []
"""
import re
import jc.utils


class info():
    version = '1.0'
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
            "who":     string,
            "bar":     boolean,
            "baz":     integer
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

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if cleandata:
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

            # extended info: idle
            if len(linedata) > 0:
                output_line['idle'] = linedata.pop(0)

            # extended info: pid
            if len(linedata) > 0:
                output_line['pid'] = linedata.pop(0)

            # extended info: comment
            if len(linedata) > 0:
                output_line['comment'] = ' '.join(linedata)

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
