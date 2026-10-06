[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.who"></a>

# jc.parsers.who

jc - JSON Convert `who` command output parser

Accepts any of the following who options (or no options): `-aTH`

The `epoch` calculated timestamp field is naive. (i.e. based on the local
time of the system the parser is run on)

Usage (cli):

    $ who | jc --who

or

    $ jc who

Usage (module):

    import jc
    result = jc.parse('who', who_command_output)

Schema:

    [
      {
        "user":            string,
        "event":           string,
        "writeable_tty":   string,
        "process":         string,
        "tty":             string,
        "time":            string,
        "epoch":           integer,     # [0]
        "idle":            string,
        "pid":             integer,
        "from":            string,
        "comment":         string
      }
    ]

    [0] naive timestamp. null if time cannot be converted

Examples:

    $ who -a | jc --who -p
    [
      {
        "event": "reboot",
        "time": "Feb 7 23:31",
        "pid": 1,
        "epoch": null
      },
      {
        "user": "joeuser",
        "writeable_tty": "-",
        "tty": "console",
        "time": "Feb 7 23:32",
        "idle": "old",
        "pid": 105,
        "epoch": null
      },
      {
        "user": "joeuser",
        "writeable_tty": "+",
        "tty": "ttys000",
        "time": "Feb 13 16:44",
        "idle": ".",
        "pid": 51217,
        "comment": "term=0 exit=0",
        "epoch": null
      },
      {
        "user": "joeuser",
        "writeable_tty": "?",
        "tty": "ttys003",
        "time": "Feb 28 08:59",
        "idle": "01:36",
        "pid": 41402,
        "epoch": null
      },
      {
        "user": "joeuser",
        "writeable_tty": "+",
        "tty": "ttys004",
        "time": "Mar 1 16:35",
        "idle": ".",
        "pid": 15679,
        "from": "192.168.1.5",
        "epoch": null
      }
    ]

    $ who -a | jc --who -p -r
    [
      {
        "event": "reboot",
        "time": "Feb 7 23:31",
        "pid": "1"
      },
      {
        "user": "joeuser",
        "writeable_tty": "-",
        "tty": "console",
        "time": "Feb 7 23:32",
        "idle": "old",
        "pid": "105"
      },
      {
        "user": "joeuser",
        "writeable_tty": "+",
        "tty": "ttys000",
        "time": "Feb 13 16:44",
        "idle": ".",
        "pid": "51217",
        "comment": "term=0 exit=0"
      },
      {
        "user": "joeuser",
        "writeable_tty": "?",
        "tty": "ttys003",
        "time": "Feb 28 08:59",
        "idle": "01:36",
        "pid": "41402"
      },
      {
        "user": "joeuser",
        "writeable_tty": "+",
        "tty": "ttys004",
        "time": "Mar 1 16:35",
        "idle": ".",
        "pid": "15679",
        "from": "192.168.1.5"
      }
    ]

<a id="jc.parsers.who.parse"></a>

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

Source: [`jc/parsers/who.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/who.py)

Version 1.9 by Kelly Brazil (kellyjonbrazil@gmail.com)
