[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.csv_s"></a>

# jc.parsers.csv_s

jc - JSON Convert `csv` file streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

The `csv` streaming parser will attempt to automatically detect the
delimiter character. If the delimiter cannot be detected it will default
to comma. The first row of the file must be a header row.

> Note: The first 100 rows are read into memory to enable delimiter
> detection, then the rest of the rows are loaded lazily.

Usage (cli):

    $ cat file.csv | jc --csv-s

Usage (module):

    import jc

    result = jc.parse('csv_s', csv_output.splitlines())
    for item in result:
        # do something

Schema:

CSV file converted to a Dictionary:
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

    $ cat homes.csv
    "Sell", "List", "Living", "Rooms", "Beds", "Baths", "Age", "Acres"...
    142, 160, 28, 10, 5, 3,  60, 0.28,  3167
    175, 180, 18,  8, 4, 1,  12, 0.43,  4033
    129, 132, 13,  6, 3, 1,  41, 0.33,  1471
    ...

    $ cat homes.csv | jc --csv-s
    {"Sell":"142","List":"160","Living":"28","Rooms":"10","Beds":"5"...}
    {"Sell":"175","List":"180","Living":"18","Rooms":"8","Beds":"4"...}
    {"Sell":"129","List":"132","Living":"13","Rooms":"6","Beds":"3"...}
    ...

<a id="jc.parsers.csv_s.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False, ignore_exceptions=False)
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

Source: [`jc/parsers/csv_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/csv_s.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
