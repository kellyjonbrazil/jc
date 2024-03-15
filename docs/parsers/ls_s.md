[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ls_s"></a>

# jc.parsers.ls_s

jc - JSON Convert `ls` and `vdir` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Requires the `-l` option to be used on `ls`. If there are newline characters
in the filename, then make sure to use the `-b` option on `ls`.

The `jc` `-qq` option can be used to ignore parsing errors. (e.g. filenames
with newline characters, but `-b` was not used)

The `epoch` calculated timestamp field is naive (i.e. based on the local
time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the timezone field is UTC.

Usage (cli):

    $ ls | jc --ls-s

Usage (module):

    import jc

    result = jc.parse('ls_s', ls_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "filename":       string,
      "flags":          string,
      "links":          integer,
      "parent":         string,
      "owner":          string,
      "group":          string,
      "size":           integer,
      "date":           string,
      "epoch":          integer,     # [0]
      "epoch_utc":      integer,     # [1]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] naive timestamp if date field exists and can be converted.
    [1] timezone aware timestamp if date field is in UTC and can
        be converted

Examples:

    $ ls -l /usr/bin | jc --ls-s
    {"filename":"2to3-","flags":"-rwxr-xr-x","links":4,"owner":"root","...}
    {"filename":"2to3-2.7","link_to":"../../System/Library/Frameworks/P...}
    {"filename":"AssetCacheLocatorUtil","flags":"-rwxr-xr-x","links":1,...}
    ...

    $ ls -l /usr/bin | jc --ls-s -r
    {"filename":"2to3-","flags":"-rwxr-xr-x","links":"4","owner":"roo"..."}
    {"filename":"2to3-2.7","link_to":"../../System/Library/Frameworks/P...}
    {"filename":"AssetCacheLocatorUtil","flags":"-rwxr-xr-x","links":"1...}
    ...

<a id="jc.parsers.ls_s.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False, ignore_exceptions=False)
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
Compatibility:  linux, darwin, cygwin, aix, freebsd

Source: [`jc/parsers/ls_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ls_s.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
