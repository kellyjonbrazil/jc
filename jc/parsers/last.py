"""jc - JSON CLI output utility last Parser

Usage:

    specify --last as the first argument if the piped input is coming from last or lastb

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

Examples:

    $ last | jc --last -p
    []

    $ last | jc --last -p -r
    []
"""
import re
import jc.utils


class info():
    version = '1.0'
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
            "last":     string,
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
        for entry in cleandata:
            output_line = {}

            if entry.startswith('wtmp begins '):
                continue

            entry = entry.replace('system boot', 'system_boot')
            entry = entry.replace('  still logged in', '- still_logged_in')

            linedata = entry.split()
            if re.match('[MTWFS][ouerha][nedritnu] [JFMASOND][aepuco][nbrynlgptvc]', ' '.join(linedata[2:4])):
                linedata.insert(2, '-')

            output_line['user'] = linedata[0]
            output_line['tty'] = linedata[1]
            output_line['hostname'] = linedata[2]
            output_line['login'] = ' '.join(linedata[3:7])

            if len(linedata) > 8:
                print(linedata)
                output_line['logout'] = linedata[8]

            if len(linedata) > 9:
                output_line['duration'] = linedata[9].replace('(', '').replace(')', '')

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
