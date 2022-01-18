[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.finger
jc - JSON CLI output utility `finger` command output parser

Supports `-s` output option. Does not support the `-l` detail option.

Usage (cli):

    $ finger | jc --finger

    or

    $ jc finger

Usage (module):

    import jc
    result = jc.parse('finger', finger_command_output)

    or

    import jc.parsers.finger
    result = jc.parsers.finger.parse(finger_command_output)

Schema:

    [
      {
        "login":                string,
        "name":                 string,
        "tty":                  string,
        "idle":                 string,     # null if empty
        "login_time":           string,
        "details":              string,
        "tty_writeable":        boolean,
        "idle_minutes":         integer,
        "idle_hours":           integer,
        "idle_days":            integer,
        "total_idle_minutes":   integer
      }
    ]

Examples:

    $ finger | jc --finger -p
    [
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "tty1",
        "idle": "14d",
        "login_time": "Mar 22 21:14",
        "tty_writeable": false,
        "idle_minutes": 0,
        "idle_hours": 0,
        "idle_days": 14,
        "total_idle_minutes": 20160
      },
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "pts/0",
        "idle": null,
        "login_time": "Apr  5 15:33",
        "details": "(192.168.1.22)",
        "tty_writeable": true,
        "idle_minutes": 0,
        "idle_hours": 0,
        "idle_days": 0,
        "total_idle_minutes": 0
      },
      ...
    ]

    $ finger | jc --finger -p -r
    [
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "*tty1",
        "idle": "14d",
        "login_time": "Mar 22 21:14"
      },
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "pts/0",
        "idle": null,
        "login_time": "Apr  5 15:33",
        "details": "(192.168.1.22)"
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
Compatibility:  linux, darwin, cygwin, freebsd

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
