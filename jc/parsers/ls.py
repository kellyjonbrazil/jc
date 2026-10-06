r"""jc - JSON Convert `ls` and `vdir` command output parser

Options supported:
- `lbaR1`
- `--time-style=full-iso`
- `--time-style=long-iso`

Block (`b`) and character (`c`) device entries report `major_number` and
`minor_number` instead of `size`, since `ls` prints the device's major and
minor numbers in that column rather than a byte count.

`--time-style=iso` is not supported since its date field is a different
width depending on how old each file is, which this parser cannot detect
reliably. Use `--time-style=long-iso` or `--time-style=full-iso` instead.

> Note: The `-1`, `-l`, or `-b` option of `ls` should be used to correctly
> parse filenames that include newline characters. Since `ls` does not
> encode newlines in filenames when outputting to a pipe it will cause `jc`
> to see multiple files instead of a single file if `-1`, `-l`, or `-b` is
> not used. Alternatively, `vdir` can be used, which is the same as running
> `ls -lb`.

The `epoch` calculated timestamp field is naive. (i.e. based on the local
time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the timezone field is UTC.

Usage (cli):

    $ ls | jc --ls

or

    $ jc ls

Usage (module):

    import jc
    result = jc.parse('ls', ls_command_output)

Schema:

    [
      {
        "filename":     string,
        "flags":        string,
        "links":        integer,
        "parent":       string,
        "owner":        string,
        "group":        string,
        "size":         integer,
        "major_number": integer,     # [0]
        "minor_number": integer,     # [0]
        "date":         string,
        "epoch":        integer,     # [1]
        "epoch_utc":    integer      # [2]
      }
    ]

    [0] only exists for block (b) and character (c) device entries,
        in place of size.
    [1] naive timestamp if date field exists and can be converted.
    [2] timezone aware timestamp if date field is in UTC and can
        be converted.

Examples:

    $ ls /usr/bin | jc --ls -p
    [
      {
        "filename": "apropos"
      },
      {
        "filename": "arch"
      },
      ...
    ]

    $ ls -l /usr/bin | jc --ls -p
    [
      {
        "filename": "apropos",
        "link_to": "whatis",
        "flags": "lrwxrwxrwx.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 6,
        "date": "Aug 15 10:53"
      },
      {
        "filename": "ar",
        "flags": "-rwxr-xr-x.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 62744,
        "date": "Aug 8 16:14"
      },
      ...
    ]

    $ ls -l /usr/bin | jc --ls -p -r
    [
      {
        "filename": "apropos",
        "link_to": "whatis",
        "flags": "lrwxrwxrwx.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "6",
        "date": "Aug 15 10:53"
      },
      {
        "filename": "arch",
        "flags": "-rwxr-xr-x.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "33080",
        "date": "Aug 19 23:25"
      },
      ...
    ]

    $ ls -l /dev | jc --ls -p
    [
      {
        "filename": "null",
        "flags": "crw-rw-rw-",
        "links": 1,
        "owner": "root",
        "group": "root",
        "major_number": 1,
        "minor_number": 3,
        "date": "Sep 16 08:00"
      },
      ...
    ]
"""
import re
import jc.utils

_PERM_RE = re.compile(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?')
_LONG_ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
_LONG_ISO_TIME_RE = re.compile(r'^\d{2}:\d{2}$')


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.13'
    description = '`ls` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['ls', 'vdir']
    tags = ['command']


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

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    int_list = {'links', 'size', 'major_number', 'minor_number'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        if 'date' in entry:
            # to speed up processing only try to convert the date if it's not the default format
            if not re.match(r'[a-zA-Z]{3}\s{1,2}\d{1,2}\s{1,2}[0-9:]{4,5}', entry['date']):
                ts = jc.utils.timestamp(entry['date'], format_hint=(7200,))
                entry['epoch'] = ts.naive
                entry['epoch_utc'] = ts.utc

    return proc_data


def parse(data, raw=False, quiet=False):
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

    raw_output = []
    warned = False
    parent = ''
    next_is_parent = False
    new_section = False

    linedata = data.splitlines()

    if jc.utils.has_data(data):

        # Delete first line if it starts with 'total 1234'
        if re.match(r'total [0-9]+', linedata[0]):
            linedata.pop(0)

        # Look for parent line if glob or -R is used
        if not _PERM_RE.match(linedata[0]) \
           and linedata[0].endswith(':'):
            parent = linedata.pop(0)[:-1]
            # Pop following total line if it exists
            if re.match(r'total [0-9]+', linedata[0]):
                linedata.pop(0)

        # Check if -l was used to parse extra data
        if _PERM_RE.match(linedata[0]):
            # detect date field width once for the whole listing: 3 tokens
            # for the default and --time-style=full-iso formats, 2 for
            # --time-style=long-iso (see _detect_date_width)
            date_width = 3
            for candidate in linedata:
                if _PERM_RE.match(candidate):
                    date_width = _detect_date_width(candidate)
                    break

            for entry in linedata:
                output_line = {}

                if not _PERM_RE.match(entry) \
                   and entry.endswith(':'):
                    parent = entry[:-1]
                    new_section = True

                    # fixup to remove trailing \n in previous entry
                    raw_output[-1]['filename'] = raw_output[-1]['filename'][:-1]
                    continue

                if re.match(r'total [0-9]+', entry):
                    new_section = False
                    continue

                # fix for OSX - doesn't print 'total xx' line if empty directory
                if new_section and entry == '':
                    new_section = False
                    continue

                # fixup for filenames with newlines
                if not new_section \
                   and not _PERM_RE.match(entry):
                    raw_output[-1]['filename'] = raw_output[-1]['filename'] + '\n' + entry
                    continue

                # block (b) and character (c) device entries report
                # major,minor instead of a size, which takes one extra
                # whitespace-separated token
                device = entry[0] in ('b', 'c')
                size_width = 2 if device else 1
                fixed_width = 4 + size_width + date_width

                parsed_line = entry.split(maxsplit=fixed_width)

                # split filenames and links
                if len(parsed_line) == fixed_width + 1:
                    filename_field = parsed_line[fixed_width].split(' -> ')
                else:
                    # in case of filenames starting with a newline character
                    filename_field = ['']

                # create list of dictionaries
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
                raw_output.append(output_line)
        else:
            for entry in linedata:
                output_line = {}

                if entry == '':
                    next_is_parent = True
                    continue

                if next_is_parent and entry.endswith(':'):
                    parent = entry[:-1]
                    next_is_parent = False
                    continue

                if not quiet and next_is_parent and not entry.endswith(':') and not warned:
                    jc.utils.warning_message(['Newline characters detected. Filenames probably corrupted. Use ls -l or -b instead.'])
                    warned = True

                output_line['filename'] = entry

                if parent:
                    output_line['parent'] = parent

                raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
