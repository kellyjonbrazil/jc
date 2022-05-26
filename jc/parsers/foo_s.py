"""jc - JSON Convert `foo` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

<<Short foo description and caveats>>

Usage (cli):

    $ foo | jc --foo-s

Usage (module):

    import jc

    result = jc.parse('foo_s', foo_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "foo":            string,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
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
from typing import Dict, Iterable, Union
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`foo` command streaming parser'
    author = 'John Doe'
    author_email = 'johndoe@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    streaming = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float,
    # bool conversions and timestamps

    return proc_data


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Union[Iterable[Dict], tuple]:
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True


    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    for line in data:
        try:
            streaming_line_input_type_check(line)
            output_line: Dict = {}

            # parse the content here
            # check out helper functions in jc.utils
            # and jc.parsers.universal

            if output_line:
                yield output_line if raw else _process(output_line)
            else:
                raise ParseError('Not foo data')

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
