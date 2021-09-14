[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.ping_s
jc - JSON CLI output utility `ping` command output streaming parser

Usage (cli):

    $ ping | jc --ping_s

Usage (module):

    import jc.parsers.ping_s
    result = jc.parsers.ping_s.parse(ping_command_output)    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "ping":            string,
      "_meta":                       # This object only exists if using -q or quiet=True
        {
          "success":    booean,      # true if successfully parsed, false if error
          "error_msg":  string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ ping | jc --ping-s
    {example output}
    ...

    $ ping | jc --ping-s -r
    {example output}
    ...


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing generator function. Produces an iterable object.

Parameters:

    data:        (string)  line-based text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages and ignore parsing errors if True

Yields:

    Dictionary. Raw or processed structured data.

## Parser Information
Compatibility:  linux, darwin, cygwin, aix, freebsd

Version 0.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
