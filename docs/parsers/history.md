# jc.parsers.history
jc - JSON CLI output utility history Parser

Usage:
    specify --history as the first argument if the piped input is coming from history

Compatibility:
    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

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

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    dictionary   structured data with the following schema:

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

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    dictionary   raw or processed structured data

