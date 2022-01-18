[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.stat_s
jc - JSON CLI output utility `stat` command output streaming parser

> This streaming parser outputs JSON Lines

The `xxx_epoch` calculated timestamp fields are naive (i.e. based on the local time of the system the parser is run on).

The `xxx_epoch_utc` calculated timestamp fields are timezone-aware and are only available if the timezone field is UTC.

Usage (cli):

    $ stat * | jc --stat-s

Usage (module):

    import jc
    result = jc.parse('stat_s', stat_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

    or

    import jc.parsers.stat_s
    result = jc.parsers.stat_s.parse(stat_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "file":                     string,
      "link_to"                   string,
      "size":                     integer,
      "blocks":                   integer,
      "io_blocks":                integer,
      "type":                     string,
      "device":                   string,
      "inode":                    integer,
      "links":                    integer,
      "access":                   string,
      "flags":                    string,
      "uid":                      integer,
      "user":                     string,
      "gid":                      integer,
      "group":                    string,
      "access_time":              string,    # - = null
      "access_time_epoch":        integer,   # naive timestamp
      "access_time_epoch_utc":    integer,   # timezone-aware timestamp
      "modify_time":              string,    # - = null
      "modify_time_epoch":        integer,   # naive timestamp
      "modify_time_epoch_utc":    integer,   # timezone-aware timestamp
      "change_time":              string,    # - = null
      "change_time_epoch":        integer,   # naive timestamp
      "change_time_epoch_utc":    integer,   # timezone-aware timestamp
      "birth_time":               string,    # - = null
      "birth_time_epoch":         integer,   # naive timestamp
      "birth_time_epoch_utc":     integer,   # timezone-aware timestamp
      "unix_device":              integer,
      "rdev":                     integer,
      "block_size":               integer,
      "unix_flags":               string,
      "_jc_meta":                            # This object only exists if using -qq or ignore_exceptions=True
        {
          "success":              boolean,   # true if successfully parsed, false if error
          "error":                string,    # exists if "success" is false
          "line":                 string     # exists if "success" is false
        }
    }

Examples:

    $ stat | jc --stat-s
    {"file":"(stdin)","unix_device":1027739696,"inode":1155,"flags":"crw--w----","links":1,"user":"kbrazil","group":"tty","rdev":268435456,"size":0,"access_time":"Jan  4 15:27:44 2022","modify_time":"Jan  4 15:27:44 2022","change_time":"Jan  4 15:27:44 2022","birth_time":"Dec 31 16:00:00 1969","block_size":131072,"blocks":0,"unix_flags":"0","access_time_epoch":1641338864,"access_time_epoch_utc":null,"modify_time_epoch":1641338864,"modify_time_epoch_utc":null,"change_time_epoch":1641338864,"change_time_epoch_utc":null,"birth_time_epoch":null,"birth_time_epoch_utc":null}

    $ stat | jc --stat-s -r
    {"file":"(stdin)","unix_device":"1027739696","inode":"1155","flags":"crw--w----","links":"1","user":"kbrazil","group":"tty","rdev":"268435456","size":"0","access_time":"Jan  4 15:28:08 2022","modify_time":"Jan  4 15:28:08 2022","change_time":"Jan  4 15:28:08 2022","birth_time":"Dec 31 16:00:00 1969","block_size":"131072","blocks":"0","unix_flags":"0"}


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False, ignore_exceptions=False)
```

Main text parsing generator function. Returns an iterator object.

Parameters:

    data:              (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
    raw:               (boolean)   output preprocessed JSON if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True

Yields:

    Dictionary. Raw or processed structured data.

Returns:

    Iterator object

## Parser Information
Compatibility:  linux, darwin, freebsd

Version 0.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
