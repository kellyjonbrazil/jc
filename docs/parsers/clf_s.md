[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.clf_s"></a>

# jc.parsers.clf_s

jc - JSON Convert Common Log Format file streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

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

    $ cat file.log | jc --clf-s

Usage (module):

    import jc

    result = jc.parse('clf_s', common_log_file_output.splitlines())
    for item in result:
        # do something

Schema:

    Empty strings and `-` values are converted to `null`/`None`.

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

    [0] naive timestamp
    [1] timezone-aware timestamp. Only available if timezone field is UTC
    [2] exists if the line was not able to be parsed

Examples:

    $ cat file.log | jc --clf-s
    {"host":"127.0.0.1","ident":"user-identifier","authuser":"frank","...}
    {"host":"1.1.1.2","ident":null,"authuser":null,"date":"11/Nov/2016...}
    ...

    $ cat file.log | jc --clf-s -r
    {"host":"127.0.0.1","ident":"user-identifier","authuser":"frank","...}
    {"host":"1.1.1.2","ident":"-","authuser":"-","date":"11/Nov/2016:0...}
    ...

<a id="jc.parsers.clf_s.parse"></a>

### parse

```python
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Iterator[Union[Dict[str, Any], Tuple[BaseException, str]]]
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

Source: [`jc/parsers/clf_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/clf_s.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
