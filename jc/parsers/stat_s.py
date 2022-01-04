"""jc - JSON CLI output utility `stat` command output streaming parser

> This streaming parser outputs JSON Lines

<<Short stat description and caveats>>

Usage (cli):

    $ stat | jc --stat-s

Usage (module):

    import jc.parsers.stat_s
    result = jc.parsers.stat_s.parse(stat_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "stat":            string,
      "_jc_meta":                    # This object only exists if using -qq or ignore_exceptions=True
        {
          "success":    boolean,     # true if successfully parsed, false if error
          "error":      string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ stat | jc --stat-s
    {example output}
    ...

    $ stat | jc --stat-s -r
    {example output}
    ...
"""
import shlex
import jc.utils
from jc.utils import stream_success, stream_error
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '0.5'
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
    #
    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool conversions and timestamps
    #

    return proc_data


def parse(data, raw=False, quiet=False, ignore_exceptions=False):
    """
    Main text parsing generator function. Returns an iterator object.

    Parameters:

        data:              (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
        raw:               (boolean)   output preprocessed JSON if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Yields:

        Dictionary. Raw or processed structured data.

    Returns:

        Iterator object
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.streaming_input_type_check(data)

    output_line = {}
    os_type = ''

    for line in data:
        try:
            jc.utils.streaming_line_input_type_check(line)
            linecomplete = False
            line = line.rstrip()

            # linux output
            if line.startswith('  File: '):
                os_type = 'linux'

            if os_type == 'linux':
                # stats output contains 9 lines
                # line #1
                if line.startswith('  File: '):
                    if output_line:
                        linecomplete = True
                    else:
                        linecomplete = False
                        output_line = {}
                    line_list = line.split(maxsplit=1)
                    output_line['file'] = line_list[1]

                    # populate link_to field if -> found
                    if ' -> ' in output_line['file']:
                        filename = output_line['file'].split(' -> ')[0].strip('\u2018').rstrip('\u2019')
                        link = output_line['file'].split(' -> ')[1].strip('\u2018').rstrip('\u2019')
                        output_line['file'] = filename
                        output_line['link_to'] = link
                        # continue
                    else:
                        filename = output_line['file'].split(' -> ')[0].strip('\u2018').rstrip('\u2019')
                        output_line['file'] = filename
                        # continue

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
                if line.startswith('Context: '):
                    # ignore this line
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

            # FreeBSD/OSX output
            if os_type != 'linux':
                value = shlex.split(line)
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
                linecomplete = True

            if linecomplete and output_line:
                yield stream_success(output_line, ignore_exceptions) if raw else stream_success(_process(output_line), ignore_exceptions)
            elif linecomplete:
                raise ParseError('Not stat data')

        except Exception as e:
            yield stream_error(e, ignore_exceptions, line)
