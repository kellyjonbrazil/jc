[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.wc"></a>

# jc.parsers.wc

jc - JSON Convert `wc` command output parser

Usage (cli):

    $ wc file.txt | jc --wc

or

    $ jc wc file.txt

Usage (module):

    import jc
    result = jc.parse('wc', wc_command_output)

Schema:

    [
      {
        "filename":     string,
        "lines":        integer,
        "words":        integer,
        "characters":   integer
      }
    ]

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

<a id="jc.parsers.wc.parse"></a>

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
Compatibility:  linux, darwin, cygwin, aix, freebsd

Source: [`jc/parsers/wc.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/wc.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
