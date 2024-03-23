[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pip_list"></a>

# jc.parsers.pip_list

jc - JSON Convert `pip-list` command output parser

Usage (cli):

    $ pip list | jc --pip-list

or

    $ jc pip list

Usage (module):

    import jc
    result = jc.parse('pip_list', pip_list_command_output)

Schema:

    [
      {
        "package":     string,
        "version":     string,
        "location":    string
      }
    ]

Examples:

    $ pip list | jc --pip-list -p
    [
      {
        "package": "ansible",
        "version": "2.8.5"
      },
      {
        "package": "antlr4-python3-runtime",
        "version": "4.7.2"
      },
      {
        "package": "asn1crypto",
        "version": "0.24.0"
      },
      ...
    ]

<a id="jc.parsers.pip_list.parse"></a>

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

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/pip_list.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/pip_list.py)

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
