[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.lsof"></a>

# jc.parsers.lsof

jc - JSON Convert `lsof` command output parser

Usage (cli):

    $ lsof | jc --lsof

or

    $ jc lsof

Usage (module):

    import jc
    result = jc.parse('lsof', lsof_command_output)

Schema:

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

<a id="jc.parsers.lsof.parse"></a>

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

Source: [`jc/parsers/lsof.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/lsof.py)

Version 1.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
