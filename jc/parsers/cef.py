"""jc - JSON Convert CEF string parser

This is a best-effort parser since there are so many variations to CEF
formatting from different vendors. If you require special handling for your
CEF input, you can copy this parser code to the `jc` pluggin directory for
your system and modify it to suit your needs.

This parser will accept a single CEF string or multiple CEF string lines.
Any text before "CEF" will be ignored. Syslog and CEF escaped characters
(`\\`, `\\"`, `\\]`, `\\|`, `\\n`, `\\r`) are unescaped. To preserve
escaping, use the `--raw` or `raw=True` option in the `parse()` function.

Usage (cli):

    $ echo 'CEF:0|Vendor|Product|3.2.0|1|SYSTEM|1|... | jc --cef

Usage (module):

    import jc
    result = jc.parse('cef', cef_string_output)

Schema:

    [
      {
        "cef":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ cef | jc --cef -p
    []

    $ cef | jc --cef -p -r
    []
"""
from typing import List, Dict
import re
import jc.utils
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'CEF string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the pycef library at https://github.com/DavidJBianco/pycef/releases/tag/v1.11-2'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']

__version__ = info.version


############################################################################
"""
The MIT License (MIT)

Copyright (c) 2016 DavidJBianco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def _pycef_parse(str_input):
    """
    Parse a string in CEF format and return a dict with the header values
    and the extension data.
    """

    # Create the empty dict we'll return later
    values = dict()

    # This regex separates the string into the CEF header and the extension
    # data.  Once we do this, it's easier to use other regexes to parse each
    # part.
    header_re = r'((CEF:\d+)([^=\\]+\|){,7})(.*)'

    res = re.search(header_re, str_input)

    if res:
        header = res.group(1)
        extension = res.group(4)

        # Split the header on the "|" char.  Uses a negative lookbehind
        # assertion to ensure we don't accidentally split on escaped chars,
        # though.
        spl = re.split(r'(?<!\\)\|', header)

        # If the input entry had any blanks in the required headers, that's wrong
        # and we should return.  Note we explicitly don't check the last item in the
        # split list becuase the header ends in a '|' which means the last item
        # will always be an empty string (it doesn't exist, but the delimiter does).
        if "" in spl[0:-1]:
            raise ParseError('Blank field(s) in CEF header. Is it valid CEF format?')

        # Since these values are set by their position in the header, it's
        # easy to know which is which.
        values["DeviceVendor"] = spl[1]
        values["DeviceProduct"] = spl[2]
        values["DeviceVersion"] = spl[3]
        values["DeviceEventClassID"] = spl[4]
        values["Name"] = spl[5]
        if len(spl) > 6:
            values["Severity"] = spl[6]

        # The first value is actually the CEF version, formatted like
        # "CEF:#".  Ignore anything before that (like a date from a syslog message).
        # We then split on the colon and use the second value as the
        # version number.
        cef_start = spl[0].find('CEF')
        if cef_start == -1:
            raise ParseError('Invalid CEF string.')
        (cef, version) = spl[0][cef_start:].split(':')
        values["CEFVersion"] = version

        # The ugly, gnarly regex here finds a single key=value pair,
        # taking into account multiple whitespaces, escaped '=' and '|'
        # chars.  It returns an iterator of tuples.
        spl = re.findall(r'([^=\s]+)=((?:[\\]=|[^=])+)(?:\s|$)', extension)

        for i in spl:
            # Split the tuples and put them into the dictionary
            values[i[0]] = i[1]

        # Process custom field labels
        for key in list(values.keys()):
            # If the key string ends with Label, replace it in the appropriate
            # custom field
            if key[-5:] == "Label":
                customlabel = key[:-5]
                # Find the corresponding customfield and replace with the label
                for customfield in list(values.keys()):
                    if customfield == customlabel:
                        values[values[key]] = values[customfield]
                        del values[customfield]
                        del values[key]
    else:
        raise ParseError('Could not parse record. Is it valid CEF format?')

    return values

############################################################################


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    # fix escape chars specified in syslog RFC 5424 and CEF spec
    # https://www.rfc-editor.org/rfc/rfc5424.html#section-6
    # https://www.microfocus.com/documentation/arcsight/arcsight-smartconnectors-8.3/cef-implementation-standard/Content/CEF/Chapter%201%20What%20is%20CEF.htm?tocpath=_____2#_Toc494359738
    escape_map = {
        r'\\': '\\',
        r'\"': '"',
        r'\]': ']',
        r'\|': '|',
        r'\=': '=',
        r'\%': '%',
        r'\#': '#',
        r'\n': '\n',
        r'\r': '\r'
    }

    for item in proc_data:
        for key, value in item.copy().items():
            # remove any spaces around values
            item[key] = value.strip()

            # fixup escaped characters
            for esc, esc_sub in escape_map.items():
                item[key] = item[key].replace(esc, esc_sub)

            # remove any quotation marks from key names
            if '"' in key:
                new_key = key.replace('"', '')
                item[new_key] = item.pop(key)

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List = []

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            raw_output.append(_pycef_parse(line))

    return raw_output if raw else _process(raw_output)