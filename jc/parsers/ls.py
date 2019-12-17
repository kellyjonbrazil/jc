"""jc - JSON CLI output utility ls Parser

Usage:

    specify --ls as the first argument if the piped input is coming from ls

    ls options supported:
    - None
    - la
    - h       file sizes will be available in text form with -r but larger file sizes
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
    version = '1.0'
    description = 'ls parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']


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

    linedata = data.splitlines()

    # Delete first line if it starts with 'total'
    if linedata:
        if linedata[0].find('total') == 0:
            linedata.pop(0)

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:
        # Check if -l was used to parse extra data
        if re.match('^[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', cleandata[0]):
            for entry in cleandata:
                output_line = {}

                parsed_line = entry.split(maxsplit=8)

                # split filenames and links
                filename_field = parsed_line[8].split(' -> ')

                # create list of dictionaries
                output_line['filename'] = filename_field[0]

                if len(filename_field) > 1:
                    output_line['link_to'] = filename_field[1]

                output_line['flags'] = parsed_line[0]
                output_line['links'] = parsed_line[1]
                output_line['owner'] = parsed_line[2]
                output_line['group'] = parsed_line[3]
                output_line['size'] = parsed_line[4]
                output_line['date'] = ' '.join(parsed_line[5:8])
                raw_output.append(output_line)
        else:
            for entry in cleandata:
                output_line = {}
                output_line['filename'] = entry
                raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
