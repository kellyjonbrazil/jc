[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.xml
jc - JSON CLI output utility `XML` file parser

Usage (cli):

    $ cat foo.xml | jc --xml

Usage (module):

    import jc
    result = jc.parse('xml', xml_file_output)

    or

    import jc.parsers.xml
    result = jc.parsers.xml.parse(xml_file_output)

Schema:

    XML Document converted to a Dictionary
    See https://github.com/martinblech/xmltodict for details

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

    Dictionary. Raw or processed structured data.

## Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
