"""jc - JSON CLI output utility ASCII table parser

Supports common ASCII table formats

Usage (cli):

    $ virsh list --all | jc --ascii

    or

    $ jc ascii

Usage (module):

    import jc.parsers.ascii
    result = jc.parsers.ascii.parse(ascii_table_output)

Schema:

    [
      {
        "column1":     string,
        "column2":     boolean,
        "column3":     integer
      }
    ]
    
Examples:

    $ virsh domifaddr foo | jc --ascii
    [{"name":"vnet0","mac_address":"01:23:45:67:89:ab","protocol":"ipv4","address":"192.168.122.100/24"}]

"""
import jc.utils
import jc.parsers.universal
import re


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'ASCII table parser'
    author = 'Alexandru Barbur'
    author_email = 'alex@ctrlc.name'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['ascii']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool conversions and timestamps

    return proc_data


def _snake_case(value):
    """
    Convert a value to snake case
    
    Parameters:
    
        value:    (string) original value
        
    Returns:
    
        Snake cased value.
    """

    value = value.replace('-', '_')
    value = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', value)
    value = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', value)
    value = re.sub(r'\s+', r'_', value)
    return value.lower()


def _process_headers(line):
    """
    Detect and clean header values in the table header row
    
    Parameters:
    
        line:    (string) header row line data
        
    Returns:
    
        Line with cleaned header values.
    """

    # XXX: what about tables that only use a single space between columns?
    matches = list(re.finditer(r"\w+( \w+)*", line))
    for match in matches:
        original_header = match.group()

        # snake case the header and pad or trim it to match original length
        clean_header = _snake_case(original_header)
        clean_header.ljust(len(original_header))
        clean_header = clean_header[:len(original_header)]

        # replace the matched header with the cleaned version in the line
        line = line[:match.start()] + clean_header + line[match.end():]

    return line
    

def _header_or_data_row(line):
    """
    Filter lines of text for header or data rows
    
    Parameters:
    
        line:    (string) line of text
        
    Returns:
    
        True if the line contains headers or data
    """

    # ignore empty or blank lines
    if not line:
        return False

    # ignore separator lines (i.e. "----")
    if len(set(line)) <= 1:
        return False

    # must be a header or data line
    return True


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """

    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):
        cleandata = list(filter(_header_or_data_row, data.splitlines()))
        cleandata[0] = _process_headers(cleandata[0])

        raw_output = jc.parsers.universal.sparse_table_parse(cleandata)

    if raw:
        return raw_output

    else:
        return _process(raw_output)
