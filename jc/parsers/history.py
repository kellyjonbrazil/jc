"""jc - JSON CLI output utility history Parser

Usage:

    specify --history as the first argument if the piped input is coming from history

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

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
    version = '1.3'
    description = 'history command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Optimizations by https://github.com/philippeitis'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']


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
            "line":     integer,
            "command":  string
          }
        ]
    """

    # rebuild output for added semantic information
    processed = []
    for k, v in proc_data.items():
        proc_line = {
            'line': int(k) if k.isdigit() else None,
            'command': v,
        }
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
        list of dictionaries of processed structured data
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):

        # split lines and clear out any non-ascii chars
        linedata = data.encode('ascii', errors='ignore').decode().splitlines()

        # Skip any blank lines
        for entry in filter(None, linedata):
            try:
                parsed_line = entry.split(maxsplit=1)
                raw_output[parsed_line[0]] = parsed_line[1]
            except IndexError:
                # need to catch indexerror in case there is weird input from prior commands
                pass

    if raw:
        return raw_output
    else:
        return process(raw_output)
