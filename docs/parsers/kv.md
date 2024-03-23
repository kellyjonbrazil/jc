[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.kv"></a>

# jc.parsers.kv

jc - JSON Convert `Key/Value` file and string parser

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

<a id="jc.parsers.kv.parse"></a>

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

    Dictionary representing a Key/Value pair document.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/kv.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/kv.py)

Version 2.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
