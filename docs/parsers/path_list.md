[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.path_list"></a>

# jc.parsers.path_list

jc - JSON Convert POSIX path list string parser

Parse a colon-separated POSIX path list, commonly found in environment
variables.

Usage (cli):

    $ echo "/Users/admin/.docker/bin:/Users/admin/.asdf/shims" | jc --path-list

Usage (module):

    import jc
    result = jc.parse('path-list', path_string)

Schema:

    [
      {
        "path":                      string,
        "parent":                    string,
        "filename":                  string,
        "stem":                      string,
        "extension":                 string,
        "path_list": [
                                     string
        ],
      }
    ]

Examples:

    $ echo "/abc/def/gh.txt:/xyz/uvw/ab.app" | jc --path-list -p

    [
      {
        "path": "/abc/def/gh.txt",
        "parent": "/abc/def",
        "filename": "gh.txt",
        "stem": "gh",
        "extension": "txt",
        "path_list": [
          "/",
          "abc",
          "def",
          "gh.txt"
        ]
      },
      {
        "path": "/xyz/uvw/ab.app",
        "parent": "/xyz/uvw",
        "filename": "ab.app",
        "stem": "ab",
        "extension": "app",
        "path_list": [
          "/",
          "xyz",
          "uvw",
          "ab.app"
        ]
      }
    ]

<a id="jc.parsers.path_list.parse"></a>

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

    List of Dictionaries representing a Key/Value pair document.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/path_list.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/path_list.py)

This parser can be used with the `--slurp` command-line option.

Version 1.0 by Michael Nietzold (https://github.com/muescha)
