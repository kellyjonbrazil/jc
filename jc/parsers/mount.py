"""jc - JSON Convert `mount` command output parser

Usage (cli):

    $ mount | jc --mount

or

    $ jc mount

Usage (module):

    import jc
    result = jc.parse('mount', mount_command_output)

Schema:

    [
      {
        "filesystem":       string,
        "mount_point":      string,
        "type":             string,
        "options": [
                            string
        ]
      }
    ]

Example:

    $ mount | jc --mount -p
    [
      {
        "filesystem": "sysfs",
        "mount_point": "/sys",
        "type": "sysfs",
        "options": [
          "rw",
          "nosuid",
          "nodev",
          "noexec",
          "relatime"
        ]
      },
      {
        "filesystem": "proc",
        "mount_point": "/proc",
        "type": "proc",
        "options": [
          "rw",
          "nosuid",
          "nodev",
          "noexec",
          "relatime"
        ]
      },
      {
        "filesystem": "udev",
        "mount_point": "/dev",
        "type": "devtmpfs",
        "options": [
          "rw",
          "nosuid",
          "relatime",
          "size=977500k",
          "nr_inodes=244375",
          "mode=755"
        ]
      },
      ...
    ]
"""
import re

import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.9'
    description = '`mount` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd', 'aix']
    magic_commands = ['mount']
    tags = ['command']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    # nothing to process
    return proc_data


def _osx_parse(data):
    output = []

    for entry in data:
        output_line = {}

        filesystem = entry.split(' on ')
        filesystem = filesystem[0]
        output_line['filesystem'] = filesystem

        mount_point = entry.split(' on ')
        mount_point = mount_point[1].split(' (')
        mount_point = mount_point[0]
        output_line['mount_point'] = mount_point

        options = entry.split('(', maxsplit=1)
        options = options[1].rstrip(')')
        options = options.split(', ')
        output_line['options'] = options

        output.append(output_line)

    return output


def _linux_parse(data):
    output = []

    for entry in data:
        output_line = {}

        pattern = re.compile(
            r'''
            (?P<filesystem>\S+)\s+
            on\s+
            (?P<mount_point>.*?)\s+
            type\s+
            (?P<type>\S+)\s+
            \((?P<options>.*?)\)\s*''',
            re.VERBOSE)

        match = pattern.match(entry)
        groups = match.groupdict()

        if groups:
            output_line['filesystem'] = groups["filesystem"]
            output_line['mount_point'] = groups["mount_point"]
            output_line['type'] = groups["type"]
            output_line['options'] = groups["options"].split(',')
            output.append(output_line)

    return output

def _aix_parse(data):
    output = []

    # AIX mount command starts with these headers:
    #   node       mounted        mounted over    vfs       date        options
    # -------- ---------------  ---------------  ------ ------------ ---------------
    # Remove them
    data.pop(0)
    data.pop(0)

    for entry in data:
        output_line = {}
        parsed_line = entry.split()

        # AIX mount entries have the remote node as the zeroth element. If the
        # mount is local, the zeroth element is the filesystem instead. We can
        # detect this by the length of the list. For local mounts, length is 7,
        # and for remote mounts, the length is 8. In the remote case, pop off
        # the zeroth element. Then parsed_line has a consistent format.
        if len(parsed_line) == 8:
            parsed_line.pop(0)

        output_line['filesystem'] = parsed_line[0]
        output_line['mount_point'] = parsed_line[1]
        output_line['type'] = parsed_line[2]
        output_line['options'] = parsed_line[6].lstrip('(').rstrip(')').split(',')

        output.append(output_line)

    return output


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

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))
    raw_output = []

    if jc.utils.has_data(data):

        # check for OSX and AIX output
        if ' type ' not in cleandata[0]:
            if 'node' in cleandata[0]:
                raw_output = _aix_parse(cleandata)
            else:
                raw_output = _osx_parse(cleandata)

        else:
            raw_output = _linux_parse(cleandata)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
