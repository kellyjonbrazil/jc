[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.git_log"></a>

# jc.parsers.git\_log

jc - JSON Convert `git log` command output parser

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

    $ git log | jc --git-log

    or

    $ jc git log

Usage (module):

    import jc
    result = jc.parse('git_log', git_log_command_output)

Schema:

    [
      {
        "commit":               string,
        "author":               string,
        "author_email":         string,
        "date":                 string,
        "epoch":                integer,
        "epoch_utc":            integer,
        "commit_by":            string,
        "commit_by_email":      string,
        "commit_by_date":       string,
        "message":              string,
        "stats" : {
          "files_changed":      integer,
          "insertions":         integer,
          "deletions":          integer,
          "files": [
                                string
          ]
        }
      }
    ]

Examples:

    $ git-log | jc --git-log -p
    []

    $ git-log | jc --git-log -p -r
    []

<a id="jc.parsers.git_log.parse"></a>

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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
