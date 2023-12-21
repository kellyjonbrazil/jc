[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.last"></a>

# jc.parsers.last

jc - JSON Convert `last` and `lastb` command output parser

Supports `-w`, `-F`, and `-x` options.

Calculated epoch time fields are naive (i.e. based on the local time of the
system the parser is run on) since there is no timezone information in the
`last` command output.

Usage (cli):

    $ last | jc --last

or

    $ jc last

Usage (module):

    import jc
    result = jc.parse('last', last_command_output)

Schema:

    [
      {
        "user":             string,
        "tty":              string,
        "hostname":         string,
        "login":            string,
        "logout":           string,
        "duration":         string,
        "login_epoch":      integer,  # (naive) available w/last -F option
        "logout_epoch":     integer,  # (naive) available w/last -F option
        "duration_seconds": integer   # available w/last -F option
      }
    ]

Examples:

    $ last -F | jc --last -p
    [
      {
        "user": "kbrazil",
        "tty": "ttys002",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "still logged in"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "Mon Dec 28 17:25:01 2020",
        "duration": "00:00",
        "login_epoch": 1565891826,
        "logout_epoch": 1565895404,
        "duration_seconds": 3578
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "Mon Dec 28 17:25:01 2020",
        "duration": "00:00",
        "login_epoch": 1565891826,
        "logout_epoch": 1565895404,
        "duration_seconds": 3578
      },
      ...
    ]

    $ last | jc --last -p -r
    [
      {
        "user": "kbrazil",
        "tty": "ttys002",
        "hostname": "-",
        "login": "Thu Feb 27 14:31",
        "logout": "still_logged_in"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": "-",
        "login": "Thu Feb 27 10:38",
        "logout": "10:38",
        "duration": "00:00"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": "-",
        "login": "Thu Feb 27 10:18",
        "logout": "10:18",
        "duration": "00:00"
      },
      ...
    ]

<a id="jc.parsers.last.parse"></a>

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
Compatibility:  linux, darwin, aix, freebsd

Source: [`jc/parsers/last.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/last.py)

Version 1.9 by Kelly Brazil (kellyjonbrazil@gmail.com)
