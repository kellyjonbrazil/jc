"""jc - JSON Convert INI file parser

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
import jc.utils
import configparser
import uuid


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.1'
    description = 'INI file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using configparser from the python standard library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


class MyDict(dict):
    def __setitem__(self, key, value):
        # convert None values to empty string
        if value is None:
            self[key] = ''

        else:
            super().__setitem__(key, value)


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary representing the INI file.
    """
    # remove quotation marks from beginning and end of values
    for k, v in proc_data.items():
        if isinstance(v, dict):
            for key, value in v.items():
                v[key] = jc.utils.remove_quotes(value)
            continue

        proc_data[k] = jc.utils.remove_quotes(v)

    return proc_data


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
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):

        ini_parser = configparser.ConfigParser(
            dict_type = MyDict,
            allow_no_value=True,
            interpolation=None,
            default_section=None,
            strict=False
        )

        # don't convert keys to lower-case:
        ini_parser.optionxform = lambda option: option

        try:
            ini_parser.read_string(data)
            raw_output = {s: dict(ini_parser.items(s)) for s in ini_parser.sections()}

        except configparser.MissingSectionHeaderError:
            # find a top-level section name that will not collide with any existing ones
            while True:
                my_uuid = str(uuid.uuid4())
                if my_uuid not in data:
                    break

            data = f'[{my_uuid}]\n' + data
            ini_parser.read_string(data)
            temp_dict = {s: dict(ini_parser.items(s)) for s in ini_parser.sections()}

            # move items under fake top-level sections to the root
            raw_output = temp_dict.pop(my_uuid)

            # get the rest of the sections
            raw_output.update(temp_dict)

    return raw_output if raw else _process(raw_output)

