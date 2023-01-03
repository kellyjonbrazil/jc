"""jc - JSON Convert `INI` file parser

Parses standard `INI` files.

- Delimiter can be `=` or `:`. Missing values are supported.
- Comment prefix can be `#` or `;`. Comments must be on their own line.
- If duplicate keys are found, only the last value will be used.

> Note: If there is no top-level section identifier, then this parser will
> add a key named `_top_level_section_` with the top-level key/values
> included.

> Note: The section identifier `[DEFAULT]` is special and provides default
> values for the section keys that follow. To disable this behavior you must
> rename the `[DEFAULT]` section identifier to something else before
> parsing.

> Note: Values starting and ending with double or single quotation marks
> will have the marks removed. If you would like to keep the quotation
> marks, use the `-r` command-line argument or the `raw=True` argument in
> `parse()`.

Usage (cli):

    $ cat foo.ini | jc --ini

Usage (module):

    import jc
    result = jc.parse('ini', ini_file_output)

Schema:

ini document converted to a dictionary - see the python configparser
standard library documentation for more details.

    {
      "key1":       string,
      "key2":       string
    }

Examples:

    $ cat example.ini
    [DEFAULT]
    ServerAliveInterval = 45
    Compression = yes
    CompressionLevel = 9
    ForwardX11 = yes

    [bitbucket.org]
    User = hg

    [topsecret.server.com]
    Port = 50022
    ForwardX11 = no

    $ cat example.ini | jc --ini -p
    {
      "bitbucket.org": {
        "ServerAliveInterval": "45",
        "Compression": "yes",
        "CompressionLevel": "9",
        "ForwardX11": "yes",
        "User": "hg"
      },
      "topsecret.server.com": {
        "ServerAliveInterval": "45",
        "Compression": "yes",
        "CompressionLevel": "9",
        "ForwardX11": "no",
        "Port": "50022"
      }
    }
"""
import jc.utils
import configparser


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.0'
    description = 'INI file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using configparser from the python standard library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary representing an ini or simple key/value pair document.
    """
    # remove quotation marks from beginning and end of values
    for heading in proc_data:
        for key, value in proc_data[heading].items():
            if value is not None and value.startswith('"') and value.endswith('"'):
                proc_data[heading][key] = value.lstrip('"').rstrip('"')

            elif value is not None and value.startswith("'") and value.endswith("'"):
                proc_data[heading][key] = value.lstrip("'").rstrip("'")

            elif value is None:
                proc_data[heading][key] = ''

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary representing the ini file
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):

        ini = configparser.ConfigParser(allow_no_value=True,
                                        interpolation=None,
                                        strict=False)

        # don't convert keys to lower-case:
        ini.optionxform = lambda option: option

        try:
            ini.read_string(data)
            raw_output = {s: dict(ini.items(s)) for s in ini.sections()}

        except configparser.MissingSectionHeaderError:
            data = '[_top_level_section_]\n' + data
            ini.read_string(data)
            raw_output = {s: dict(ini.items(s)) for s in ini.sections()}

    if raw:
        return raw_output
    else:
        return _process(raw_output)
