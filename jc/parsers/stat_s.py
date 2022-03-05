"""jc - JSON Convert `stat` command output streaming parser

> This streaming parser outputs JSON Lines

The `xxx_epoch` calculated timestamp fields are naive. (i.e. based on the
local time of the system the parser is run on).

The `xxx_epoch_utc` calculated timestamp fields are timezone-aware and are
only available if the timezone field is UTC.

Usage (cli):

    $ stat * | jc --stat-s

Usage (module):

    import jc
    # result is an iterable object (generator)
    result = jc.parse('stat_s', stat_command_output.splitlines())
    for item in result:
        # do something

    or

    import jc.parsers.stat_s
    # result is an iterable object (generator)
    result = jc.parsers.stat_s.parse(stat_command_output.splitlines())
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

      # Below object only exists if using -qq or ignore_exceptions=True

      "_jc_meta":
        {
          "success":              boolean,   # false if error parsing
          "error":                string,    # exists if "success" is false
          "line":                 string     # exists if "success" is false
        }
    }

Examples:

    $ stat | jc --stat-s
    {"file":"(stdin)","unix_device":1027739696,"inode":1155,"flags":"cr...}

    $ stat | jc --stat-s -r
    {"file":"(stdin)","unix_device":"1027739696","inode":"1155","flag...}
"""
import shlex
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`stat` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    streaming = True


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = ['size', 'blocks', 'io_blocks', 'inode', 'links', 'uid', 'gid',
                'unix_device', 'rdev', 'block_size']
    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

    # turn - into null for time fields and add calculated timestamp fields
    null_list = ['access_time', 'modify_time', 'change_time', 'birth_time']
    for key in null_list:
        if key in proc_data:
            if proc_data[key] == '-':
                proc_data[key] = None
            ts = jc.utils.timestamp(proc_data[key], format_hint=(7100, 7200))
            proc_data[key + '_epoch'] = ts.naive
            proc_data[key + '_epoch_utc'] = ts.utc

    return proc_data


@add_jc_meta
def parse(data, raw=False, quiet=False, ignore_exceptions=False):
    """
    Main text parsing generator function. Returns an iterator object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Yields:

        Dictionary. Raw or processed structured data.

    Returns:

        Iterator object (generator)
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    output_line = {}
    os_type = ''

    for line in data:
        try:
            streaming_line_input_type_check(line)
            line = line.rstrip()

            # ignore blank lines
            if line == '':
                continue

            # linux output
            if line.startswith('  File: '):
                os_type = 'linux'

            if os_type == 'linux':
                # stats output contains 9 lines
                # line #1
                if line.startswith('  File: '):
                    if output_line:
                        yield output_line if raw else _process(output_line)

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
                if line.startswith('  Size: '):
                    line_list = line.split(maxsplit=7)
                    output_line['size'] = line_list[1]
                    output_line['blocks'] = line_list[3]
                    output_line['io_blocks'] = line_list[6]
                    output_line['type'] = line_list[7]
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
                value = shlex.split(line)

                if not value[0].isdigit() or not value[1].isdigit():
                    raise ParseError('Not stat data')

                output_line = {
                    'file': ' '.join(value[15:]),
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
