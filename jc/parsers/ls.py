"""jc - JSON CLI output utility ls Parser

Note: The -l or -b option of ls should be used to correctly parse filenames that include newline characters.
      Since ls does not encode newlines in filenames when outputting to a pipe it will cause jc to see
      multiple files instead of a single file if -l or -b is not used.

Usage:

    specify --ls as the first argument if the piped input is coming from ls

    ls options supported:

                    -lbaR
    --time-style=full-iso
                       -h  file sizes will be available in text form with -r but larger file sizes
                               with human readable suffixes will be converted to Null in default view
                               since the parser attempts to convert this field to an integer.

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ ls /usr/bin | jc --ls -p
    [
      {
        "filename": "apropos"
      },
      {
        "filename": "arch"
      },
      {
        "filename": "awk"
      },
      {
        "filename": "base64"
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
      {
        "filename": "arch",
        "flags": "-rwxr-xr-x.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 33080,
        "date": "Aug 19 23:25"
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
      {
        "filename": "awk",
        "link_to": "gawk",
        "flags": "lrwxrwxrwx.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "4",
        "date": "Aug 15 10:53"
      },
      {
        "filename": "base64",
        "flags": "-rwxr-xr-x.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "37360",
        "date": "Aug 19 23:25"
      },
      {
        "filename": "basename",
        "flags": "-rwxr-xr-x.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "29032",
        "date": "Aug 19 23:25"
      },
      {
        "filename": "bash",
        "flags": "-rwxr-xr-x.",
        "links": "1",
        "owner": "root",
        "group": "root",
        "size": "964600",
        "date": "Aug 8 05:06"
      },
      ...
    ]

    $ ls -l /usr/bin | jc --ls | jq '.[] | select(.size > 50000000)'
    {
      "filename": "emacs",
      "flags": "-r-xr-xr-x",
      "links": 1,
      "owner": "root",
      "group": "wheel",
      "size": 117164432,
      "date": "May 3 2019"
    }
"""
import re
import jc.utils


class info():
    version = '1.6'
    description = 'ls command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['ls']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "filename": string,
            "flags":    string,
            "links":    integer,
            "parent":   string,
            "owner":    string,
            "group":    string,
            "size":     integer,
            "date":     string
          }
        ]
    """

    for entry in proc_data:
        int_list = ['links', 'size']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

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
        if not re.match(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', linedata[0]) \
           and linedata[0].endswith(':'):
            parent = linedata.pop(0)[:-1]
            # Pop following total line if it exists
            if re.match(r'total [0-9]+', linedata[0]):
                linedata.pop(0)

        # Check if -l was used to parse extra data
        if re.match(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', linedata[0]):
            for entry in linedata:
                output_line = {}

                parsed_line = entry.split(maxsplit=8)

                if not re.match(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', entry) \
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
                   and not re.match(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', entry):
                    raw_output[-1]['filename'] = raw_output[-1]['filename'] + '\n' + entry
                    continue

                # split filenames and links
                if len(parsed_line) == 9:
                    filename_field = parsed_line[8].split(' -> ')
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
                output_line['size'] = parsed_line[4]
                output_line['date'] = ' '.join(parsed_line[5:8])
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
                    jc.utils.warning_message('Newline characters detected. Filenames probably corrupted. Use ls -l or -b instead.')
                    warned = True

                output_line['filename'] = entry

                if parent:
                    output_line['parent'] = parent

                raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
