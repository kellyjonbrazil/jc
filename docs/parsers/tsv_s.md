[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.tsv_s"></a>

# jc.parsers.tsv_s

jc - JSON Convert `TSV` file streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

The `tsv` streaming parser is a clone of the `csv` streaming parser that
uses '\t' as the delimiter character. The first row of the file must be a
header row.

> Note: The first 100 rows are read into memory for file analysis, then the
> rest of the rows are loaded lazily.

Usage (cli):

    $ cat file.tsv | jc --tsv-s

Usage (module):

    import jc
    result = jc.parse('tsv_s', tsv_output.splitlines())

Schema:

TSV file converted to a Dictionary:
https://docs.python.org/3/library/csv.html

    {
      "column_name1":     string,
      "column_name2":     string,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":        boolean,     # false if error parsing
        "error":          string,      # exists if "success" is false
        "line":           string       # exists if "success" is false
      }
    }

Examples:

    $ cat homes.tsv
    "Sell"	"List"	"Living"	"Rooms"	"Beds"	"Baths"	"Age"	"Acres"...
    142	160	28	10	5	3	60	0.28	3167
    175	180	18	8	4	1	12	0.43	4033
    129	132	13	6	3	1	41	0.33	1471
    ...

    $ cat homes.tsv | jc --tsv-s
    {"Sell":"142","List":"160","Living":"28","Rooms":"10","Beds":"5"...}
    {"Sell":"175","List":"180","Living":"18","Rooms":"8","Beds":"4"...}
    {"Sell":"129","List":"132","Living":"13","Rooms":"6","Beds":"3"...}

<a id="jc.parsers.tsv_s.parse"></a>

### parse

```python
def parse(data: Union[str, bytes],
          raw: bool = False,
          quiet: bool = False,
          ignore_exceptions: bool = False) -> List[Dict[str, Any]]
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

Source: [`jc/parsers/tsv_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/tsv_s.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
