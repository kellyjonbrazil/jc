r"""jc - JSON Convert `XML` file parser

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
"""
import jc.utils
from jc.exceptions import LibraryNotInstalled


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.10'
    description = 'XML file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the xmltodict library at https://github.com/martinblech/xmltodict'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


def _process(proc_data, has_data=False, xml_mod=None):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary representing an XML document.
    """
    if not xml_mod:
        raise LibraryNotInstalled('The xmltodict library is not installed.')

    proc_output = []

    if has_data:
        # standard output with @ prefix for attributes
        try:
            proc_output = xml_mod.parse(proc_data,
                                          dict_constructor=dict,
                                          process_comments=True)
        except (ValueError, TypeError):
            proc_output = xml_mod.parse(proc_data, dict_constructor=dict)

    return proc_output


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    xmltodict = None
    try:
        import xmltodict
    except Exception:
        raise LibraryNotInstalled('The xmltodict library is not installed.')

    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []
    has_data = False

    if jc.utils.has_data(data):
        has_data = True

    if raw and has_data:
        # modified output with _ prefix for attributes
        try:
            raw_output = xmltodict.parse(data,
                                         dict_constructor=dict,
                                         process_comments=True,
                                         attr_prefix='_')
        except (ValueError, TypeError):
            raw_output = xmltodict.parse(data,
                                         dict_constructor=dict,
                                         attr_prefix='_')

        return raw_output

    return _process(data, has_data, xml_mod=xmltodict)
