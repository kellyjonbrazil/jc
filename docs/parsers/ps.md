[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ps"></a>

# jc.parsers.ps

jc - JSON Convert `ps` command output parser

`ps` options supported:
- `ef`
- `axu`

Usage (cli):

    $ ps | jc --ps

or

    $ jc ps

Usage (module):

    import jc
    result = jc.parse('ps', ps_command_output)

Schema:

    [
      {
        "uid":           string,
        "pid":           integer,
        "ppid":          integer,
        "c":             integer,
        "stime":         string,
        "tty":           string,    # ? or ?? = Null
        "tt":            string,    # ?? = Null
        "time":          string,
        "cmd":           string,
        "user":          string,
        "cpu_percent":   float,
        "mem_percent":   float,
        "vsz":           integer,
        "rss":           integer,
        "stat":          string,
        "start":         string,
        "command":       string
      }
    ]

Examples:

    $ ps -ef | jc --ps -p
    [
      {
        "uid": "root",
        "pid": 1,
        "ppid": 0,
        "c": 0,
        "stime": "Nov01",
        "tty": null,
        "time": "00:00:11",
        "cmd": "/usr/lib/systemd/systemd --switched-root --system --dese..."
      },
      {
        "uid": "root",
        "pid": 2,
        "ppid": 0,
        "c": 0,
        "stime": "Nov01",
        "tty": null,
        "time": "00:00:00",
        "cmd": "[kthreadd]"
      },
      {
        "uid": "root",
        "pid": 4,
        "ppid": 2,
        "c": 0,
        "stime": "Nov01",
        "tty": null,
        "time": "00:00:00",
        "cmd": "[kworker/0:0H]"
      },
      ...
    ]

    $ ps -ef | jc --ps -p -r
    [
      {
        "uid": "root",
        "pid": "1",
        "ppid": "0",
        "c": "0",
        "stime": "Nov01",
        "tty": "?",
        "time": "00:00:11",
        "cmd": "/usr/lib/systemd/systemd --switched-root --system --dese..."
      },
      {
        "uid": "root",
        "pid": "2",
        "ppid": "0",
        "c": "0",
        "stime": "Nov01",
        "tty": "?",
        "time": "00:00:00",
        "cmd": "[kthreadd]"
      },
      {
        "uid": "root",
        "pid": "4",
        "ppid": "2",
        "c": "0",
        "stime": "Nov01",
        "tty": "?",
        "time": "00:00:00",
        "cmd": "[kworker/0:0H]"
      },
      ...
    ]

    $ ps axu | jc --ps -p
    [
      {
        "user": "root",
        "pid": 1,
        "cpu_percent": 0.0,
        "mem_percent": 0.1,
        "vsz": 128072,
        "rss": 6784,
        "tty": null,
        "stat": "Ss",
        "start": "Nov09",
        "time": "0:08",
        "command": "/usr/lib/systemd/systemd --switched-root --system --..."
      },
      {
        "user": "root",
        "pid": 2,
        "cpu_percent": 0.0,
        "mem_percent": 0.0,
        "vsz": 0,
        "rss": 0,
        "tty": null,
        "stat": "S",
        "start": "Nov09",
        "time": "0:00",
        "command": "[kthreadd]"
      },
      {
        "user": "root",
        "pid": 4,
        "cpu_percent": 0.0,
        "mem_percent": 0.0,
        "vsz": 0,
        "rss": 0,
        "tty": null,
        "stat": "S<",
        "start": "Nov09",
        "time": "0:00",
        "command": "[kworker/0:0H]"
      },
      ...
    ]

    $ ps axu | jc --ps -p -r
    [
      {
        "user": "root",
        "pid": "1",
        "cpu_percent": "0.0",
        "mem_percent": "0.1",
        "vsz": "128072",
        "rss": "6784",
        "tty": "?",
        "stat": "Ss",
        "start": "Nov09",
        "time": "0:08",
        "command": "/usr/lib/systemd/systemd --switched-root --system --..."
      },
      {
        "user": "root",
        "pid": "2",
        "cpu_percent": "0.0",
        "mem_percent": "0.0",
        "vsz": "0",
        "rss": "0",
        "tty": "?",
        "stat": "S",
        "start": "Nov09",
        "time": "0:00",
        "command": "[kthreadd]"
      },
      {
        "user": "root",
        "pid": "4",
        "cpu_percent": "0.0",
        "mem_percent": "0.0",
        "vsz": "0",
        "rss": "0",
        "tty": "?",
        "stat": "S<",
        "start": "Nov09",
        "time": "0:00",
        "command": "[kworker/0:0H]"
      },
      ...
    ]

<a id="jc.parsers.ps.parse"></a>

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

Source: [`jc/parsers/ps.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ps.py)

Version 1.7 by Kelly Brazil (kellyjonbrazil@gmail.com)
