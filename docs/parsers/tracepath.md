# jc.parsers.tracepath
jc - JSON CLI output utility tracepath Parser

Usage:

    specify --tracepath as the first argument if the piped input is coming from tracepath

Compatibility:

    'linux'

Examples:

    $ tracepath | jc --tracepath -p
    []

    $ tracepath | jc --tracepath -p -r
    []

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

    List of dictionaries. Structured data with the following schema:

    [
      {
        "tracepath":     string,
        "bar":     boolean,
        "baz":     integer
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

