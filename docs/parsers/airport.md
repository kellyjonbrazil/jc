# jc.parsers.airport
jc - JSON CLI output utility airport Parser

Usage:

    specify --airport as the first argument if the piped input is coming from airport

Compatibility:

    'darwin'

Examples:

    $ airport | jc --airport -p
    {

    }

    $ airport | jc --airport -p -r
    {

    }

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

    Dictionary. Structured data with the following schema:

    {

    }

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

    Dictionary. Raw or processed structured data.

