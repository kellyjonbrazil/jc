[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.asciitable_m"></a>

# jc.parsers.asciitable_m

jc - JSON Convert `asciitable-m` parser

This parser converts various styles of ASCII and Unicode text tables with
multi-line rows. Tables must have a header row and separator line between
rows.

For example:

    ╒══════════╤═════════╤════════╕
    │ foo      │ bar baz │ fiz    │
    │          │         │ buz    │
    ╞══════════╪═════════╪════════╡
    │ good day │ 12345   │        │
    │ mate     │         │        │
    ├──────────┼─────────┼────────┤
    │ hi there │ abc def │ 3.14   │
    │          │         │        │
    ╘══════════╧═════════╧════════╛

Cells with multiple lines within rows will be joined with a newline
character ('\\n').

Headers (keys) are converted to snake-case and newlines between multi-line
headers are joined with an underscore. All values are returned as strings,
except empty strings, which are converted to None/null.

> Note: To preserve the case of the keys use the `-r` cli option or
> `raw=True` argument in `parse()`.

> Note: table column separator characters (e.g. `|`) cannot be present
> inside the cell data. If detected, a warning message will be printed to
> `STDERR` and the line will be skipped. The warning message can be
> suppressed by using the `-q` command option or by setting `quiet=True` in
> `parse()`.

Usage (cli):

    $ cat table.txt | jc --asciitable-m

Usage (module):

    import jc
    result = jc.parse('asciitable_m', asciitable-string)

Schema:

    [
      {
        "column_name1":     string,    # empty string is null
        "column_name2":     string     # empty string is null
      }
    ]

Examples:

    $ echo '
    > +----------+---------+--------+
    > | foo      | bar     | baz    |
    > |          |         | buz    |
    > +==========+=========+========+
    > | good day | 12345   |        |
    > | mate     |         |        |
    > +----------+---------+--------+
    > | hi there | abc def | 3.14   |
    > |          |         |        |
    > +==========+=========+========+' | jc --asciitable-m -p
    [
      {
        "foo": "good day\\nmate",
        "bar": "12345",
        "baz_buz": null
      },
      {
        "foo": "hi there",
        "bar": "abc def",
        "baz_buz": "3.14"
      }
    ]

    $ echo '
    > ╒══════════╤═════════╤════════╕
    > │ foo      │ bar     │ baz    │
    > │          │         │ buz    │
    > ╞══════════╪═════════╪════════╡
    > │ good day │ 12345   │        │
    > │ mate     │         │        │
    > ├──────────┼─────────┼────────┤
    > │ hi there │ abc def │ 3.14   │
    > │          │         │        │
    > ╘══════════╧═════════╧════════╛' | jc --asciitable-m -p
    [
      {
        "foo": "good day\\nmate",
        "bar": "12345",
        "baz_buz": null
      },
      {
        "foo": "hi there",
        "bar": "abc def",
        "baz_buz": "3.14"
      }
    ]

<a id="jc.parsers.asciitable_m.parse"></a>

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

Source: [`jc/parsers/asciitable_m.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/asciitable_m.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
