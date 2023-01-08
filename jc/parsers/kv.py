"""jc - JSON Convert `Key/Value` file and string parser

Supports files containing simple key/value pairs.

- Delimiter can be `=` or `:`. Missing values are supported.
- Comment prefix can be `#` or `;`. Comments must be on their own line.
- If duplicate keys are found, only the last value will be used.

> Note: Values starting and ending with quotation marks will have the marks
> removed. If you would like to keep the quotation marks, use the `-r`
> command-line argument or the `raw=True` argument in `parse()`.

Usage (cli):

    $ cat foo.txt | jc --kv

Usage (module):

    import jc
    result = jc.parse('kv', kv_file_output)

Schema:

Key/Value document converted to a dictionary - see the python configparser
standard library documentation for more details.

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

    $ cat keyvalue.txt | jc --kv -p
    {
      "name": "John Doe",
      "address": "555 California Drive",
      "age": "34",
      "occupation": "Engineer"
    }
"""
import jc.utils
import configparser


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.0'
    description = 'Key/Value file and string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using configparser from the python standard library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['generic', 'file', 'string']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary representing a Key/Value pair document.
    """
    # remove quotation marks from beginning and end of values
    for key in proc_data:
        if proc_data[key] is None:
            proc_data[key] = ''

        elif proc_data[key].startswith('"') and proc_data[key].endswith('"'):
            proc_data[key] = proc_data[key][1:-1]

        elif proc_data[key].startswith("'") and proc_data[key].endswith("'"):
            proc_data[key] = proc_data[key][1:-1]

    return proc_data


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
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):

        kv_parser = configparser.ConfigParser(
            allow_no_value=True,
            interpolation=None,
            default_section=None,
            strict=False
        )

        # don't convert keys to lower-case:
        kv_parser.optionxform = lambda option: option

        data = '[data]\n' + data
        kv_parser.read_string(data)
        output_dict = {s: dict(kv_parser.items(s)) for s in kv_parser.sections()}
        for key, value in output_dict['data'].items():
            raw_output[key] = value

    return raw_output if raw else _process(raw_output)

