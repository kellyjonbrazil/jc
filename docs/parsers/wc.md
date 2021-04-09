[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.wc
jc - JSON CLI output utility `wc` command output parser

Usage (cli):

    $ wc file.txt | jc --wc

    or

    $ jc wc file.txt

Usage (module):

    import jc.parsers.wc
    result = jc.parsers.wc.parse(wc_command_output)

Schema:

    [
      {
        "filename":     string,
        "lines":        integer,
        "words":        integer,
        "characters":   integer
      }
    ]

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ wc * | jc --wc -p
    [
      {
        "filename": "airport-I.json",
        "lines": 1,
        "words": 30,
        "characters": 307
      },
      {
        "filename": "airport-I.out",
        "lines": 15,
        "words": 33,
        "characters": 348
      },
      {
        "filename": "airport-s.json",
        "lines": 1,
        "words": 202,
        "characters": 2152
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
Compatibility:  linux, darwin, cygwin, aix, freebsd

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
