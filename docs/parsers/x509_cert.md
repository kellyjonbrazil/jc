[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.x509_cert"></a>

# jc.parsers.x509\_cert

jc - JSON Convert X.509 Certificate format file parser

This parser will convert DER and PEM encoded X.509 certificates.

Usage (cli):

    $ cat certificate.pem | jc --x509-cert

Usage (module):

    import jc
    result = jc.parse('x509_cert', x509_cert_file_output)

Schema:

    [
      {
        "x509_cert":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ cat certificate.pem | jc --x509-cert -p
    []

    $ cat certificate.der | jc --x509-cert -p -r
    []

<a id="jc.parsers.x509_cert.parse"></a>

### parse

```python
def parse(data: Union[str, bytes],
          raw: bool = False,
          quiet: bool = False) -> List[Dict]
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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
