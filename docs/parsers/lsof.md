# jc.parsers.lsof
jc - JSON CLI output utility lsof Parser

Usage:
    specify --lsof as the first argument if the piped input is coming from lsof

Compatibility:
    'linux'

Examples:

    $ sudo lsof | jc --lsof -p
    [
      {
        "command": "systemd",
        "pid": 1,
        "tid": null,
        "user": "root",
        "fd": "cwd",
        "type": "DIR",
        "device": "253,0",
        "size_off": 224,
        "node": 64,
        "name": "/"
      },
      {
        "command": "systemd",
        "pid": 1,
        "tid": null,
        "user": "root",
        "fd": "rtd",
        "type": "DIR",
        "device": "253,0",
        "size_off": 224,
        "node": 64,
        "name": "/"
      },
      {
        "command": "systemd",
        "pid": 1,
        "tid": null,
        "user": "root",
        "fd": "txt",
        "type": "REG",
        "device": "253,0",
        "size_off": 1624520,
        "node": 50360451,
        "name": "/usr/lib/systemd/systemd"
      },
      ...
    ]

    $ sudo lsof | jc --lsof -p -r
    [
      {
        "command": "systemd",
        "pid": "1",
        "tid": null,
        "user": "root",
        "fd": "cwd",
        "type": "DIR",
        "device": "8,2",
        "size_off": "4096",
        "node": "2",
        "name": "/"
      },
      {
        "command": "systemd",
        "pid": "1",
        "tid": null,
        "user": "root",
        "fd": "rtd",
        "type": "DIR",
        "device": "8,2",
        "size_off": "4096",
        "node": "2",
        "name": "/"
      },
      {
        "command": "systemd",
        "pid": "1",
        "tid": null,
        "user": "root",
        "fd": "txt",
        "type": "REG",
        "device": "8,2",
        "size_off": "1595792",
        "node": "668802",
        "name": "/lib/systemd/systemd"
      },
      ...
    ]

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    dictionary   structured data with the following schema:

    [
      {
        "command":    string,
        "pid":        integer,
        "tid":        integer,
        "user":       string,
        "fd":         string,
        "type":       string,
        "device":     string,
        "size_off":   integer,
        "node":       integer,
        "name":       string
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

    dictionary   raw or processed structured data

