[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.syslog_bsd_s"></a>

# jc.parsers.syslog_bsd_s

jc - JSON Convert Syslog RFC 3164 string streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

This parser accepts a single syslog line string or multiple syslog lines
separated by newlines. A warning message to `STDERR` will be printed if an
unparsable line is found unless `--quiet` or `quiet=True` is used.

Usage (cli):

    $ echo '<34>Oct 11 22:14:15 mymachine su: su ro...' | jc --syslog-bsd-s

Usage (module):

    import jc

    result = jc.parse('syslog_bsd_s', syslog_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "priority":                   integer/null,
      "date":                       string,
      "hostname":                   string,
      "tag":                        string/null,
      "content":                    string,
      "unparsable":                 string,  # [0]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] this field exists if the syslog line is not parsable. The value
        is the original syslog line.

Examples:

    $ cat syslog.txt | jc --syslog-bsd-s -p
    {"priority":34,"date":"Oct 11 22:14:15","hostname":"mymachine","t...}
    {"priority":34,"date":"Oct 11 22:14:16","hostname":"mymachine","t...}
    ...

    $ cat syslog.txt | jc --syslog-bsd-s -p -r
    {"priority":"34","date":"Oct 11 22:14:15","hostname":"mymachine","...}
    {"priority":"34","date":"Oct 11 22:14:16","hostname":"mymachine","...}
    ...

<a id="jc.parsers.syslog_bsd_s.parse"></a>

### parse

```python
def parse(data: Iterable[str],
          raw: bool = False,
          quiet: bool = False,
          ignore_exceptions: bool = False) -> Union[Iterable[Dict], tuple]
```

Main text parsing generator function. Returns an iterable object.

Parameters:

    data:              (iterable)  line-based text data to parse
                                   (e.g. sys.stdin or str.splitlines())

    raw:               (boolean)   unprocessed output if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True


Returns:

    Iterable of Dictionaries

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/syslog_bsd_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/syslog_bsd_s.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
