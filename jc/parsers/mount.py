r"""jc - JSON Convert `mount` command output parser

> Note: Mount points that contain ` on ` (space, on, space) are not
> supported because `mount` output does not mark where the mount point
> begins.

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
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.12'
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


# a backslash and the character after it, a double-quoted string, or a comma
_OPTION_TOKEN = re.compile(r'\\.|"[^"]*"|,')


def _split_options(options):
    """
    Split a comma-separated option list. Commas inside a double-quoted
    string (e.g. an SELinux `context="...:c12,c34"`) or escaped with a
    backslash (e.g. an overlay `upperdir=/a\\,b`) do not split. The option
    text is kept as printed.
    """
    result = []
    start = 0

    for match in _OPTION_TOKEN.finditer(options):
        if match.group() == ',':
            result.append(options[start:match.start()])
            start = match.end()

    result.append(options[start:])
    return result


# The options are at the end of the line, so the entry is matched from the
# end: the last `type <type> (<options>)` (Linux) or ` (<options>)` (macOS and
# BSD) ends the mount point, and the last ` on ` before it ends the filesystem.
_LINUX_TAIL = re.compile(
    r'''
        (?P<head>.*)
        \stype\s
        (?P<type>\S+)
        \s+
        \((?P<options>.*)\)\Z
    ''', re.VERBOSE
)

_OSX_TAIL = re.compile(
    r'''
        (?P<head>.*)
        \s
        \((?P<options>.*)\)\Z
    ''', re.VERBOSE
)

_HEAD = re.compile(
    r'''
        (?P<filesystem>.*)
        \son\s
        (?P<mount_point>.*)\Z
    ''', re.VERBOSE
)


def _trim_entry(entry):
    """Cut the entry after the `)` that closes the options."""
    entry = entry.rstrip()

    # `mount -l` adds the filesystem label as ` [LABEL]` at the end
    if entry.endswith(']'):
        pos = entry.rfind(') [')
        if pos != -1:
            entry = entry[:pos + 1]

    # a match always ends at a `)`, so stop at the last one
    return entry[:entry.rfind(')') + 1]


def _match_entry(tail_pattern, entry):
    """Return the tail and head groupdicts of an entry or raise ParseError"""
    tail = tail_pattern.match(_trim_entry(entry))
    head = _HEAD.match(tail.group('head')) if tail else None

    if not head:
        raise ParseError('Unrecognized mount line')

    return tail.groupdict(), head.groupdict()


def _osx_parse(data):
    output = []

    for entry in data:
        output_line = {}

        tail, groups = _match_entry(_OSX_TAIL, entry)

        if groups:
            output_line['filesystem'] = groups['filesystem']
            output_line['mount_point'] = groups['mount_point']
            options = tail['options'].split(', ')
            output_line['options'] = options

        output.append(output_line)

    return output


def _linux_parse(data):
    output = []

    for entry in data:
        output_line = {}

        tail, groups = _match_entry(_LINUX_TAIL, entry)

        if groups:
            output_line['filesystem'] = groups["filesystem"]
            output_line['mount_point'] = groups["mount_point"]
            output_line['type'] = tail["type"]
            output_line['options'] = _split_options(tail["options"])
            output.append(output_line)

    return output


_AIX_HEADER = ['node', 'mounted', 'mounted', 'over', 'vfs', 'date', 'options']


def _aix_columns(separator_line):
    """
    Return the start positions of the columns in the AIX header separator
    line (`-------- ---------------  ...`).
    """
    return [m.start() for m in re.finditer(r'-+', separator_line)]


def _aix_split_head(head, has_node, mounted_over_start):
    """
    Return the device and the mount point from the start of an AIX row
    (everything before the vfs column), skipping the node name if there is
    one. The mount point can contain spaces, so it starts at the
    `mounted over` column when the row is aligned to it. Otherwise the
    device is the first word after the node.
    """
    pos = 0

    if has_node:
        pos = re.match(r'\S+', head).end()

    if (mounted_over_start is not None
            and pos < mounted_over_start < len(head)
            and head[mounted_over_start - 1].isspace()
            and not head[mounted_over_start].isspace()
            and head[pos:mounted_over_start].strip()):
        device = head[pos:mounted_over_start].strip()
        mount_point = head[mounted_over_start:].strip()
    else:
        device, mount_point = head[pos:].split(None, 1)
        mount_point = mount_point.strip()

    return device, mount_point


def _aix_parse(data):
    output = []

    # AIX mount command starts with these headers:
    #   node       mounted        mounted over    vfs       date        options
    # -------- ---------------  ---------------  ------ ------------ ---------------
    # Remove them
    data.pop(0)
    columns = _aix_columns(data.pop(0))
    mounted_over_start = columns[2] if len(columns) > 2 else None

    for entry in data:
        output_line = {}

        # vfs, the three date words, and the options are the last five words
        # of the row. The node, device, and mount point are in front of them.
        head, vfs, _, _, _, options = entry.rstrip().rsplit(None, 5)

        head_words = head.split()

        if len(head_words) == 2:
            device, mount_point = head_words
        else:
            # local mounts have a blank node column. Remote mounts start with
            # the node name.
            has_node = not head[0].isspace()
            device, mount_point = _aix_split_head(head, has_node, mounted_over_start)

        output_line['filesystem'] = device
        output_line['mount_point'] = mount_point
        output_line['type'] = vfs
        output_line['options'] = _split_options(options.lstrip('(').rstrip(')'))

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
    cleandata = list(filter(None, jc.utils.splitlines(data)))
    raw_output = []

    if jc.utils.has_data(data):

        # check for OSX and AIX output
        if ' type ' not in cleandata[0]:
            # AIX only when the first line is its column header
            if cleandata[0].split() == _AIX_HEADER:
                raw_output = _aix_parse(cleandata)
            else:
                raw_output = _osx_parse(cleandata)

        else:
            raw_output = _linux_parse(cleandata)

    return raw_output if raw else _process(raw_output)
