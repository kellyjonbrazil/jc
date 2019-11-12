# jc.parsers.history
jc - JSON CLI output utility history Parser

Usage:
    specify --history as the first argument if the piped input is coming from history

Examples:

    $ history | jc --history -p
    [
      {
        "line": "118",
        "command": "sleep 100"
      },
      {
        "line": "119",
        "command": "ls /bin"
      },
      {
        "line": "120",
        "command": "echo "hello""
      },
      {
        "line": "121",
        "command": "docker images"
      },
      ...
    ]

    $ history | jc --history -p -r
    {
      "118": "sleep 100",
      "119": "ls /bin",
      "120": "echo "hello"",
      "121": "docker images",
      ...
    }

## process
```python
process(proc_data)
```

schema:

    [
      {
        "line":     string,
        "command":  string
      }
    ]

## parse
```python
parse(data, raw=False, quiet=False)
```

Main parsing function

Arguments:

    raw:    (boolean) output preprocessed JSON if True
    quiet:  (boolean) suppress warning messages if True

