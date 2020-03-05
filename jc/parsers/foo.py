"""jc - JSON CLI output utility foo Parser

Usage:

    specify --foo as the first argument if the piped input is coming from foo

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ foo | jc --foo -p
    []

    $ foo | jc --foo -p -r
    []
"""
import jc.utils


class info():
    version = '1.0'
    description = 'foo command parser'
    author = 'John Doe'
    author_email = 'johndoe@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['foo']


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
            "foo":     string,
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

    for line in filter(None, data.splitlines()):
        # parse the content
        pass

    if raw:
        return raw_output
    else:
        return process(raw_output)
