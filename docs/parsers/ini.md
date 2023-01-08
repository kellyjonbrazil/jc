[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ini"></a>

# jc.parsers.ini

jc - JSON Convert `INI` file parser

Parses standard `INI` files.

- Delimiter can be `=` or `:`. Missing values are supported.
- Comment prefix can be `#` or `;`. Comments must be on their own line.
- If duplicate keys are found, only the last value will be used.

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
      "key1":       string,
      "key2":       string
    }

Examples:

    $ cat example.ini
    foo = bar
    baz = buz

    [section1]
    key1 = value1
    key2 = value2

    [section2]
    key1 = value1
    key2 = value2

    $ cat example.ini | jc --ini -p
    {
      "foo": "bar",
      "baz": "buz",
      "section1": {
        "key1": "value1",
        "key2": "value2"
      },
      "section2": {
        "key1": "value1",
        "key2": "value2"
      }
    }

<a id="jc.parsers.ini.parse"></a>

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

Version 2.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
