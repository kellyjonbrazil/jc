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

Entries that `ls` cannot stat (e.g. `-????????? ? ? ? ?  ? name`) report
`null` for `links`, `owner`, `group`, `size`, and `date`.

Only symbolic link (`l`) entries have a `link_to` field. The filename is
split at the first ` -> `, so a link whose name contains ` -> ` reports
the rest of its name as part of `link_to`.

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

    result = jc.parse('ls_s', ls_command_output.split('\n'))
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

_PERM_RE = re.compile(r'[-dclpsbDCMnP?](([-r][-w][-xsS]){2}([-r][-w][-xtT])|\?{9})[+]?')
# entries `ls` cannot stat print '?' for the permissions and every field
_NO_STAT_RE = re.compile(r'[-dclpsbDCMnP?]\?{9}')
_LONG_ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
_LONG_ISO_TIME_RE = re.compile(r'^\d{2}:\d{2}$')


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.4'
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
    a data line that matches _PERM_RE and not _NO_STAT_RE.
    """
    device = sample_line[0] in ('b', 'c')
    tokens = sample_line.split()
    start = 6 if device else 5

    if len(tokens) > start + 1 \
       and _LONG_ISO_DATE_RE.match(tokens[start]) \
       and _LONG_ISO_TIME_RE.match(tokens[start + 1]):
        return 2

    return 3


def _is_blank(line):
    return isinstance(line, str) and not line.strip()


def _split_entry(line, field_count):
    """
    Split an `ls -l` entry line into its first `field_count` fields,
    which are separated by runs of spaces, and the filename. `ls` prints
    exactly one space between the date and the filename, so the filename
    is the rest of the line after that space and keeps any leading or
    trailing whitespace. The filename is None if the line ends after the
    last field.
    """
    fields = []
    pos = 0
    length = len(line)

    while len(fields) < field_count:
        while pos < length and line[pos] in ' \t':
            pos += 1

        if pos == length:
            break

        start = pos
        while pos < length and line[pos] not in ' \t':
            pos += 1

        fields.append(line[start:pos])

    filename = line[pos + 1:] if pos < length else None
    return fields, filename


def _is_total(line):
    """Return True if the line is a 'total 1234' block count line."""
    return isinstance(line, str) and bool(re.match(r'total [0-9]+', line))


def _is_section_header(line, prev_line, next_line):
    """
    Return True if `line` is a directory header ("name:") printed for
    globs and -R. `ls` only prints a header as the first line or after a
    blank line. A header that looks like an entry line must also be
    followed by a 'total 1234' line, since an entry line for a filename
    ending in ':' can be followed by a blank line or the end of the
    output. `prev_line` and `next_line` are None at the start and end of
    the output.
    """
    if not line.endswith(':'):
        return False

    if prev_line is not None and not _is_blank(prev_line):
        return False

    if next_line is not None and _is_total(next_line):
        return True

    return not _PERM_RE.match(line)


def _with_neighbors(data):
    """
    Yield (prev_line, line, next_line) for each line in `data`, reading
    only one line ahead. `prev_line` and `next_line` are None at the
    start and end of the input.
    """
    prev_line = None
    line = None
    started = False

    for next_line in data:
        if started:
            yield prev_line, line, next_line
            prev_line = line
        line = next_line
        started = True

    if started:
        yield prev_line, line, None


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

    if proc_data.get('date') is not None:
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
                                       (e.g. sys.stdin or str.split('\\n'))

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
    new_section = True

    for prev_line, line, next_line in _with_neighbors(data):
        try:
            streaming_line_input_type_check(line)

            # remove only the line ending: filenames can start or end
            # with whitespace
            if line.endswith('\n'):
                line = line[:-1]
            if line.endswith('\r'):
                line = line[:-1]

            # skip blank lines
            if not line.strip():
                new_section = False
                continue

            # Look for parent line if glob or -R is used
            if _is_section_header(line, prev_line, next_line):
                parent = line[:-1]
                new_section = True
                continue

            # 'total 1234' is only printed as the first line or directly
            # after a parent line
            if new_section and _is_total(line):
                new_section = False
                continue

            new_section = False

            if not _PERM_RE.match(line):
                raise ParseError('Not ls -l data')

            # entries `ls` cannot stat have a single '?' in each field
            # and no link target
            no_stat = bool(_NO_STAT_RE.match(line))

            # block (b) and character (c) device entries report
            # major,minor instead of a size, which takes one extra
            # whitespace-separated token
            device = line[0] in ('b', 'c') and not no_stat
            size_width = 2 if device else 1

            # date field width is consistent for the whole `ls` invocation,
            # so it only needs to be detected once per stream
            if date_width is None and not no_stat:
                date_width = _detect_date_width(line)

            entry_date_width = 1 if no_stat else date_width
            fixed_width = 4 + size_width + entry_date_width
            parsed_line, filename = _split_entry(line, fixed_width)
            output_line = {}

            # split filenames and links
            if filename is None:
                # in case of filenames starting with a newline character
                filename_field = ['']
            elif line[0] == 'l' and not no_stat:
                # only symbolic links print ' -> target'. A link name that
                # contains ' -> ' is ambiguous, so split at the first one
                filename_field = filename.split(' -> ', 1)
            else:
                filename_field = [filename]

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
            output_line['date'] = ' '.join(parsed_line[date_start:date_start + entry_date_width])

            if no_stat:
                for key in ('links', 'owner', 'group', 'size', 'date'):
                    output_line[key] = None

            yield output_line if raw else _process(output_line)

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
