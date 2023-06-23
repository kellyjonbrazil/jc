[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.find"></a>

# jc.parsers.find

jc - JSON Convert `find` command output parser

Usage (cli):

    $ find | jc --find

Usage (module):

    import jc
    result = jc.parse('find', find_command_output)

Schema:

    [
      {
        "path":     string,
        "node":     string,
        "error":    string
      }
    ]

Examples:

    $ find | jc --find -p
    [
        {
          "path": "./directory"
          "node": "filename"
        },
        {
          "path": "./anotherdirectory"
          "node": "anotherfile"
        },
        {
          "path":   null
          "node":   null
          "error":  "find: './inaccessible': Permission denied"
        }
        ...
    ]

    $ find | jc --find -p -r
    [
      "./templates/readme_template",
      "./templates/manpage_template",
      "./.github/workflows/pythonapp.yml",
      ...
    ]

<a id="jc.parsers.find.parse"></a>

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

    Dictionary of raw structured data or
    List of Dictionaries of processed structured data

### Parser Information
Compatibility:  linux

Version 1.0 by Solomon Leang (solomonleang@gmail.com)
