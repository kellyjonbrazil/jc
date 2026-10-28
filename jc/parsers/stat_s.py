r"""jc - JSON Convert `stat` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

The `xxx_epoch` calculated timestamp fields are naive. (i.e. based on the
local time of the system the parser is run on).

The `xxx_epoch_utc` calculated timestamp fields are timezone-aware and are
only available if the timezone field is UTC.

Only symbolic links (`type` is `symbolic link`) have a `link_to` field. The
`File:` line is split at the first ` -> `, so a link whose name contains
` -> ` reports the rest of its name as part of `link_to`.

Usage (cli):

    $ stat * | jc --stat-s

Usage (module):

    import jc

    result = jc.parse('stat_s', stat_command_output.split('\n'))
    for item in result:
        # do something

Schema:

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
      "unix_flags":               string,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":                boolean,   # false if error parsing
        "error":                  string,    # exists if "success" is false
        "line":                   string     # exists if "success" is false
      }
    }

Examples:

    $ stat | jc --stat-s
    {"file":"(stdin)","unix_device":1027739696,"inode":1155,"flags":"cr...}

    $ stat | jc --stat-s -r
    {"file":"(stdin)","unix_device":"1027739696","inode":"1155","flag...}
"""
import re
import shlex
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from typing import Dict, Iterable, Set
from jc.jc_types import JSONDictType, StreamingOutputType
from jc.exceptions import ParseError

# The default FreeBSD/macOS `stat` format: device, inode, mode, links, user,
# group, rdev, size, four quoted timestamps, block size, blocks, flags, then
# the file name, which is printed as is and can contain any character.
_BSD_STAT_RE = re.compile(
    r'(\d+) (\d+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)'
    r' "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)"'
    r' (\S+) (\S+) (\S+) (.*)\Z'
)


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.4'
    description = '`stat` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    tags = ['command']
    streaming = True


__version__ = info.version


def _strip_quotes(name: str) -> str:
    """Remove the curly quotes older versions of `stat` print around names."""
    return name.strip('\u2018').rstrip('\u2019')


def _add_link_to(output_line: Dict, file_field: str) -> Dict:
    """
    Split the `File:` field of a symbolic link into `file` and `link_to`.
    `stat` prints 'name -> target'. A link name that contains ' -> ' is
    ambiguous, so the field is split at the first ' -> '. Returns a new
    dictionary with `link_to` directly after `file`.
    """
    if ' -> ' not in file_field:
        return output_line

    filename, link = file_field.split(' -> ', 1)
    new_line = {'file': _strip_quotes(filename), 'link_to': _strip_quotes(link)}

    for key, value in output_line.items():
        if key != 'file':
            new_line[key] = value

    return new_line


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list: Set[str] = {'size', 'blocks', 'io_blocks', 'inode', 'links', 'uid', 'gid',
                'unix_device', 'rdev', 'block_size'}

    null_list: Set[str] = {'access_time', 'modify_time', 'change_time', 'birth_time'}

    for key in proc_data.copy():
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

        # turn - into null for time fields and add calculated timestamp fields
        if key in null_list:
            if proc_data[key] == '-':
                proc_data[key] = None

            ts_string = proc_data[key]
            if isinstance(ts_string, str) or ts_string is None:
                ts = jc.utils.timestamp(ts_string, format_hint=(7100, 7200))
                proc_data[key + '_epoch'] = ts.naive
                proc_data[key + '_epoch_utc'] = ts.utc

    return proc_data


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> StreamingOutputType:
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

    output_line: Dict = {}
    os_type = ''
    file_field = ''

    for line in data:
        try:
            streaming_line_input_type_check(line)
            # only the line terminator is dropped from the `File:` line, as
            # the name can end with, or consist of, whitespace
            file_line = line.rstrip('\r\n')
            line = line.rstrip()

            # ignore blank lines
            if not line.strip():
                continue

            # linux output
            if file_line.startswith('  File: '):
                os_type = 'linux'

            if os_type == 'linux':
                # stats output contains 9 lines
                # line #1
                if file_line.startswith('  File: '):
                    if output_line:
                        yield output_line if raw else _process(output_line)

                    output_line = {}
                    file_field = file_line[len('  File: '):]

                    # link_to is split off once the file type is known
                    output_line['file'] = _strip_quotes(file_field)
                    continue

                # line #2
                if line.startswith('  Size: '):
                    line_list = line.split(maxsplit=7)
                    output_line['size'] = line_list[1]
                    output_line['blocks'] = line_list[3]
                    output_line['io_blocks'] = line_list[6]
                    output_line['type'] = line_list[7]

                    if output_line['type'] == 'symbolic link':
                        output_line = _add_link_to(output_line, file_field)

                    continue

                # line #3
                if line.startswith('Device: '):
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
                # not implemented
                if line.startswith('Context: '):
                    continue

                # line #6
                if line.startswith('Access: 2'):
                    line_list = line.split(maxsplit=1)
                    output_line['access_time'] = line_list[1]
                    continue

                # line #7
                if line.startswith('Modify: '):
                    line_list = line.split(maxsplit=1)
                    output_line['modify_time'] = line_list[1]
                    continue

                # line #8
                if line.startswith('Change: '):
                    line_list = line.split(maxsplit=1)
                    output_line['change_time'] = line_list[1]
                    continue

                # line #9
                if line.startswith(' Birth: '):
                    line_list = line.split(maxsplit=1)
                    output_line['birth_time'] = line_list[1]
                    continue

                # catch non-stat data
                raise ParseError('Not stat data')

            # FreeBSD/OSX output
            if os_type != 'linux':
                match = _BSD_STAT_RE.match(file_line)
                if match:
                    value = list(match.groups())
                else:
                    value = shlex.split(line)
                    if not value[0].isdigit() or not value[1].isdigit():
                        raise ParseError('Not stat data')

                    value[15:] = [' '.join(value[15:])]

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

                if output_line:
                    yield output_line if raw else _process(output_line)
                    output_line = {}

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)

    # gather final item
    try:
        if output_line:
            yield output_line if raw else _process(output_line)

    except Exception as e:
        yield raise_or_yield(ignore_exceptions, e, '')
