"""jc - JSON CLI output utility `foo` command output streaming parser

Usage (cli):

    $ foo | jc --foo_s

Usage (module):

    import jc.parsers.foo_s
    result = jc.parsers.foo_s.parse(foo_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "foo":            string,
      "_meta":                       # This object only exists if using -q or quiet=True
        {
          "success":    booean,      # true if successfully parsed, false if error
          "error":      string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ foo | jc --foo-s
    {example output}
    ...

    $ foo | jc --foo-s -r
    {example output}
    ...
"""
import jc.utils
from jc.utils import stream_success, stream_error


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`foo` command streaming parser'
    author = 'John Doe'
    author_email = 'johndoe@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    streaming = True


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    #
    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool conversions and timestamps
    #

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing generator function. Returns an iterator object.

    Parameters:

        data:        (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
        raw:         (boolean)   output preprocessed JSON if True
        quiet:       (boolean)   suppress warning messages and ignore parsing exceptions if True

    Yields:

        Dictionary. Raw or processed structured data.

    Returns:

        Iterator object
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    for line in data:
        try:
            #
            # parse the input here
            #

            yield stream_success(output_line, quiet) if raw else stream_success(_process(output_line), quiet)
            
        except Exception as e:
            yield stream_error(e, quiet, line)
