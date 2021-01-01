
# jc.parsers.hash
jc - JSON CLI output utility `hash` command output parser

Usage (cli):

    $ hash | jc --hash

Usage (module):

    import jc.parsers.hash
    result = jc.parsers.hash.parse(hash_command_output)

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ hash | jc --hash -p
    [
      {
        "hits": 2,
        "command": "/bin/cat"
      },
      {
        "hits": 1,
        "command": "/bin/ls"
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

    proc_data:   (dictionary) raw structured data to process

Returns:

    List of dictionaries. Structured data with the following schema:

    [
      {
        "command":       string,
        "hits":          integer
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

