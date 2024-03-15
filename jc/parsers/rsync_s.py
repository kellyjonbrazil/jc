r"""jc - JSON Convert `rsync` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Supports the `-i` or `--itemize-changes` options with all levels of
verbosity. This parser will process the `STDOUT` output or a log file
generated with the `--log-file` option.

Usage (cli):

    $ rsync -i -a source/ dest | jc --rsync-s

or

    $ cat rsync-backup.log | jc --rsync-s

Usage (module):

    import jc

    result = jc.parse('rsync_s', rsync_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "type":                           string,       # 'file' or 'summary'
      "date":                           string,
      "time":                           string,
      "process":                        integer,
      "sent":                           integer,
      "received":                       integer,
      "total_size":                     integer,
      "matches":                        integer,
      "hash_hits":                      integer,
      "false_alarms":                   integer,
      "data":                           integer,
      "bytes_sec":                      float,
      "speedup":                        float,
      "filename":                       string,
      "date":                           string,
      "time":                           string,
      "process":                        integer,
      "metadata":                       string,
      "update_type":                    string/null,  # [0]
      "file_type":                      string/null,  # [1]
      "checksum_or_value_different":    bool/null,
      "size_different":                 bool/null,
      "modification_time_different":    bool/null,
      "permissions_different":          bool/null,
      "owner_different":                bool/null,
      "group_different":                bool/null,
      "acl_different":                  bool/null,
      "extended_attribute_different":   bool/null,
      "epoch":                          integer,      # [2]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] 'file sent', 'file received', 'local change or creation',
        'hard link', 'not updated', 'message'
    [1] 'file', 'directory', 'symlink', 'device', 'special file'
    [2] naive timestamp if time and date fields exist and can be converted.

Examples:

    $ rsync -i -a source/ dest | jc --rsync-s
    {"type":"file","filename":"./","metadata":".d..t......","update_...}
    ...

    $ cat rsync_backup.log | jc --rsync-s
    {"type":"file","filename":"./","date":"2022/01/28","time":"03:53...}
    ...
"""
import re
from typing import Dict, Iterable, Union
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`rsync` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    tags = ['command']
    streaming = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = {
        'process', 'sent', 'received', 'total_size', 'matches', 'hash_hits',
        'false_alarms', 'data'
    }

    float_list = {'bytes_sec', 'speedup'}

    for key in proc_data.copy():
        if key in int_list:
            proc_data[key] = jc.utils.convert_size_to_int(proc_data[key])

        if key in float_list:
            converted_val: Union[float, None] = None
            val = proc_data[key]
            if any([
                'K' in val,
                'M' in val,
                'G' in val,
                'T' in val
            ]):
                converted_int_val = jc.utils.convert_size_to_int(val)

                if not converted_int_val is None:
                    converted_val = float(converted_int_val)

            else:
                converted_val = jc.utils.convert_to_float(val)

            proc_data[key] = converted_val

        # add timestamp
        if 'date' in proc_data and 'time' in proc_data:
            date = proc_data['date'].replace('/', '-')
            date_time = f'{date} {proc_data["time"]}'
            ts = jc.utils.timestamp(date_time, format_hint=(7250,))
            proc_data['epoch'] = ts.naive

    return proc_data


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Union[Iterable[Dict], tuple]:
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    summary: Dict = {}
    process: str = ''
    last_process: str = ''

    update_type = {
        '<': 'file sent',
        '>': 'file received',
        'c': 'local change or creation',
        'h': 'hard link',
        '.': 'not updated',
        '*': 'message',
        '+': None
    }

    file_type = {
        'f': 'file',
        'd': 'directory',
        'L': 'symlink',
        'D': 'device',
        'S': 'special file',
        '+': None
    }

    checksum_or_value_different = {
        'c': True,
        '.': False,
        '+': None,
        ' ': None,
        '?': None
    }

    size_different = {
        's': True,
        '.': False,
        '+': None,
        ' ': None,
        '?': None
    }

    modification_time_different = {
        't': True,
        '.': False,
        '+': None,
        ' ': None,
        '?': None
    }

    permissions_different = {
        'p': True,
        '.': False,
        '+': None,
        ' ': None,
        '?': None
    }

    owner_different = {
        'o': True,
        '.': False,
        '+': None,
        ' ': None,
        '?': None
    }

    group_different = {
        'g': True,
        '.': False,
        '+': None,
        ' ': None,
        '?': None
    }

    acl_different = {
        'a': True,
        '.': False,
        '+': None,
        ' ': None,
        '?': None
    }

    extended_attribute_different = {
        'x': True,
        '.': False,
        '+': None,
        ' ': None,
        '?': None
    }

    file_line_re = re.compile(r'(?P<meta>[<>ch.*][fdlDS][c.+ ?][s.+ ?][t.+ ?][p.+ ?][o.+ ?][g.+ ?][u.+ ?][a.+ ?][x.+ ?]) (?P<name>.+)')
    file_line_mac_re = re.compile(r'(?P<meta>[<>ch.*][fdlDS][c.+ ?][s.+ ?][t.+ ?][p.+ ?][o.+ ?][g.+ ?][x.+ ?]) (?P<name>.+)')
    stat1_line_re = re.compile(r'(sent)\s+(?P<sent>[0-9,]+)\s+(bytes)\s+(received)\s+(?P<received>[0-9,]+)\s+(bytes)\s+(?P<bytes_sec>[0-9,.]+)\s+(bytes/sec)')
    stat2_line_re = re.compile(r'(total size is)\s+(?P<total_size>[0-9,]+)\s+(speedup is)\s+(?P<speedup>[0-9,.]+)')

    stat1_line_simple_re = re.compile(r'(sent)\s+(?P<sent>[0-9,.TGMK]+)\s+(bytes)\s+(received)\s+(?P<received>[0-9,.TGMK]+)\s+(bytes)\s+(?P<bytes_sec>[0-9,.TGMK]+)\s+(bytes/sec)')
    stat2_line_simple_re = re.compile(r'(total\s+size\s+is)\s+(?P<total_size>[0-9,.TGMK]+)\s+(speedup\s+is)\s+(?P<speedup>[0-9,.TGMK]+)')

    file_line_log_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+(?P<meta>[<>ch.*][fdlDS][c.+ ?][s.+ ?][t.+ ?][p.+ ?][o.+ ?][g.+ ?][u.+ ?][a.+ ?][x.+ ?]) (?P<name>.+)')
    file_line_log_mac_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+(?P<meta>[<>ch.*][fdlDS][c.+ ?][s.+ ?][t.+ ?][p.+ ?][o.+ ?][g.+ ?][x.+ ?]) (?P<name>.+)')
    stat_line_log_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+sent\s+(?P<sent>[\d,]+)\s+bytes\s+received\s+(?P<received>[\d,]+)\s+bytes\s+total\s+size\s+(?P<total_size>[\d,]+)')

    stat1_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)]\s+total:\s+matches=(?P<matches>[\d,]+)\s+hash_hits=(?P<hash_hits>[\d,]+)\s+false_alarms=(?P<false_alarms>[\d,]+)\s+data=(?P<data>[\d,]+)')
    stat2_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+sent\s+(?P<sent>[\d,]+)\s+bytes\s+received\s+(?P<received>[\d,]+)\s+bytes\s+(?P<bytes_sec>[\d,.]+)\s+bytes/sec')
    stat3_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)]\s+total\s+size\s+is\s+(?P<total_size>[\d,]+)\s+speedup\s+is\s+(?P<speedup>[\d,.]+)')

    for line in data:
        try:
            streaming_line_input_type_check(line)
            output_line: Dict = {}

            # ignore blank lines
            if not line.strip():
                continue

            file_line = file_line_re.match(line)
            if file_line:
                filename = file_line.group('name')
                meta = file_line.group('meta')

                output_line = {
                    'type': 'file',
                    'filename': filename,
                    'metadata': meta,
                    'update_type': update_type[meta[0]],
                    'file_type': file_type[meta[1]],
                    'checksum_or_value_different': checksum_or_value_different[meta[2]],
                    'size_different': size_different[meta[3]],
                    'modification_time_different': modification_time_different[meta[4]],
                    'permissions_different': permissions_different[meta[5]],
                    'owner_different': owner_different[meta[6]],
                    'group_different': group_different[meta[7]],
                    'acl_different': acl_different[meta[9]],
                    'extended_attribute_different': extended_attribute_different[meta[10]]
                }

                yield output_line if raw else _process(output_line)
                continue

            file_line_mac = file_line_mac_re.match(line)
            if file_line_mac:
                filename = file_line_mac.group('name')
                meta = file_line_mac.group('meta')

                output_line = {
                    'type': 'file',
                    'filename': filename,
                    'metadata': meta,
                    'update_type': update_type[meta[0]],
                    'file_type': file_type[meta[1]],
                    'checksum_or_value_different': checksum_or_value_different[meta[2]],
                    'size_different': size_different[meta[3]],
                    'modification_time_different': modification_time_different[meta[4]],
                    'permissions_different': permissions_different[meta[5]],
                    'owner_different': owner_different[meta[6]],
                    'group_different': group_different[meta[7]]
                }

                yield output_line if raw else _process(output_line)
                continue

            file_line_log = file_line_log_re.match(line)
            if file_line_log:
                if process != last_process:
                    if summary:
                        yield output_line if raw else _process(output_line)
                    last_process = process
                    summary = {}

                filename = file_line_log.group('name')
                date = file_line_log.group('date')
                time = file_line_log.group('time')
                process = file_line_log.group('process')
                meta = file_line_log.group('meta')

                output_line = {
                    'type': 'file',
                    'filename': filename,
                    'date': date,
                    'time': time,
                    'process': process,
                    'metadata': meta,
                    'update_type': update_type[meta[0]],
                    'file_type': file_type[meta[1]],
                    'checksum_or_value_different': checksum_or_value_different[meta[2]],
                    'size_different': size_different[meta[3]],
                    'modification_time_different': modification_time_different[meta[4]],
                    'permissions_different': permissions_different[meta[5]],
                    'owner_different': owner_different[meta[6]],
                    'group_different': group_different[meta[7]],
                    'acl_different': acl_different[meta[9]],
                    'extended_attribute_different': extended_attribute_different[meta[10]]
                }

                yield output_line if raw else _process(output_line)
                continue

            file_line_log_mac = file_line_log_mac_re.match(line)
            if file_line_log_mac:
                if process != last_process:
                    if summary:
                        yield output_line if raw else _process(output_line)
                    last_process = process
                    summary = {}

                filename = file_line_log_mac.group('name')
                date = file_line_log_mac.group('date')
                time = file_line_log_mac.group('time')
                process = file_line_log_mac.group('process')
                meta = file_line_log_mac.group('meta')

                output_line = {
                    'type': 'file',
                    'filename': filename,
                    'date': date,
                    'time': time,
                    'process': process,
                    'metadata': meta,
                    'update_type': update_type[meta[0]],
                    'file_type': file_type[meta[1]],
                    'checksum_or_value_different': checksum_or_value_different[meta[2]],
                    'size_different': size_different[meta[3]],
                    'modification_time_different': modification_time_different[meta[4]],
                    'permissions_different': permissions_different[meta[5]],
                    'owner_different': owner_different[meta[6]],
                    'group_different': group_different[meta[7]]
                }

                yield output_line if raw else _process(output_line)
                continue

            stat1_line = stat1_line_re.match(line)
            if stat1_line:
                summary = {
                    'type': 'summary',
                    'sent': stat1_line.group('sent'),
                    'received': stat1_line.group('received'),
                    'bytes_sec': stat1_line.group('bytes_sec')
                }
                continue

            stat2_line = stat2_line_re.match(line)
            if stat2_line:
                summary['total_size'] = stat2_line.group('total_size')
                summary['speedup'] = stat2_line.group('speedup')
                continue

            stat1_line_simple = stat1_line_simple_re.match(line)
            if stat1_line_simple:
                summary = {
                    'type': 'summary',
                    'sent': stat1_line_simple.group('sent'),
                    'received': stat1_line_simple.group('received'),
                    'bytes_sec': stat1_line_simple.group('bytes_sec')
                }
                continue

            stat2_line_simple = stat2_line_simple_re.match(line)
            if stat2_line_simple:
                summary['total_size'] = stat2_line_simple.group('total_size')
                summary['speedup'] = stat2_line_simple.group('speedup')
                continue

            stat_line_log = stat_line_log_re.match(line)
            if stat_line_log:
                summary = {
                    'type': 'summary',
                    'date': stat_line_log.group('date'),
                    'time': stat_line_log.group('time'),
                    'process': stat_line_log.group('process'),
                    'sent': stat_line_log.group('sent'),
                    'received': stat_line_log.group('received'),
                    'total_size': stat_line_log.group('total_size')
                }
                continue

            stat1_line_log_v = stat1_line_log_v_re.match(line)
            if stat1_line_log_v:
                summary = {
                    'type': 'summary',
                    'date': stat1_line_log_v.group('date'),
                    'time': stat1_line_log_v.group('time'),
                    'process': stat1_line_log_v.group('process'),
                    'matches': stat1_line_log_v.group('matches'),
                    'hash_hits': stat1_line_log_v.group('hash_hits'),
                    'false_alarms': stat1_line_log_v.group('false_alarms'),
                    'data': stat1_line_log_v.group('data')
                }
                continue

            stat2_line_log_v = stat2_line_log_v_re.match(line)
            if stat2_line_log_v:
                summary['sent'] = stat2_line_log_v.group('sent')
                summary['received'] = stat2_line_log_v.group('received')
                summary['bytes_sec'] = stat2_line_log_v.group('bytes_sec')
                continue

            stat3_line_log_v = stat3_line_log_v_re.match(line)
            if stat3_line_log_v:
                summary['total_size'] = stat3_line_log_v.group('total_size')
                summary['speedup'] = stat3_line_log_v.group('speedup')
                continue

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)

    # gather final item
    try:
        if summary:
            yield summary if raw else _process(summary)

    except Exception as e:
        yield raise_or_yield(ignore_exceptions, e, '')
