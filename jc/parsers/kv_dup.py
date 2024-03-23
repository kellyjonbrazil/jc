r"""jc - JSON Convert `Key/Value` with duplicate key file and string parser

Supports files containing simple key/value pairs and preserves duplicate
values. All values are contained in lists/arrays.

- Delimiter can be `=` or `:`. Missing values are supported.
- Comment prefix can be `#` or `;`. Comments must be on their own line.
- If multi-line values are used, each line will be a separate item in the
  value list. Blank lines in multi-line values are not supported.

> Note: Values starting and ending with quotation marks will have the marks
> removed. If you would like to keep the quotation marks, use the `-r`
> command-line argument or the `raw=True` argument in `parse()`.

Usage (cli):

    $ cat foo.txt | jc --kv-dup

Usage (module):

    import jc
    result = jc.parse('kv_dup', kv_file_output)

Schema:

Key/Value document converted to a dictionary - see the python configparser
standard library documentation for more details.

    {
      "<key1>": [
                            string
      ],
      "<key2>": [
                            string
      ]
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
    occupation = "Pilot"

    $ cat keyvalue.txt | jc --kv-dup -p
    {
      "name": ["John Doe"],
      "address": ["555 California Drive"],
      "age": ["34"],
      "occupation": ["Engineer", "Pilot"]
    }
"""
import jc.parsers.ini_dup as ini_dup


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'Key/Value with duplicate key file and string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the ini-dup parser'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['generic', 'file', 'string']


__version__ = info.version


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary representing a Key/Value pair document.
    """
    # This parser is an alias of ini_dup.py
    ini_dup.info = info  # type: ignore
    ini_dup.__name__ = __name__
    return ini_dup.parse(data, raw, quiet)
