[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.file"></a>

# jc.parsers.file

jc - JSON Convert `file` command output parser

Usage (cli):

    $ file * | jc --file

or

    $ jc file *

Usage (module):

    import jc
    result = jc.parse('file', file_command_output)

Schema:

    [
      {
        "filename":   string,
        "type":       string
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
        "type": "XML 1.0 document text, ASCII text, with CRLF line ..."
      },
      {
        "filename": "centosserial.sh",
        "type": "Bourne-Again shell script text executable, UTF-8 ..."
      },
      ...
    ]

<a id="jc.parsers.file.parse"></a>

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
Compatibility:  linux, aix, freebsd, darwin

Source: [`jc/parsers/file.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/file.py)

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
