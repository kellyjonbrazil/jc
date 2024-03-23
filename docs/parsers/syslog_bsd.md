[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.syslog_bsd"></a>

# jc.parsers.syslog_bsd

jc - JSON Convert Syslog RFC 3164 string parser

This parser accepts a single syslog line string or multiple syslog lines
separated by newlines. A warning message to `STDERR` will be printed if an
unparsable line is found unless `--quiet` or `quiet=True` is used.

Usage (cli):

    $ echo '<34>Oct 11 22:14:15 mymachine su: su root...' | jc --syslog-bsd

Usage (module):

    import jc
    result = jc.parse('syslog_bsd', syslog_command_output)

Schema:

    [
      {
        "priority":                   integer/null,
        "date":                       string,
        "hostname":                   string,
        "tag":                        string/null,
        "content":                    string,
        "unparsable":                 string,  # [0]
      }
    ]

    [0] this field exists if the syslog line is not parsable. The value
        is the original syslog line.

Examples:

    $ cat syslog.txt | jc --syslog-bsd -p
    [
      {
        "priority": 34,
        "date": "Oct 11 22:14:15",
        "hostname": "mymachine",
        "tag": "su",
        "content": "'su root' failed for lonvick on /dev/pts/8"
      }
    ]

    $ cat syslog.txt | jc --syslog-bsd -p -r
    [
      {
        "priority": "34",
        "date": "Oct 11 22:14:15",
        "hostname": "mymachine",
        "tag": "su",
        "content": "'su root' failed for lonvick on /dev/pts/8"
      }
    ]

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

Source: [`jc/parsers/syslog_bsd.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/syslog_bsd.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
