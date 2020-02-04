# jc.parsers.yaml
jc - JSON CLI output utility YAML Parser

Usage:

    specify --yaml as the first argument if the piped input is coming from a YAML file

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ cat example.yaml | jc --yaml -p
    [
        {
            "Description": "This is a YAML document",
            "Number": 42
        },
        {
            "Description": "Yet Another YAML document"
            "Boolean": true
        }
    ]

## info
```python
info(self, /, *args, **kwargs)
```

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    List of dictionaries. Each dictionary represents a YAML document:

    [
      {
        YAML Document converted to a Dictionary
        See https://pypi.org/project/ruamel.yaml for details
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

