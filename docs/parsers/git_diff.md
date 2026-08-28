[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.git_diff"></a>

# jc.parsers.git_diff

jc - JSON Convert `git diff --name-status` command output parser

Only the `--name-status` output format is currently supported.

Usage (cli):

    $ git diff --name-status | jc --git-diff

or

    $ jc git diff --name-status

Usage (module):

    import jc
    result = jc.parse('git_diff', git_diff_command_output)

Schema:

    [
      {
        "status":       string,        # A, M, D, R, C, T, U, or X
        "similarity":   integer/null,  # [0]
        "old_path":     string/null,   # [0]
        "path":         string
      }
    ]

    [0] only available for renamed (`R`) and copied (`C`) entries

Examples:

    $ git diff --name-status | jc --git-diff -p
    [
      {
        "status": "M",
        "similarity": null,
        "old_path": null,
        "path": "bootstrap/bootstrap.sh"
      },
      {
        "status": "D",
        "similarity": null,
        "old_path": null,
        "path": "configs/sample.json"
      },
      {
        "status": "A",
        "similarity": null,
        "old_path": null,
        "path": "scripts/status.py"
      },
      {
        "status": "R",
        "similarity": 100,
        "old_path": "README.md",
        "path": "README_now.md"
      }
    ]

    $ git diff --name-status | jc --git-diff -p -r
    [
      {
        "status": "R100",
        "similarity": null,
        "old_path": "README.md",
        "path": "README_now.md"
      }
    ]

<a id="jc.parsers.git_diff.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
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

Source: [`jc/parsers/git_diff.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/git_diff.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
