[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.syslog_bsd"></a>

# jc.parsers.syslog\_bsd

jc - JSON Convert Syslog RFC 3164 string parser

<<Short syslog-3164 description and caveats>>

Usage (cli):

    $ syslogstring | jc --syslog-bsd

    or

    $ jc syslog-3164

Usage (module):

    import jc
    result = jc.parse('syslog_bsd', syslog_command_output)

Schema:

    [
      {
        "syslog-3164":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ syslog-3164 | jc --syslog-3164 -p
    []

    $ syslog-3164 | jc --syslog-3164 -p -r
    []

<a id="jc.parsers.syslog_bsd.parse"></a>

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
