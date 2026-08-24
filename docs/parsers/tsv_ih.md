[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.tsv_ih"></a>

# jc.parsers.tsv_ih

jc - JSON Convert `tsv` implicit header file parser

The `tsv` implicit header file parser is a clone of the `csv` implicit
header file parser that uses '\t' as the delimiter character. The file must
have no header, and the field names will be generated as "c0", "c1", etc.

Usage (cli):

    $ cat file.tsv | jc --tsv-ih

Usage (module):

    import jc
    result = jc.parse('tsv_ih', tsv_output)

Schema:

TSV file converted to a Dictionary:
https://docs.python.org/3/library/csv.html

    [
      {
        "c0":     string,
        "c1":     string
      }
    ]

Examples:

    $ cat homes.tsv
    142	160	28	10	5	3	60	0.28	3167
    175	180	18	8	4	1	12	0.43	4033
    129	132	13	6	3	1	41	0.33	1471
    ...

    $ cat homes.tsv | jc --tsv-ih -p
    [
      {
        "c0": "142",
        "c1": "160",
        "c2": "28",
        "c3": "10",
        "c4": "5",
        "c5": "3",
        "c6": "60",
        "c7": "0.28",
        "c8": "3167"
      },
      {
        "c0": "175",
        "c1": "180",
        "c2": "18",
        "c3": "8",
        "c4": "4",
        "c5": "1",
        "c6": "12",
        "c7": "0.43",
        "c8": "4033"
      },
      {
        "c0": "129",
        "c1": "132",
        "c2": "13",
        "c3": "6",
        "c4": "3",
        "c5": "1",
        "c6": "41",
        "c7": "0.33",
        "c8": "1471"
      },
      ...
    ]

<a id="jc.parsers.tsv_ih.parse"></a>

### parse

```python
def parse(data: Union[str, bytes],
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
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

Source: [`jc/parsers/tsv_ih.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/tsv_ih.py)

Version 1.0 by Gary Gurlaskie (https://github.com/garyg1)
