[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.csv_s
jc - JSON CLI output utility `csv` file streaming parser

The `csv` streaming parser will attempt to automatically detect the delimiter character. If the delimiter cannot be detected it will default to comma. The first row of the file must be a header row.

Note: The first 100 rows are read into memory to enable delimiter detection, then the rest of the rows are loaded lazily.

Usage (cli):

    $ cat file.csv | jc --csv-s

Usage (module):

    import jc.parsers.csv_s
    result = jc.parsers.csv_s.parse(csv_output)

Schema:

    csv file converted to a Dictionary: https://docs.python.org/3/library/csv.html

    {
      "column_name1":     string,
      "column_name2":     string
    }

Examples:

    $ cat homes.csv
    "Sell", "List", "Living", "Rooms", "Beds", "Baths", "Age", "Acres", "Taxes"
    142, 160, 28, 10, 5, 3,  60, 0.28,  3167
    175, 180, 18,  8, 4, 1,  12, 0.43,  4033
    129, 132, 13,  6, 3, 1,  41, 0.33,  1471
    ...

    $ cat homes.csv | jc --csv-s
    {"Sell":"142","List":"160","Living":"28","Rooms":"10","Beds":"5","Baths":"3","Age":"60","Acres":"0.28","Taxes":"3167"}
    {"Sell":"175","List":"180","Living":"18","Rooms":"8","Beds":"4","Baths":"1","Age":"12","Acres":"0.43","Taxes":"4033"}
    {"Sell":"129","List":"132","Living":"13","Rooms":"6","Beds":"3","Baths":"1","Age":"41","Acres":"0.33","Taxes":"1471"}
    ...


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False, ignore_exceptions=False)
```

Main text parsing generator function. Returns an iterator object.

Parameters:

    data:              (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
    raw:               (boolean)   output preprocessed JSON if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True

Yields:

    Dictionary. Raw or processed structured data.

Returns:

    Iterator object

## Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
