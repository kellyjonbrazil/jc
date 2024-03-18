r"""jc - JSON Convert INI with duplicate key file parser

Parses standard INI files and preserves duplicate values. All values are
contained in lists/arrays.

- Delimiter can be `=` or `:`. Missing values are supported.
- Comment prefix can be `#` or `;`. Comments must be on their own line.
- If any section names have the same name as a top-level key, the top-level
  key will be overwritten by the section data.
- If multi-line values are used, each line will be a separate item in the
  value list. Blank lines in multi-line values are not supported.

> Note: Values starting and ending with double or single quotation marks
> will have the marks removed. If you would like to keep the quotation
> marks, use the `-r` command-line argument or the `raw=True` argument in
> `parse()`.

Usage (cli):

    $ cat foo.ini | jc --ini-dup

Usage (module):

    import jc
    result = jc.parse('ini_dup', ini_file_output)

Schema:

INI document converted to a dictionary - see the python configparser
standard library documentation for more details.

    {
      "<key1>": [
                            string
      ],
      "<key2>": [
                            string
      ],
      "<section1>": {
        "<key1>": [
                            string
        ],
        "<key2>": [
                            string
        ]
      }
    }

Examples:

    $ cat example.ini
    foo = fiz
    bar = buz

    [section1]
    fruit = apple
    color = blue
    color = red

    [section2]
    fruit = pear
    fruit = peach
    color = green

    $ cat example.ini | jc --ini-dup -p
    {
      "foo": [
        "fiz"
      ],
      "bar": [
        "buz"
      ],
      "section1": {
        "fruit": [
          "apple"
        ],
        "color": [
          "blue",
          "red"
        ]
      },
      "section2": {
        "fruit": [
          "pear",
          "peach"
        ],
        "color": [
          "green"
        ]
      }
    }
"""
import jc.utils
import configparser
import uuid


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = 'INI with duplicate key file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using configparser from the python standard library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


class MultiDict(dict):
    # https://stackoverflow.com/a/38286559/12303989
    def __setitem__(self, key, value):
        if value is None:
            self[key] = ['']

        if key in self:
            if isinstance(value, list):
                self[key].extend(value)

            elif isinstance(value, str):
                if len(self[key])>1:
                    return

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
                if isinstance(value, list):
                    v[key] = [jc.utils.remove_quotes(x) for x in value]
                else:
                    v[key] = jc.utils.remove_quotes(value)
            continue

        elif isinstance(v, list):
            proc_data[k] = [jc.utils.remove_quotes(x) for x in v]

        else:
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
            dict_type = MultiDict,
            allow_no_value=True,
            interpolation=None,
            default_section=None,
            empty_lines_in_values=False,
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
