[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.ls_s
jc - JSON CLI output utility `ls` and `vdir` command output streaming parser

This streaming parser requires the `-l` option to be used on `ls`. If there are newline characters in the filename, then make sure to use the `-b` option on `ls`.

The `jc` `-q` option can be used to ignore parsing errors. (e.g. filenames with newline characters, but `-b` was not used)

The `epoch` calculated timestamp field is naive (i.e. based on the local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only available if the timezone field is UTC.

Usage (cli):

    $ ls | jc --ls-s

Usage (module):

    import jc.parsers.ls_s
    result = jc.parsers.ls_s.parse(ls_command_output)    # result is an iterable object
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
      "epoch":          integer,     # naive timestamp if date field exists and can be converted
      "epoch_utc":      integer,     # timezone aware timestamp if date field is in UTC and can be converted
      "_meta":                       # This object only exists if using -q or quiet=True
        {
          "success":    booean,      # true if successfully parsed, false if error
          "error_msg":  string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ ls -l /usr/bin | jc --ls-s
    {"filename":"2to3-","flags":"-rwxr-xr-x","links":4,"owner":"root","group":"wheel","size":925,"date":"Feb 22 2019"}
    {"filename":"2to3-2.7","link_to":"../../System/Library/Frameworks/Python.framework/Versions/2.7/bin/2to3-2.7","flags":"lrwxr-xr-x","links":1,"owner":"root","group":"wheel","size":74,"date":"May 4 2019"}
    {"filename":"AssetCacheLocatorUtil","flags":"-rwxr-xr-x","links":1,"owner":"root","group":"wheel","size":55152,"date":"May 3 2019"}
    ...

    $ ls -l /usr/bin | jc --ls-s -r
    {"filename":"2to3-","flags":"-rwxr-xr-x","links":"4","owner":"root","group":"wheel","size":"925","date":"Feb 22 2019"}
    {"filename":"2to3-2.7","link_to":"../../System/Library/Frameworks/Python.framework/Versions/2.7/bin/2to3-2.7","flags":"lrwxr-xr-x","links":"1","owner":"root","group":"wheel","size":"74","date":"May 4 2019"}
    {"filename":"AssetCacheLocatorUtil","flags":"-rwxr-xr-x","links":"1","owner":"root","group":"wheel","size":"55152","date":"May 3 2019"}
    ...


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing generator function. Produces an iterable object.

Parameters:

    data:        (string)  line-based text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages and ignore parsing errors if True

Yields:

    Dictionary. Raw or processed structured data.

## Parser Information
Compatibility:  linux, darwin, cygwin, aix, freebsd

Version 0.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
