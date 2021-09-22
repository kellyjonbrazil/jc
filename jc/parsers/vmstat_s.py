"""jc - JSON CLI output utility `vmstat` command output streaming parser

Usage (cli):

    $ vmstat | jc --vmstat-s

Usage (module):

    import jc.parsers.vmstat_s
    result = jc.parsers.vmstat_s.parse(vmstat_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "vmstat":            string,
      "_meta":                       # This object only exists if using -q or quiet=True
        {
          "success":    booean,      # true if successfully parsed, false if error
          "error":      string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ vmstat | jc --vmstat-s
    {example output}
    ...

    $ vmstat | jc --vmstat-s -r
    {example output}
    ...
"""
import jc.utils
from jc.utils import stream_success, stream_error


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`vmstat` command streaming parser'
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
