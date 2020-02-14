"""jc - JSON CLI output utility stat Parser

Usage:

    specify --stat as the first argument if the piped input is coming from stat

Compatibility:

    'linux'

Examples:

    $ stat /bin/* | jc --stat -p
    [
      {
        "file": "/bin/bash",
        "size": 1113504,
        "blocks": 2176,
        "io_blocks": 4096,
        "type": "regular file",
        "device": "802h/2050d",
        "inode": 131099,
        "links": 1,
        "access": "0755",
        "flags": "-rwxr-xr-x",
        "uid": 0,
        "user": "root",
        "gid": 0,
        "group": "root",
        "access_time": "2019-11-14 08:18:03.509681766 +0000",
        "modify_time": "2019-06-06 22:28:15.000000000 +0000",
        "change_time": "2019-08-12 17:21:29.521945390 +0000",
        "birth_time": null
      },
      {
        "file": "/bin/btrfs",
        "size": 716464,
        "blocks": 1400,
        "io_blocks": 4096,
        "type": "regular file",
        "device": "802h/2050d",
        "inode": 131100,
        "links": 1,
        "access": "0755",
        "flags": "-rwxr-xr-x",
        "uid": 0,
        "user": "root",
        "gid": 0,
        "group": "root",
        "access_time": "2019-11-14 08:18:28.990834276 +0000",
        "modify_time": "2018-03-12 23:04:27.000000000 +0000",
        "change_time": "2019-08-12 17:21:29.545944399 +0000",
        "birth_time": null
      },
      ...
    ]

    $ stat /bin/* | jc --stat -p -r
    [
      {
        "file": "/bin/bash",
        "size": "1113504",
        "blocks": "2176",
        "io_blocks": "4096",
        "type": "regular file",
        "device": "802h/2050d",
        "inode": "131099",
        "links": "1",
        "access": "0755",
        "flags": "-rwxr-xr-x",
        "uid": "0",
        "user": "root",
        "gid": "0",
        "group": "root",
        "access_time": "2019-11-14 08:18:03.509681766 +0000",
        "modify_time": "2019-06-06 22:28:15.000000000 +0000",
        "change_time": "2019-08-12 17:21:29.521945390 +0000",
        "birth_time": null
      },
      {
        "file": "/bin/btrfs",
        "size": "716464",
        "blocks": "1400",
        "io_blocks": "4096",
        "type": "regular file",
        "device": "802h/2050d",
        "inode": "131100",
        "links": "1",
        "access": "0755",
        "flags": "-rwxr-xr-x",
        "uid": "0",
        "user": "root",
        "gid": "0",
        "group": "root",
        "access_time": "2019-11-14 08:18:28.990834276 +0000",
        "modify_time": "2018-03-12 23:04:27.000000000 +0000",
        "change_time": "2019-08-12 17:21:29.545944399 +0000",
        "birth_time": null
      },
      ..
    ]
"""
import jc.utils


class info():
    version = '1.0'
    description = 'stat command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['stat']


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
            "file":         string,
            "link_to"       string,
            "size":         integer,
            "blocks":       integer,
            "io_blocks":    integer,
            "type":         string,
            "device":       string,
            "inode":        integer,
            "links":        integer,
            "access":       string,
            "flags":        string,
            "uid":          integer,
            "user":         string,
            "gid":          integer,
            "group":        string,
            "access_time":  string,    # - = null
            "modify_time":  string,    # - = null
            "change_time":  string,    # - = null
            "birth_time":   string     # - = null
          }
        ]
    """
    for entry in proc_data:
        int_list = ['size', 'blocks', 'io_blocks', 'inode', 'links', 'uid', 'gid']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

    # turn - into null for time fields
    for entry in proc_data:
        null_list = ['access_time', 'modify_time', 'change_time', 'birth_time']
        for key in null_list:
            if key in entry:
                if entry[key] == '-':
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
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if cleandata:
        # stats output contains 8 lines
        for line in cleandata:

            # line #1
            if line.find('File:') == 2:
                output_line = {}
                line_list = line.split(maxsplit=1)
                output_line['file'] = line_list[1]

                # populate link_to field if -> found
                if output_line['file'].find(' -> ') != -1:
                    filename = output_line['file'].split(' -> ')[0].strip('\u2018').rstrip('\u2019')
                    link = output_line['file'].split(' -> ')[1].strip('\u2018').rstrip('\u2019')
                    output_line['file'] = filename
                    output_line['link_to'] = link
                else:
                    filename = output_line['file'].split(' -> ')[0].strip('\u2018').rstrip('\u2019')
                    output_line['file'] = filename

                continue

            # line #2
            if line.find('Size:') == 2:
                line_list = line.split(maxsplit=7)
                output_line['size'] = line_list[1]
                output_line['blocks'] = line_list[3]
                output_line['io_blocks'] = line_list[6]
                output_line['type'] = line_list[7]
                continue

            # line #3
            if line.find('Device:') == 0:
                line_list = line.split()
                output_line['device'] = line_list[1]
                output_line['inode'] = line_list[3]
                output_line['links'] = line_list[5]
                continue

            # line #4
            if line.find('Access: (') == 0:
                line = line.replace('(', ' ').replace(')', ' ').replace('/', ' ')
                line_list = line.split()
                output_line['access'] = line_list[1]
                output_line['flags'] = line_list[2]
                output_line['uid'] = line_list[4]
                output_line['user'] = line_list[5]
                output_line['gid'] = line_list[7]
                output_line['group'] = line_list[8]
                continue

            # line #5
            if line.find('Access: 2') == 0:
                line_list = line.split(maxsplit=1)
                output_line['access_time'] = line_list[1]
                continue

            # line #6
            if line.find('Modify:') == 0:
                line_list = line.split(maxsplit=1)
                output_line['modify_time'] = line_list[1]
                continue

            # line #7
            if line.find('Change:') == 0:
                line_list = line.split(maxsplit=1)
                output_line['change_time'] = line_list[1]
                continue

            # line #8
            if line.find('Birth:') == 1:
                line_list = line.split(maxsplit=1)
                output_line['birth_time'] = line_list[1]

                raw_output.append(output_line)
                continue

    if raw:
        return raw_output
    else:
        return process(raw_output)
