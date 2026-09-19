[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ls"></a>

# jc.parsers.ls

jc - JSON Convert `ls` and `vdir` command output parser

Options supported:
- `lbaR1`
- `--time-style=full-iso`
- `--time-style=long-iso`

Block (`b`) and character (`c`) device entries report `major_number` and
`minor_number` instead of `size`, since `ls` prints the device's major and
minor numbers in that column rather than a byte count.

`--time-style=iso` is not supported since its date field is a different
width depending on how old each file is, which this parser cannot detect
reliably. Use `--time-style=long-iso` or `--time-style=full-iso` instead.

> Note: The `-1`, `-l`, or `-b` option of `ls` should be used to correctly
> parse filenames that include newline characters. Since `ls` does not
> encode newlines in filenames when outputting to a pipe it will cause `jc`
> to see multiple files instead of a single file if `-1`, `-l`, or `-b` is
> not used. Alternatively, `vdir` can be used, which is the same as running
> `ls -lb`.

The `epoch` calculated timestamp field is naive. (i.e. based on the local
time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the timezone field is UTC.

Usage (cli):

    $ ls | jc --ls

or

    $ jc ls

Usage (module):

    import jc
    result = jc.parse('ls', ls_command_output)

Schema:

    [
      {
        "filename":     string,
        "flags":        string,
        "links":        integer,
        "parent":       string,
        "owner":        string,
        "group":        string,
        "size":         integer,
        "major_number": integer,     # [0]
        "minor_number": integer,     # [0]
        "date":         string,
        "epoch":        integer,     # [1]
        "epoch_utc":    integer      # [2]
      }
    ]

    [0] only exists for block (b) and character (c) device entries,
        in place of size.
    [1] naive timestamp if date field exists and can be converted.
    [2] timezone aware timestamp if date field is in UTC and can
        be converted.

Examples:

    $ ls /usr/bin | jc --ls -p
    [
      {
        "filename": "apropos"
      },
      {
        "filename": "arch"
      },
      ...
    ]

    $ ls -l /usr/bin | jc --ls -p
    [
      {
        "filename": "apropos",
        "link_to": "whatis",
        "flags": "lrwxrwxrwx.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 6,
        "date": "Aug 15 10:53"
      },
      {
        "filename": "ar",
        "flags": "-rwxr-xr-x.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 62744,
        "date": "Aug 8 16:14"
      },
      ...
    ]

    $ ls -l /usr/bin | jc --ls -p -r
    [
      {
        "filename": "apropos",
        "link_to": "whatis",
        "flags": "lrwxrwxrwx.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "6",
        "date": "Aug 15 10:53"
      },
      {
        "filename": "arch",
        "flags": "-rwxr-xr-x.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "33080",
        "date": "Aug 19 23:25"
      },
      ...
    ]

    $ ls -l /dev | jc --ls -p
    [
      {
        "filename": "null",
        "flags": "crw-rw-rw-",
        "links": 1,
        "owner": "root",
        "group": "root",
        "major_number": 1,
        "minor_number": 3,
        "date": "Sep 16 08:00"
      },
      ...
    ]

<a id="jc.parsers.ls.parse"></a>

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
Compatibility:  linux, darwin, cygwin, aix, freebsd

Source: [`jc/parsers/ls.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ls.py)

Version 1.13 by Kelly Brazil (kellyjonbrazil@gmail.com)
