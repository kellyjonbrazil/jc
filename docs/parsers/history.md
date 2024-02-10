[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.history"></a>

# jc.parsers.history

jc - JSON Convert `history` command output parser

This parser will output a list of dictionaries each containing `line` and
`command` keys. If you would like a simple dictionary output, then use the
`-r` command-line option or the `raw=True` argument in the `parse()`
function.

The "Magic" syntax is not supported since the `history` command is a shell
builtin.

Usage (cli):

    $ history | jc --history

Usage (module):

    import jc
    result = jc.parse('history', history_command_output)

Schema:

    [
      {
        "line":     integer,
        "command":  string
      }
    ]

Examples:

    $ history | jc --history -p
    [
      {
        "line": 118,
        "command": "sleep 100"
      },
      {
        "line": 119,
        "command": "ls /bin"
      },
      {
        "line": 120,
        "command": "echo \"hello\""
      },
      {
        "line": 121,
        "command": "docker images"
      },
      ...
    ]

    $ history | jc --history -p -r
    {
      "118": "sleep 100",
      "119": "ls /bin",
      "120": "echo \"hello\"",
      "121": "docker images",
      ...
    }

<a id="jc.parsers.history.parse"></a>

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

    Dictionary of raw structured data or
    List of Dictionaries of processed structured data

### Parser Information
Compatibility:  linux, darwin, cygwin, aix, freebsd

Source: [`jc/parsers/history.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/history.py)

Version 1.7 by Kelly Brazil (kellyjonbrazil@gmail.com)
