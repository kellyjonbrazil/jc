[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.hashsum"></a>

# jc.parsers.hashsum

jc - JSON Convert `hash sum` command output parser

This parser works with the following hash calculation utilities:
- `md5`
- `md5sum`
- `shasum`
- `sha1sum`
- `sha224sum`
- `sha256sum`
- `sha384sum`
- `sha512sum`

Usage (cli):

    $ md5sum file.txt | jc --hashsum

or

    $ jc md5sum file.txt

Usage (module):

    import jc
    result = jc.parse('hashsum', md5sum_command_output)

Schema:

    [
      {
        "filename":     string,
        "hash":         string,
      }
    ]

Examples:

    $ md5sum * | jc --hashsum -p
    [
      {
        "filename": "devtoolset-3-gcc-4.9.2-6.el7.x86_64.rpm",
        "hash": "65fc958c1add637ec23c4b137aecf3d3"
      },
      {
        "filename": "digout",
        "hash": "5b9312ee5aff080927753c63a347707d"
      },
      {
        "filename": "dmidecode.out",
        "hash": "716fd11c2ac00db109281f7110b8fb9d"
      },
      {
        "filename": "file with spaces in the name",
        "hash": "d41d8cd98f00b204e9800998ecf8427e"
      },
      {
        "filename": "id-centos.out",
        "hash": "4295be239a14ad77ef3253103de976d2"
      },
      {
        "filename": "ifcfg.json",
        "hash": "01fda0d9ba9a75618b072e64ff512b43"
      },
      ...
    ]

<a id="jc.parsers.hashsum.parse"></a>

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

Source: [`jc/parsers/hashsum.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/hashsum.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
