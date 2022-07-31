[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.plist"></a>

# jc.parsers.plist

jc - JSON Convert PLIST file parser

Converts binary and XML PLIST files.

Usage (cli):

    $ cat file.plist | jc --plist

Usage (module):

    import jc
    result = jc.parse('plist', plist_command_output)

Schema:

    [
      {
        "plist":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ plist | jc --plist -p
    []

    $ plist | jc --plist -p -r
    []

<a id="jc.parsers.plist.parse"></a>

### parse

```python
def parse(data: Union[str, bytes],
          raw: bool = False,
          quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
