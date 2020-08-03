"""jc - JSON CLI output utility Key/Value File Parser

Usage:

    Specify --kv as the first argument if the piped input is coming from a simple
    key/value pair file. Delimiter can be '=' or ':'. Missing values are supported.
    Comment prefix can be '#' or ';'. Comments must be on their own line.

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ cat keyvalue.txt
    # this file contains key/value pairs
    name = John Doe
    address=555 California Drive
    age: 34
    ; comments can include # or ;
    # delimiter can be = or :
    # quoted values have quotation marks stripped by default
    # but can be preserved with the -r argument
    occupation:"Engineer"

    $ cat keyvalue.txt | jc --ini -p
    {
      "name": "John Doe",
      "address": "555 California Drive",
      "age": "34",
      "occupation": "Engineer"
    }
"""


class info():
    version = '1.0'
    description = 'Key/Value file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'This is a wrapper for the INI parser'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

        Note: this is just a wrapper for jc.parsers.ini

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary representing the key/value file
    """
    import jc.parsers.ini
    return jc.parsers.ini.parse(data, raw=raw, quiet=quiet)
