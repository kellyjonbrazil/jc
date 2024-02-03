"""jc - JSON Convert INI file parser with nested groups

Parses standard INI files.

- Delimiter can be `=` or `:`. Missing values are supported.
- Comment prefix can be `#` or `;`. Comments must be on their own line.
- If duplicate keys are found, only the last value will be used.
- If any section names have the same name as a top-level key, the top-level
  key will be overwritten by the section data.

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

INI document converted to a dictionary - see the python configparser
standard library documentation for more details.

    {
      "<key1>":               string,
      "<key2>":               string,
      "<section1>": {
        "<key1>":             string,
        "<key2>":             string
      },
      "<section2>": {
        "<key1>":             string,
        "<key2>":             string
      }
    }

Examples:

    $ cat example.ini
    foo = fiz
    bar = buz

    [section1]
    fruit = apple
    color = blue

    [section2]
    fruit = pear
    color = green

    $ cat example.ini | jc --ini -p
    {
      "foo": "fiz",
      "bar": "buz",
      "section1": {
        "fruit": "apple",
        "color": "blue"
      },
      "section2": {
        "fruit": "pear",
        "color": "green"
      }
    }
"""
import jc.parsers.ini as ini
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'INI file parser with nested groups'
    author = 'Michael Nietzold'
    author_email = 'https://github.com/muescha'
    details = 'Using ini paser (configparser) from the python standard library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version

def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary representing the INI file.
    """

    convert_numberkeys_to_list=True

    result = jc.utils.convert_dict_to_nested_dict(proc_data,"][")
    if convert_numberkeys_to_list:
        result = jc.utils.convert_dict_with_numberkeys_to_lists(result)

    return result


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary representing the INI file.
    """
    ini.info = info  # type: ignore
    raw_output = ini.parse(data, raw, quiet)
    return raw_output if raw else _process(raw_output)

