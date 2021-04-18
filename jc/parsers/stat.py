"""jc - JSON CLI output utility `stat` command output parser

The `xxx_epoch` calculated timestamp fields are naive (i.e. based on the local time of the system the parser is run on)

The `xxx_epoch_utc` calculated timestamp fields are timezone-aware and are only available if the timezone field is UTC.

Usage (cli):

    $ stat * | jc --stat

    or

    $ jc stat *

Usage (module):

    import jc.parsers.stat
    result = jc.parsers.stat.parse(stat_command_output)

Schema:

    [
      {
        "file":                     string,
        "link_to"                   string,
        "size":                     integer,
        "blocks":                   integer,
        "io_blocks":                integer,
        "type":                     string,
        "device":                   string,
        "inode":                    integer,
        "links":                    integer,
        "access":                   string,
        "flags":                    string,
        "uid":                      integer,
        "user":                     string,
        "gid":                      integer,
        "group":                    string,
        "access_time":              string,    # - = null
        "access_time_epoch":        integer,   # naive timestamp
        "access_time_epoch_utc":    integer,   # timezone-aware timestamp
        "modify_time":              string,    # - = null
        "modify_time_epoch":        integer,   # naive timestamp
        "modify_time_epoch_utc":    integer,   # timezone-aware timestamp
        "change_time":              string,    # - = null
        "change_time_epoch":        integer,   # naive timestamp
        "change_time_epoch_utc":    integer,   # timezone-aware timestamp
        "birth_time":               string,    # - = null
        "birth_time_epoch":         integer,   # naive timestamp
        "birth_time_epoch_utc":     integer,   # timezone-aware timestamp
        "unix_device":              integer,
        "rdev":                     integer,
        "block_size":               integer,
        "unix_flags":               string
      }
    ]

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
        "birth_time": null,
        "access_time_epoch": 1573748283,
        "access_time_epoch_utc": 1573719483,
        "modify_time_epoch": 1559885295,
        "modify_time_epoch_utc": 1559860095,
        "change_time_epoch": 1565655689,
        "change_time_epoch_utc": 1565630489,
        "birth_time_epoch": null,
        "birth_time_epoch_utc": null
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
        "birth_time": null,
        "access_time_epoch": 1573748308,
        "access_time_epoch_utc": 1573719508,
        "modify_time_epoch": 1520921067,
        "modify_time_epoch_utc": 1520895867,
        "change_time_epoch": 1565655689,
        "change_time_epoch_utc": 1565630489,
        "birth_time_epoch": null,
        "birth_time_epoch_utc": null
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
      ...
    ]
"""
import shlex
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.8'
    description = '`stat` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['stat']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        int_list = ['size', 'blocks', 'io_blocks', 'inode', 'links', 'uid', 'gid', 'unix_device',
                    'rdev', 'block_size']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    # turn - into null for time fields and add calculated timestamp fields
    for entry in proc_data:
        null_list = ['access_time', 'modify_time', 'change_time', 'birth_time']
        for key in null_list:
            if key in entry:
                if entry[key] == '-':
                    entry[key] = None
                ts = jc.utils.timestamp(entry[key])
                entry[key + '_epoch'] = ts.naive
                entry[key + '_epoch_utc'] = ts.utc

    return proc_data


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

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        # linux output
        if cleandata[0].startswith('  File: '):
            # stats output contains 8 lines
            for line in cleandata:

                # line #1
                if line.find('File:') == 2:
                    output_line = {}
                    line_list = line.split(maxsplit=1)
                    output_line['file'] = line_list[1]

                    # populate link_to field if -> found
                    if ' -> ' in output_line['file']:
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
                if line.startswith('Device:'):
                    line_list = line.split()
                    output_line['device'] = line_list[1]
                    output_line['inode'] = line_list[3]
                    output_line['links'] = line_list[5]
                    continue

                # line #4
                if line.startswith('Access: ('):
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
                if line.startswith('Access: 2'):
                    line_list = line.split(maxsplit=1)
                    output_line['access_time'] = line_list[1]
                    continue

                # line #6
                if line.startswith('Modify:'):
                    line_list = line.split(maxsplit=1)
                    output_line['modify_time'] = line_list[1]
                    continue

                # line #7
                if line.startswith('Change:'):
                    line_list = line.split(maxsplit=1)
                    output_line['change_time'] = line_list[1]
                    continue

                # line #8
                if line.find('Birth:') == 1:
                    line_list = line.split(maxsplit=1)
                    output_line['birth_time'] = line_list[1]

                    raw_output.append(output_line)
                    continue

        # FreeBSD/OSX output
        else:
            for line in cleandata:
                value = shlex.split(line)
                output_line = {
                    'file': value[15],
                    'unix_device': value[0],
                    'inode': value[1],
                    'flags': value[2],
                    'links': value[3],
                    'user': value[4],
                    'group': value[5],
                    'rdev': value[6],
                    'size': value[7],
                    'access_time': value[8],
                    'modify_time': value[9],
                    'change_time': value[10],
                    'birth_time': value[11],
                    'block_size': value[12],
                    'blocks': value[13],
                    'unix_flags': value[14]
                }

                raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
