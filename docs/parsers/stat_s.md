[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.stat_s"></a>

# jc.parsers.stat_s

jc - JSON Convert `stat` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

The `xxx_epoch` calculated timestamp fields are naive. (i.e. based on the
local time of the system the parser is run on).

The `xxx_epoch_utc` calculated timestamp fields are timezone-aware and are
only available if the timezone field is UTC.

Usage (cli):

    $ stat * | jc --stat-s

Usage (module):

    import jc

    result = jc.parse('stat_s', stat_command_output.splitlines())
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

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":                boolean,   # false if error parsing
        "error":                  string,    # exists if "success" is false
        "line":                   string     # exists if "success" is false
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
Compatibility:  linux, darwin, freebsd

Source: [`jc/parsers/stat_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/stat_s.py)

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
