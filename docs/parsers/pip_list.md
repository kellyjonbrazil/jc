
# jc.parsers.pip_list
jc - JSON CLI output utility pip-list Parser

Usage:

    specify --pip-list as the first argument if the piped input is coming from pip list

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ pip list | jc --pip-list -p
    [
      {
        "package": "ansible",
        "version": "2.8.5"
      },
      {
        "package": "antlr4-python3-runtime",
        "version": "4.7.2"
      },
      {
        "package": "asn1crypto",
        "version": "0.24.0"
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

    proc_data:   (dictionary) raw structured data to process

Returns:

    List of dictionaries. Structured data with the following schema:

    [
      {
        "package":     string,
        "version":     string,
        "location":    string
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

    List of dictionaries. Raw or processed structured data.

