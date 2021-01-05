
# jc.parsers.last
jc - JSON CLI output utility `last` and `lastb` command output parser

Supports -w and -F options.

Usage (cli):

    $ last | jc --last

    or

    $ jc last

Usage (module):

    import jc.parsers.last
    result = jc.parsers.last.parse(last_command_output)

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

Examples:

    $ last | jc --last -p
    [
      {
        "user": "kbrazil",
        "tty": "ttys002",
        "hostname": null,
        "login": "Thu Feb 27 14:31",
        "logout": "still logged in"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Thu Feb 27 10:38",
        "logout": "10:38",
        "duration": "00:00"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Thu Feb 27 10:18",
        "logout": "10:18",
        "duration": "00:00"
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



## info
```python
info()
```


## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (List of Dictionaries) raw structured data to process

Returns:

    List of Dictionaries. Structured data with the following schema:

    [
      {
        "user":       string,
        "tty":        string,
        "hostname":   string,
        "login":      string,
        "logout":     string,
        "duration":   string
      }
    ]


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

