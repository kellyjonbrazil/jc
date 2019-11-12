# jc.parsers.ls
jc - JSON CLI output utility ls Parser

Usage:
    specify --ls as the first argument if the piped input is coming from ls

    ls options supported:
    - None
    - la
    - h   file sizes will be available in text form with -r but larger file sizes
          with human readable suffixes will be converted to Null in default view
          since the parser attempts to convert this field to an integer.

Examples:

    $ ls /usr/bin | jc --ls -p
    [
      {
        "filename": "apropos"
      },
      {
        "filename": "arch"
      },
      {
        "filename": "awk"
      },
      {
        "filename": "base64"
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
      {
        "filename": "arch",
        "flags": "-rwxr-xr-x.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 33080,
        "date": "Aug 19 23:25"
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
      {
        "filename": "awk",
        "link_to": "gawk",
        "flags": "lrwxrwxrwx.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "4",
        "date": "Aug 15 10:53"
      },
      {
        "filename": "base64",
        "flags": "-rwxr-xr-x.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "37360",
        "date": "Aug 19 23:25"
      },
      {
        "filename": "basename",
        "flags": "-rwxr-xr-x.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "29032",
        "date": "Aug 19 23:25"
      },
      {
        "filename": "bash",
        "flags": "-rwxr-xr-x.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "964600",
        "date": "Aug 8 05:06"
      },
      ...
    ]

    $ ls -l /usr/bin | jc --ls | jq '.[] | select(.size > 50000000)'
    {
      "filename": "emacs",
      "flags": "-r-xr-xr-x",
      "links": 1,
      "owner": "root",
      "group": "wheel",
      "size": 117164432,
      "date": "May 3 2019"
    }

## process
```python
process(proc_data)
```

schema:

    [
      {
        "filename": string,
        "flags":    string,
        "links":    integer,
        "owner":    string,
        "group":    string,
        "size":     integer,
        "date":     string
      }
    ]

## parse
```python
parse(data, raw=False, quiet=False)
```

Main parsing function

Arguments:

    raw:    (boolean) output preprocessed JSON if True
    quiet:  (boolean) suppress warning messages if True

