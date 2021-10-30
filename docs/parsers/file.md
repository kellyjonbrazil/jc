[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.file
jc - JSON CLI output utility `file` command output parser

Usage (cli):

    $ file * | jc --file

    or

    $ jc file *

Usage (module):

    import jc.parsers.file
    result = jc.parsers.file.parse(file_command_output)

Schema:

    [
      {
        "filename":   string,
        "type   ":    string
      }
    ]

Examples:

    $ file * | jc --file -p
    [
      {
        "filename": "Applications",
        "type": "directory"
      },
      {
        "filename": "another file with spaces",
        "type": "empty"
      },
      {
        "filename": "argstest.py",
        "type": "Python script text executable, ASCII text"
      },
      {
        "filename": "blkid-p.out",
        "type": "ASCII text"
      },
      {
        "filename": "blkid-pi.out",
        "type": "ASCII text, with very long lines"
      },
      {
        "filename": "cd_catalog.xml",
        "type": "XML 1.0 document text, ASCII text, with CRLF line terminators"
      },
      {
        "filename": "centosserial.sh",
        "type": "Bourne-Again shell script text executable, UTF-8 Unicode text"
      },
      ...
    ]


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux, aix, freebsd, darwin

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
