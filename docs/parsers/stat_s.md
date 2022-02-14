[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.stat_s"></a>

# jc.parsers.stat\_s

jc - JSON CLI output utility `stat` command output streaming parser

> This streaming parser outputs JSON Lines

The `xxx_epoch` calculated timestamp fields are naive. (i.e. based on the
local time of the system the parser is run on).

The `xxx_epoch_utc` calculated timestamp fields are timezone-aware and are
only available if the timezone field is UTC.

Usage (cli):

    $ stat * | jc --stat-s

Usage (module):

    import jc
    # result is an iterable object (generator)
    result = jc.parse('stat_s', stat_command_output.splitlines())
    for item in result:
        # do something

    or

    import jc.parsers.stat_s
    # result is an iterable object (generator)
    result = jc.parsers.stat_s.parse(stat_command_output.splitlines())
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

      # Below object only exists if using -qq or ignore_exceptions=True

      "_jc_meta":
        {
          "success":              boolean,   # false if error parsing
          "error":                string,    # exists if "success" is false
          "line":                 string     # exists if "success" is false
        }
    }

Examples:

    $ stat | jc --stat-s
    {"file":"(stdin)","unix_device":1027739696,"inode":1155,"flags":"cr...}

    $ stat | jc --stat-s -r
    {"file":"(stdin)","unix_device":"1027739696","inode":"1155","flag...}

<a id="jc.parsers.stat_s.parse"></a>

### parse

```python
@add_jc_meta
def parse(data, raw=False, quiet=False, ignore_exceptions=False)
```

Main text parsing generator function. Returns an iterator object.

Parameters:

    data:              (iterable)  line-based text data to parse
                                   (e.g. sys.stdin or str.splitlines())

    raw:               (boolean)   unprocessed output if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True

Yields:

    Dictionary. Raw or processed structured data.

Returns:

    Iterator object (generator)

### Parser Information
Compatibility:  linux, darwin, freebsd

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
