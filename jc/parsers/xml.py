"""jc - JSON CLI output utility `XML` file parser

Usage (cli):

    $ cat foo.xml | jc --xml

Usage (module):

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
"""
import sys
import jc.utils
# check if xml library is installed and fail gracefully if it is not
try:
    import xmltodict
except Exception:
    jc.utils.error_message('The xmltodict library is not installed.')
    sys.exit(1)


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.4'
    description = 'XML file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the xmltodict library at https://github.com/martinblech/xmltodict'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary representing an XML document.
    """

    # No further processing
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        raw_output = xmltodict.parse(data)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
