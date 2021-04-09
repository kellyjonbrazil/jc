"""jc - JSON CLI output utility `Key/Value` file parser

Supports files containing simple key/value pairs. Delimiter can be `=` or `:`. Missing values are supported. Comment prefix can be `#` or `;`. Comments must be on their own line.

Note: Values starting and ending with quotation marks will have the marks removed. If you would like to keep the quotation marks, use the `-r` command-line argument or the `raw=True` argument in `parse()`.

Usage (cli):

    $ cat foo.txt | jc --kv

Usage (module):

    import jc.parsers.kv
    result = jc.parsers.kv.parse(kv_file_output)

Schema:

    key/value document converted to a dictionary - see configparser standard library documentation for more details.

    {
      "key1":       string,
      "key2":       string
    }

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
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
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
