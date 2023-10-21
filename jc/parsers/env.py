"""jc - JSON Convert `env` and `printenv` command output parser

This parser will output a list of dictionaries each containing `name` and
`value` keys. If you would like a simple dictionary output, then use the
`-r` command-line option or the `raw=True` argument in the `parse()`
function.

Usage (cli):

    $ env | jc --env

or

    $ jc env

Usage (module):

    import jc
    result = jc.parse('env', env_command_output)

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
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`env` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['env', 'printenv']
    tags = ['command']


__version__ = info.version

VAR_DEF_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*=\S*.*$')

def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
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
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary of raw structured data or (default)
        List of Dictionaries of processed structured data (raw)
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}
    key = ''
    value = None

    if jc.utils.has_data(data):
        for line in data.splitlines():
            if VAR_DEF_PATTERN.match(line):
                if not value is None:
                    raw_output[key] = value
                key, value = line.split('=', maxsplit=1)
                continue

            if not value is None:
                value = value + '\n' + line

    if not value is None:
        raw_output[key] = value

    return raw_output if raw else _process(raw_output)

