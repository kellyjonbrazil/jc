[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.pip_list
jc - JSON CLI output utility `pip-list` command output parser

Usage (cli):

    $ pip list | jc --pip-list

    or

    $ jc pip list

Usage (module):

    import jc.parsers.pip_list
    result = jc.parsers.pip_list.parse(pip_list_command_output)

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


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
