[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.asciitable"></a>

# jc.parsers.asciitable

jc - JSON Convert `asciitable` parser

This parser converts ASCII and Unicode text tables with single-line rows.

Column headers must be at least two spaces apart from each other and must
be unique. For best results, column headers should be left-justified. If
column separators are present, then non-left-justified headers will be fixed
automatically.

Row separators are optional and are ignored. Each non-row-separator line is
considered a separate row in the table.

For example:

    ╒══════════╤═════════╤════════╕
    │ foo      │ bar     │ baz    │
    ╞══════════╪═════════╪════════╡
    │ good day │         │ 12345  │
    ├──────────┼─────────┼────────┤
    │ hi there │ abc def │ 3.14   │
    ╘══════════╧═════════╧════════╛

or

    +-----------------------------+
    | foo        bar       baz    |
    +-----------------------------+
    | good day             12345  |
    | hi there   abc def   3.14   |
    +-----------------------------+

or

    | foo      | bar     | baz    |
    |----------|---------|--------|
    | good day |         | 12345  |
    | hi there | abc def | 3.14   |

or

    foo        bar       baz
    ---------  --------  ------
    good day             12345
    hi there   abc def   3.14

or

    foo        bar       baz
    good day             12345
    hi there   abc def   3.14

etc...

Headers (keys) are converted to snake-case. All values are returned as
strings, except empty strings, which are converted to None/null.

> Note: To preserve the case of the keys use the `-r` cli option or
> `raw=True` argument in `parse()`.

Usage (cli):

    $ cat table.txt | jc --asciitable

Usage (module):

    import jc
    result = jc.parse('asciitable', asciitable_string)

Schema:

    [
      {
        "column_name1":     string,    # empty string is null
        "column_name2":     string     # empty string is null
      }
    ]

Examples:

    $ echo '
    >     ╒══════════╤═════════╤════════╕
    >     │ foo      │ bar     │ baz    │
    >     ╞══════════╪═════════╪════════╡
    >     │ good day │         │ 12345  │
    >     ├──────────┼─────────┼────────┤
    >     │ hi there │ abc def │ 3.14   │
    >     ╘══════════╧═════════╧════════╛' | jc --asciitable -p
    [
      {
        "foo": "good day",
        "bar": null,
        "baz": "12345"
      },
      {
        "foo": "hi there",
        "bar": "abc def",
        "baz": "3.14"
      }
    ]

    $ echo '
    >     foo        bar       baz
    >     ---------  --------  ------
    >     good day             12345
    >     hi there   abc def   3.14'  | jc --asciitable -p
    [
      {
        "foo": "good day",
        "bar": null,
        "baz": "12345"
      },
      {
        "foo": "hi there",
        "bar": "abc def",
        "baz": "3.14"
      }
    ]

<a id="jc.parsers.asciitable.parse"></a>

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

Source: [`jc/parsers/asciitable.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/asciitable.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
