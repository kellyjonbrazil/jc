[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.syslog"></a>

# jc.parsers.syslog

jc - JSON Convert Syslog RFC 5424 string parser

<<Short syslog-5424 description and caveats>>

Usage (cli):

    $ syslogstring | jc --syslog

    or

    $ jc syslog-5424

Usage (module):

    import jc
    result = jc.parse('syslog', syslog_command_output)

Schema:

    [
      {
        "syslog-5424":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ syslog-5424 | jc --syslog-5424 -p
    []

    $ syslog-5424 | jc --syslog-5424 -p -r
    []

<a id="jc.parsers.syslog.parse"></a>

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
