"""jc - JSON CLI output utility `ls` and `vdir` command output streaming parser

Options supported:
- `lbaR1`
- `--time-style=full-iso`

Note: The `-1`, `-l`, or `-b` option of `ls` should be used to correctly parse filenames that include newline characters. Since `ls` does not encode newlines in filenames when outputting to a pipe it will cause `jc` to see multiple files instead of a single file if `-1`, `-l`, or `-b` is not used. Alternatively, `vdir` can be used, which is the same as running `ls -lb`.

The `epoch` calculated timestamp field is naive (i.e. based on the local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only available if the timezone field is UTC.

Usage (cli):

    $ ls | jc --ls-s

Usage (module):

    import jc.parsers.ls_s
    result = jc.parsers.ls_s.parse(ls_command_output)    # result is an iterable object
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
      "date":           string,
      "epoch":          integer,     # naive timestamp if date field exists and can be converted
      "epoch_utc":      integer,     # timezone aware timestamp if date field is in UTC and can be converted
      "_meta":                       # This object only exists if using -q or quiet=True
        {
          "success":    booean,      # true if successfully parsed, false if error
          "error_msg":  string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ ls -l /usr/bin | jc --ls-s
    {"filename":"2to3-","flags":"-rwxr-xr-x","links":4,"owner":"root","group":"wheel","size":925,"date":"Feb 22 2019","_meta":{"success":true}}
    {"filename":"2to3-2.7","link_to":"../../System/Library/Frameworks/Python.framework/Versions/2.7/bin/2to3-2.7","flags":"lrwxr-xr-x","links":1,"owner":"root","group":"wheel","size":74,"date":"May 4 2019","_meta":{"success":true}}
    {"filename":"AssetCacheLocatorUtil","flags":"-rwxr-xr-x","links":1,"owner":"root","group":"wheel","size":55152,"date":"May 3 2019","_meta":{"success":true}}
    ...

    $ ls -l /usr/bin | jc --ls-s -r
    {"filename":"2to3-","flags":"-rwxr-xr-x","links":"4","owner":"root","group":"wheel","size":"925","date":"Feb 22 2019","_meta":{"success":true}}
    {"filename":"2to3-2.7","link_to":"../../System/Library/Frameworks/Python.framework/Versions/2.7/bin/2to3-2.7","flags":"lrwxr-xr-x","links":"1","owner":"root","group":"wheel","size":"74","date":"May 4 2019","_meta":{"success":true}}
    {"filename":"AssetCacheLocatorUtil","flags":"-rwxr-xr-x","links":"1","owner":"root","group":"wheel","size":"55152","date":"May 3 2019","_meta":{"success":true}}
    ...
"""
import re
import jc.utils
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`ls` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    streaming = True


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    int_list = ['links', 'size']
    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

    if 'date' in proc_data:
        # to speed up processing only try to convert the date if it's not the default format
        if not re.match(r'[a-zA-Z]{3}\s{1,2}\d{1,2}\s{1,2}[0-9:]{4,5}', proc_data['date']):
            ts = jc.utils.timestamp(proc_data['date'])
            proc_data['epoch'] = ts.naive
            proc_data['epoch_utc'] = ts.utc

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  line-based text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    parent = ''
    new_section = False
    # last_object = {}

    for line in data:
        try:

            # skip line if it starts with 'total 1234'
            if re.match(r'total [0-9]+', line):
                new_section = False
                continue

            # fix for OSX - doesn't print 'total xx' line if empty directory
            if new_section and line.strip() == '':
                new_section = False
                continue

            if not new_section and line.strip() == '':
                continue

            # Look for parent line if glob or -R is used
            if not re.match(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', line) \
               and line.strip().endswith(':'):
                parent = line.strip()[:-1]
                continue

            parsed_line = line.strip().split(maxsplit=8)
            output_line = {}

            # no support for filenames with newline chars in streaming parser
            # if not re.match(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', line) \
            #    and line.endswith(':'):
            #     parent = line[:-1]
            #     new_section = True

                # no support for filenames with newline chars in streaming parser
                # fixup to remove trailing \n in previous entry
                # raw_output[-1]['filename'] = raw_output[-1]['filename'][:-1]
                # continue

            # no support for filenames with newline chars in streaming parser
            # fixup for filenames with newlines
            # if not new_section \
            #    and not re.match(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', entry):
            #     raw_output[-1]['filename'] = raw_output[-1]['filename'] + '\n' + entry
            #     continue

            # Only support -l option 
            # if not re.match(r'[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', line):
            #     raise ParseError(f'Unparsable line: {line.rstrip()[0:60]}')

            # split filenames and links
            if len(parsed_line) == 9:
                filename_field = parsed_line[8].split(' -> ')
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
            output_line['size'] = parsed_line[4]
            output_line['date'] = ' '.join(parsed_line[5:8])

            if quiet:
                output_line['_meta'] = {'success': True}

            last_object = output_line
            
            if raw:
                yield output_line
            else:
                yield _process(output_line)
            
        except Exception as e:
            if not quiet:
                e.args = (str(e) + '... Try the quiet option (-q) to ignore errors.',)
                raise e
            else:
                yield {
                    '_meta':
                        {
                            'success': False,
                            'error': 'error parsing line',
                            'line': line.strip()
                        }
                }
