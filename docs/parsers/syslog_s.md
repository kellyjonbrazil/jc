[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.syslog_s"></a>

# jc.parsers.syslog_s

jc - JSON Convert Syslog RFC 5424 string streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

This parser accepts a single syslog line string or multiple syslog lines
separated by newlines. A warning message to `STDERR` will be printed if an
unparsable line is found unless `--quiet` or `quiet=True` is used.

The `timestamp_epoch` calculated timestamp field is naive. (i.e. based on
the local time of the system the parser is run on)

The `timestamp_epoch_utc` calculated timestamp field is timezone-aware and
is only available if the timezone field is UTC.

Usage (cli):

    $ echo <165>1 2003-08-24T05:14:15.000003-07:00 192.0... | jc --syslog-s

Usage (module):

    import jc

    result = jc.parse('syslog_s', syslog_command_output.splitlines())
    for item in result:
        # do something

Schema:

Blank values converted to `null`/`None`.

    {
      "priority":                   integer,
      "version":                    integer,
      "timestamp":                  string,
      "timestamp_epoch":            integer,  # [0]
      "timestamp_epoch_utc":        integer,  # [1]
      "hostname":                   string,
      "appname":                    string,
      "proc_id":                    integer,
      "msg_id":                     string,
      "structured_data": [
        {
          "identity":               string,
          "parameters": {
            "<key>":                string
          }
        }
      ],
      "message":                    string,
      "unparsable":                 string  # [2]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] naive timestamp if "timestamp" field is parsable, else null
    [1] timezone aware timestamp available for UTC, else null
    [2] this field exists if the syslog line is not parsable. The value
        is the original syslog line.

Examples:

    $ cat syslog.txt | jc --syslog-s -p
    {"priority":165,"version":1,"timestamp":"2003-08-24T05:14:15.000003-...}
    {"priority":165,"version":1,"timestamp":"2003-08-24T05:14:16.000003-...}
    ...

    $ cat syslog.txt | jc --syslog-s -p -r
    {"priority":"165","version":"1","timestamp":"2003-08-24T05:14:15.000...}
    {"priority":"165","version":"1","timestamp":"2003-08-24T05:15:15.000...}
    ...

<a id="jc.parsers.syslog_s.parse"></a>

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

Source: [`jc/parsers/syslog_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/syslog_s.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
