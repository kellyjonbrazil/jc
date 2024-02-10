[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.xml"></a>

# jc.parsers.xml

jc - JSON Convert `XML` file parser

This parser adds a `@` prefix to attributes by default. This can be changed
to a `_` prefix by using the `-r` (cli) or `raw=True` (module) option.

Text values for nodes will have the key-name of `#text`.

Usage (cli):

    $ cat foo.xml | jc --xml

Usage (module):

    import jc
    result = jc.parse('xml', xml_file_output)

Schema:

XML Document converted to a Dictionary. See https://github.com/martinblech/xmltodict
for details.

    {
      "key1":   string/object,
      "key2":   string/object
    }

Examples:

    $ cat cd_catalog.xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CATALOG>
      <CD>
        <TITLE>Empire Burlesque</TITLE>
        <ARTIST>Bob Dylan</ARTIST>
        <COUNTRY>USA</COUNTRY>
        <COMPANY>Columbia</COMPANY>
        <PRICE>10.90</PRICE>
        <YEAR>1985</YEAR>
      </CD>
      <CD>
        <TITLE>Hide your heart</TITLE>
        <ARTIST>Bonnie Tyler</ARTIST>
        <COUNTRY>UK</COUNTRY>
        <COMPANY>CBS Records</COMPANY>
        <PRICE>9.90</PRICE>
        <YEAR>1988</YEAR>
      </CD>
      ...

    $ cat cd_catalog.xml | jc --xml -p
    {
      "CATALOG": {
        "CD": [
          {
            "TITLE": "Empire Burlesque",
            "ARTIST": "Bob Dylan",
            "COUNTRY": "USA",
            "COMPANY": "Columbia",
            "PRICE": "10.90",
            "YEAR": "1985"
          },
          {
            "TITLE": "Hide your heart",
            "ARTIST": "Bonnie Tyler",
            "COUNTRY": "UK",
            "COMPANY": "CBS Records",
            "PRICE": "9.90",
            "YEAR": "1988"
          },
      ...
    }

<a id="jc.parsers.xml.parse"></a>

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

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/xml.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/xml.py)

Version 1.10 by Kelly Brazil (kellyjonbrazil@gmail.com)
