"""jc - JSON CLI output utility /etc/passwd file Parser

Usage:

    specify --passwd as the first argument if the piped input is coming from /etc/passwd

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

Examples:

    $ cat /etc/passwd | jc --passwd -p
    [
      {
        "username": "nobody",
        "password": "*",
        "uid": -2,
        "gid": -2,
        "comment": "Unprivileged User",
        "home": "/var/empty",
        "shell": "/usr/bin/false"
      },
      {
        "username": "root",
        "password": "*",
        "uid": 0,
        "gid": 0,
        "comment": "System Administrator",
        "home": "/var/root",
        "shell": "/bin/sh"
      },
      {
        "username": "daemon",
        "password": "*",
        "uid": 1,
        "gid": 1,
        "comment": "System Services",
        "home": "/var/root",
        "shell": "/usr/bin/false"
      },
      ...
    ]

    $ cat /etc/passwd | jc --passwd -p -r
    [
      {
        "username": "nobody",
        "password": "*",
        "uid": "-2",
        "gid": "-2",
        "comment": "Unprivileged User",
        "home": "/var/empty",
        "shell": "/usr/bin/false"
      },
      {
        "username": "root",
        "password": "*",
        "uid": "0",
        "gid": "0",
        "comment": "System Administrator",
        "home": "/var/root",
        "shell": "/bin/sh"
      },
      {
        "username": "daemon",
        "password": "*",
        "uid": "1",
        "gid": "1",
        "comment": "System Services",
        "home": "/var/root",
        "shell": "/usr/bin/false"
      },
      ...
    ]
"""
import jc.utils


class info():
    version = '1.0'
    description = '/etc/passwd file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'aix', 'freebsd']


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
            "username":  string,
            "password":  string,
            "uid":       integer,
            "gid":       integer,
            "comment":   string,
            "home":      string,
            "shell":     string
          }
        ]
    """
    for entry in proc_data:
        int_list = ['uid', 'gid']
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
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if cleandata:
        for entry in cleandata:
            if entry.startswith('#'):
                continue

            output_line = {}
            fields = entry.split(':')

            output_line['username'] = fields[0]
            output_line['password'] = fields[1]
            output_line['uid'] = fields[2]
            output_line['gid'] = fields[3]
            output_line['comment'] = fields[4]
            output_line['home'] = fields[5]
            output_line['shell'] = fields[6]

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
