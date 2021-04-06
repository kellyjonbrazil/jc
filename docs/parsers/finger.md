
# jc.parsers.finger
jc - JSON CLI output utility `finger` command output parser

<<Short finger description and caveats>>

Usage (cli):

    $ finger | jc --finger

    or

    $ jc finger

Usage (module):

    import jc.parsers.finger
    result = jc.parsers.finger.parse(finger_command_output)

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ finger | jc --finger -p
    [
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "*tty1",
        "idle": "13d",
        "login_time": "Mar 22 21:14"
      },
      {
        "login": "jdoe",
        "name": "John Doe",
        "tty": "pts/0",
        "idle": null,
        "login_time": "Apr  5 15:33",
        "details": "(192.168.1.22)"
      }
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
        "login": "kbrazil",
        "name": "Kelly Brazil",
        "tty": "*tty1",
        "idle": "13d",
        "login_time": "Mar 22 21:14"
      },
      {
        "login": "kbrazil",
        "name": "Kelly Brazil",
        "tty": "pts/0",
        "idle": null,
        "login_time": "Apr  5 15:33",
        "details": "(192.168.1.221)"
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

