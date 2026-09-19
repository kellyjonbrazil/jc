r"""jc - JSON Convert `ls` and `vdir` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Requires the `-l` option to be used on `ls`. If there are newline characters
in the filename, then make sure to use the `-b` option on `ls`.

Options supported:
- `--time-style=full-iso`
- `--time-style=long-iso`

Block (`b`) and character (`c`) device entries report `major_number` and
`minor_number` instead of `size`, since `ls` prints the device's major and
minor numbers in that column rather than a byte count.

`--time-style=iso` is not supported since its date field is a different
width depending on how old each file is, which this parser cannot detect
reliably. Use `--time-style=long-iso` or `--time-style=full-iso` instead.

The `jc` `-qq` option can be used to ignore parsing errors. (e.g. filenames
with newline characters, but `-b` was not used)

The `epoch` calculated timestamp field is naive (i.e. based on the local
time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the timezone field is UTC.

Usage (cli):

    $ ls | jc --ls-s

Usage (module):

    import jc

    result = jc.parse('ls_s', ls_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "filename":       string,
      "flags":          string,
      "links":          integer,
      "parent":         string,
      "owner":          string,
      "group":          string,
      "size":           integer,
      "major_number":   integer,     # [0]
      "minor_number":   integer,     # [0]
      "date":           string,
      "epoch":          integer,     # [1]
      "epoch_utc":      integer,     # [2]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] only exists for block (b) and character (c) device entries,
        in place of size.
    [1] naive timestamp if date field exists and can be converted.
    [2] timezone aware timestamp if date field is in UTC and can
        be converted

Examples:

    $ ls -l /usr/bin | jc --ls-s
    {"filename":"2to3-","flags":"-rwxr-xr-x","links":4,"owner":"root","...}
    {"filename":"2to3-2.7","link_to":"../../System/Library/Frameworks/P...}
    {"filename":"AssetCacheLocatorUtil","flags":"-rwxr-xr-x","links":1,...}
    ...

    $ ls -l /usr/bin | jc --ls-s -r
    {"filename":"2to3-","flags":"-rwxr-xr-x","links":"4","owner":"roo"..."}
    {"filename":"2to3-2.7","link_to":"../../System/Library/Frameworks/P...}
    {"filename":"AssetCacheLocatorUtil","flags":"-rwxr-xr-x","links":"1...}
    ...

    $ ls -l /dev | jc --ls-s
    {"filename":"null","flags":"crw-rw-rw-","links":1,"owner":"root","g...}
    ...
"""
import re
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError

_PERM_RE = re.compile(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?')
_LONG_ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
_LONG_ISO_TIME_RE = re.compile(r'^\d{2}:\d{2}$')


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`ls` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    tags = ['command']
    streaming = True


__version__ = info.version


def _detect_date_width(sample_line):
    """
    Return the number of whitespace-separated tokens that make up the
    date field: 2 for --time-style=long-iso ("2024-08-15 10:53"), 3 for
    the default and --time-style=full-iso formats. `sample_line` must be
    a data line that matches _PERM_RE.
    """
    device = sample_line[0] in ('b', 'c')
    tokens = sample_line.split()
    start = 6 if device else 5

    if len(tokens) > start + 1 \
       and _LONG_ISO_DATE_RE.match(tokens[start]) \
       and _LONG_ISO_TIME_RE.match(tokens[start + 1]):
        return 2

    return 3


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = {'links', 'size', 'major_number', 'minor_number'}

    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

    if 'date' in proc_data:
        # to speed up processing only try to convert the date if it's not the default format
        if not re.match(r'[a-zA-Z]{3}\s{1,2}\d{1,2}\s{1,2}[0-9:]{4,5}', proc_data['date']):
            ts = jc.utils.timestamp(proc_data['date'], format_hint=(7200,))
            proc_data['epoch'] = ts.naive
            proc_data['epoch_utc'] = ts.utc

    return proc_data


@add_jc_meta
def parse(data, raw=False, quiet=False, ignore_exceptions=False):
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    parent = ''
    date_width = None

    for line in data:
        try:
            streaming_line_input_type_check(line)

            # skip line if it starts with 'total 1234'
            if re.match(r'total [0-9]+', line):
                continue

            # skip blank lines
            if not line.strip():
                continue

            # Look for parent line if glob or -R is used
            if not _PERM_RE.match(line) \
                and line.strip().endswith(':'):
                parent = line.strip()[:-1]
                continue

            if not _PERM_RE.match(line):
                raise ParseError('Not ls -l data')

            # block (b) and character (c) device entries report
            # major,minor instead of a size, which takes one extra
            # whitespace-separated token
            device = line[0] in ('b', 'c')
            size_width = 2 if device else 1

            # date field width is consistent for the whole `ls` invocation,
            # so it only needs to be detected once per stream
            if date_width is None:
                date_width = _detect_date_width(line.strip())

            fixed_width = 4 + size_width + date_width
            parsed_line = line.strip().split(maxsplit=fixed_width)
            output_line = {}

            # split filenames and links
            if len(parsed_line) == fixed_width + 1:
                filename_field = parsed_line[fixed_width].split(' -> ')
            else:
                # in case of filenames starting with a newline character
                filename_field = ['']

            # create output object
            output_line['filename'] = filename_field[0]

            if len(filename_field) > 1:
                output_line['link_to'] = filename_field[1]

            if parent:
                output_line['parent'] = parent

            output_line['flags'] = parsed_line[0]
            output_line['links'] = parsed_line[1]
            output_line['owner'] = parsed_line[2]
            output_line['group'] = parsed_line[3]

            if device:
                output_line['major_number'] = parsed_line[4].rstrip(',')
                output_line['minor_number'] = parsed_line[5]
            else:
                output_line['size'] = parsed_line[4]

            date_start = 4 + size_width
            output_line['date'] = ' '.join(parsed_line[date_start:date_start + date_width])

            yield output_line if raw else _process(output_line)

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
