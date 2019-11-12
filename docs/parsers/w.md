# jc.parsers.w
jc - JSON CLI output utility w Parser

Usage:
    specify --w as the first argument if the piped input is coming from w

Examples:

    $ w | jc --w -p
    [
      {
        "user": "root",
        "tty": "tty1",
        "from": null,
        "login_at": "07:49",
        "idle": "1:15m",
        "jcpu": "0.00s",
        "pcpu": "0.00s",
        "what": "-bash"
      },
      {
        "user": "root",
        "tty": "ttyS0",
        "from": null,
        "login_at": "06:24",
        "idle": "0.00s",
        "jcpu": "0.43s",
        "pcpu": "0.00s",
        "what": "w"
      },
      {
        "user": "root",
        "tty": "pts/0",
        "from": "192.168.71.1",
        "login_at": "06:29",
        "idle": "2:35m",
        "jcpu": "0.00s",
        "pcpu": "0.00s",
        "what": "-bash"
      }
    ]

    $ w | jc --w -p -r
    [
      {
        "user": "kbrazil",
        "tty": "tty1",
        "from": "-",
        "login_at": "07:49",
        "idle": "1:16m",
        "jcpu": "0.00s",
        "pcpu": "0.00s",
        "what": "-bash"
      },
      {
        "user": "kbrazil",
        "tty": "ttyS0",
        "from": "-",
        "login_at": "06:24",
        "idle": "2.00s",
        "jcpu": "0.46s",
        "pcpu": "0.00s",
        "what": "w"
      },
      {
        "user": "kbrazil",
        "tty": "pts/0",
        "from": "192.168.71.1",
        "login_at": "06:29",
        "idle": "2:36m",
        "jcpu": "0.00s",
        "pcpu": "0.00s",
        "what": "-bash"
      }
    ]

## process
```python
process(proc_data)
```

schema:

    [
      {
        "user":     string,     # '-'' = null
        "tty":      string,     # '-'' = null
        "from":     string,     # '-'' = null
        "login_at": string,     # '-'' = null
        "idle":     string,     # '-'' = null
        "jcpu":     string,
        "pcpu":     string,
        "what":     string      # '-'' = null
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

