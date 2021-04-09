"""jc - JSON CLI output utility `mount` command output parser

Usage (cli):

    $ mount | jc --mount

    or

    $ jc mount

Usage (module):

    import jc.parsers.mount
    result = jc.parsers.mount.parse(mount_command_output)

Schema:

    [
      {
        "filesystem":       string,
        "mount_point":      string,
        "type":             string,
        "access": [
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
        "access": [
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
        "access": [
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
        "access": [
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
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.6'
    description = '`mount` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['mount']


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
        parsed_line = entry.split()

        output_line['filesystem'] = parsed_line[0]
        output_line['mount_point'] = parsed_line[2]
        output_line['type'] = parsed_line[4]

        options = parsed_line[5].lstrip('(').rstrip(')').split(',')

        output_line['options'] = options

        output.append(output_line)

    return output


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

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))
    raw_output = []

    if jc.utils.has_data(data):

        # check for OSX output
        if ' type ' not in cleandata[0]:
            raw_output = _osx_parse(cleandata)

        else:
            raw_output = _linux_parse(cleandata)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
