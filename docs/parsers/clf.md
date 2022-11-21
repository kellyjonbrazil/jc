[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.clf"></a>

# jc.parsers.clf

jc - JSON Convert Common Log Format file parser

This parser will handle the Common Log Format standard as specified at
https://www.w3.org/Daemon/User/Config/Logging.html#common-logfile-format.

Combined Log Format is also supported. (Referer and User Agent fields added)

Extra fields may be present and will be enclosed in the `extra` field as
a single string.

If a log line cannot be parsed, an object with an `unparsable` field will
be present with a value of the original line.

The `epoch` calculated timestamp field is naive. (i.e. based on the
local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is
only available if the timezone field is UTC.

Usage (cli):

    $ cat file.log | jc --clf

Usage (module):

    import jc
    result = jc.parse('clf', common_log_file_output)

Schema:

Empty strings and `-` values are converted to `null`/`None`.

    [
      {
        "host":                         string,
        "ident":                        string,
        "authuser":                     string,
        "date":                         string,
        "day":                          integer,
        "month":                        string,
        "year":                         integer,
        "hour":                         integer,
        "minute":                       integer,
        "second":                       integer,
        "tz":                           string,
        "request":                      string,
        "request_method":               string,
        "request_url":                  string,
        "request_version":              string,
        "status":                       integer,
        "bytes":                        integer,
        "referer":                      string,
        "user_agent":                   string,
        "extra":                        string,
        "epoch":                        integer,  # [0]
        "epoch_utc":                    integer,  # [1]
        "unparsable":                   string    # [2]
      }
    ]

    [0] naive timestamp
    [1] timezone-aware timestamp. Only available if timezone field is UTC
    [2] exists if the line was not able to be parsed

Examples:

    $ cat file.log | jc --clf -p
    []

    $ cat file.log | jc --clf -p -r
    []

<a id="jc.parsers.clf.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[JSONDictType]
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
