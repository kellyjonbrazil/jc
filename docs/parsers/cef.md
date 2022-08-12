[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.cef"></a>

# jc.parsers.cef

jc - JSON Convert CEF string parser

This is a best-effort parser since there are so many variations to CEF
formatting from different vendors. If you require special handling for your
CEF input, you can copy this parser code to the `jc` pluggin directory for
your system and modify it to suit your needs.

This parser will accept a single CEF string or multiple CEF string lines.
Any text before "CEF" will be ignored. Syslog and CEF escaped characters
(`\\`, `\\"`, `\\]`, `\\|`, `\\n`, `\\r`) are unescaped. To preserve
escaping, use the `--raw` or `raw=True` option in the `parse()` function.

Usage (cli):

    $ echo 'CEF:0|Vendor|Product|3.2.0|1|SYSTEM|1|... | jc --cef

Usage (module):

    import jc
    result = jc.parse('cef', cef_string_output)

Schema:

    [
      {
        "cef":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ cef | jc --cef -p
    []

    $ cef | jc --cef -p -r
    []

<a id="jc.parsers.cef.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
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
