[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ini_dup"></a>

# jc.parsers.ini_dup

jc - JSON Convert INI with duplicate key file parser

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

<a id="jc.parsers.ini_dup.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary representing the INI file.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/ini_dup.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ini_dup.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
