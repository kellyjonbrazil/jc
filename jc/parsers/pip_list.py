"""jc - JSON CLI output utility `pip-list` command output parser

Usage (cli):

    $ pip list | jc --pip-list

    or

    $ jc pip list

Usage (module):

    import jc.parsers.pip_list
    result = jc.parsers.pip_list.parse(pip_list_command_output)

Schema:

    [
      {
        "package":     string,
        "version":     string,
        "location":    string
      }
    ]

Examples:

    $ pip list | jc --pip-list -p
    [
      {
        "package": "ansible",
        "version": "2.8.5"
      },
      {
        "package": "antlr4-python3-runtime",
        "version": "4.7.2"
      },
      {
        "package": "asn1crypto",
        "version": "0.24.0"
      },
      ...
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.4'
    description = '`pip list` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['pip list', 'pip3 list']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    # no further processing
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

        # detect legacy output type
        if ' (' in cleandata[0]:
            for row in cleandata:
                raw_output.append({'package': row.split(' (')[0],
                                   'version': row.split(' (')[1].rstrip(')')})

        # otherwise normal table output
        else:
            # clear separator line
            for i, line in reversed(list(enumerate(cleandata))):
                if '---' in line:
                    cleandata.pop(i)

            cleandata[0] = cleandata[0].lower()

            if cleandata:
                raw_output = jc.parsers.universal.simple_table_parse(cleandata)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
