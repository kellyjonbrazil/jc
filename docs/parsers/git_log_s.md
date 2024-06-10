[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.git_log_s"></a>

# jc.parsers.git_log_s

jc - JSON Convert `git log` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Can be used with the following format options:
- `oneline`
- `short`
- `medium`
- `full`
- `fuller`

Additional options supported:
- `--stat`
- `--shortstat`

The `epoch` calculated timestamp field is naive. (i.e. based on the
local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is
only available if the timezone field is UTC.

Usage (cli):

    $ git log | jc --git-log-s

Usage (module):

    import jc

    result = jc.parse('git_log_s', git_log_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "commit":               string,
      "author":               string/null,
      "author_email":         string/null,
      "date":                 string,
      "epoch":                integer,  # [0]
      "epoch_utc":            integer,  # [1]
      "commit_by":            string/null,
      "commit_by_email":      string/null,
      "commit_by_date":       string,
      "message":              string,
      "stats" : {
        "files_changed":      integer,
        "insertions":         integer,
        "deletions":          integer,
        "files": [
                              string
        ],
        "file_stats": [
          {
            "name":           string,
            "lines_changed":  integer
          }
        ]
      }

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] naive timestamp if "date" field is parsable, else null
    [1] timezone aware timestamp available for UTC, else null

Examples:

    $ git log | jc --git-log-s
    {"commit":"a730ae18c8e81c5261db132df73cd74f272a0a26","author":"Kelly...}
    {"commit":"930bf439c06c48a952baec05a9896c8d92b7693e","author":"Kelly...}
    ...

<a id="jc.parsers.git_log_s.parse"></a>

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

Source: [`jc/parsers/git_log_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/git_log_s.py)

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
