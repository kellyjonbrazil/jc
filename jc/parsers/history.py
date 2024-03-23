r"""jc - JSON Convert `history` command output parser

This parser will output a list of dictionaries each containing `line` and
`command` keys. If you would like a simple dictionary output, then use the
`-r` command-line option or the `raw=True` argument in the `parse()`
function.

The "Magic" syntax is not supported since the `history` command is a shell
builtin.

Usage (cli):

    $ history | jc --history

Usage (module):

    import jc
    result = jc.parse('history', history_command_output)

Schema:

    [
      {
        "line":     integer,
        "command":  string
      }
    ]

Examples:

    $ history | jc --history -p
    [
      {
        "line": 118,
        "command": "sleep 100"
      },
      {
        "line": 119,
        "command": "ls /bin"
      },
      {
        "line": 120,
        "command": "echo \"hello\""
      },
      {
        "line": 121,
        "command": "docker images"
      },
      ...
    ]

    $ history | jc --history -p -r
    {
      "118": "sleep 100",
      "119": "ls /bin",
      "120": "echo \"hello\"",
      "121": "docker images",
      ...
    }
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = '`history` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Optimizations by https://github.com/philippeitis'
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    tags = ['command']


__version__ = info.version


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
        proc_line = {
            'line': jc.utils.convert_to_int(k),
            'command': v,
        }
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

        Dictionary of raw structured data or
        List of Dictionaries of processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        linedata = data.splitlines()

        for entry in filter(None, linedata):
            try:
                number, command = entry.split(maxsplit=1)
                raw_output[number] = command
            except ValueError:
                # need to catch ValueError in case there is weird input from prior commands
                pass

    if raw:
        return raw_output
    else:
        return _process(raw_output)
