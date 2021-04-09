"""jc - JSON CLI output utility `env` and `printenv` command output parser

This parser will output a list of dictionaries each containing `name` and `value` keys. If you would like a simple dictionary output, then use the `-r` command-line option or the `raw=True` argument in the `parse()` function.

Usage (cli):

    $ env | jc --env

    or

    $ jc env

Usage (module):

    import jc.parsers.env
    result = jc.parsers.env.parse(env_command_output)

Schema:

    [
      {
        "name":     string,
        "value":    string
      }
    ]

Examples:

    $ env | jc --env -p
    [
      {
        "name": "XDG_SESSION_ID",
        "value": "1"
      },
      {
        "name": "HOSTNAME",
        "value": "localhost.localdomain"
      },
      {
        "name": "TERM",
        "value": "vt220"
      },
      {
        "name": "SHELL",
        "value": "/bin/bash"
      },
      {
        "name": "HISTSIZE",
        "value": "1000"
      },
      ...
    ]

    $ env | jc --env -p -r
    {
      "TERM": "xterm-256color",
      "SHELL": "/bin/bash",
      "USER": "root",
      "PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
      "PWD": "/root",
      "LANG": "en_US.UTF-8",
      "HOME": "/root",
      "LOGNAME": "root",
      "_": "/usr/bin/env"
    }
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`env` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['env', 'printenv']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    # rebuild output for added semantic information
    processed = []
    for k, v in proc_data.items():
        proc_line = {}
        proc_line['name'] = k
        proc_line['value'] = v
        processed.append(proc_line)

    return processed


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary of raw structured data or
        List of Dictionaries of processed structured data
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        for entry in cleandata:
            parsed_line = entry.split('=', maxsplit=1)
            raw_output[parsed_line[0]] = parsed_line[1]

    if raw:
        return raw_output
    else:
        return _process(raw_output)
