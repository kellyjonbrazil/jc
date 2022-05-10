[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.top"></a>

# jc.parsers.top

jc - JSON Convert `top -b` command output parser

<<Short top description and caveats>>

Usage (cli):

    $ top -b -n 3 | jc --top

    or

    $ jc top -b -n 3

Usage (module):

    import jc
    result = jc.parse('top', top_command_output)

Schema:

    [
      {
        "top":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ top | jc --top -p
    []

    $ top | jc --top -p -r
    []

<a id="jc.parsers.top.parse"></a>

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
Compatibility:  linux

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
