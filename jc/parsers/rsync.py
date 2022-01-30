"""jc - JSON CLI output utility `rsync` command output parser

Supports the `-i` or `--itemize-changes` option with all levels of
verbosity.

Usage (cli):

    $ rsync -i -a source/ dest | jc --rsync

    or

    $ jc rsync -i -a source/ dest

Usage (module):

    import jc
    result = jc.parse('rsync', rsync_command_output)

    or

    import jc.parsers.rsync
    result = jc.parsers.rsync.parse(rsync_command_output)

Schema:

    [
      {
        "summary": {
          "date":                           string,
          "time":                           string,
          "process":                        integer,     # need to convert
          "sent":                           integer,     # need to convert
          "received":                       integer,     # need to convert
          "total_size":                     integer      # need to convert
        },
        "items": [
          "filename":                       string,
          "metadata":                       string,
          "update_type":                    string/null,
          "file_type":                      string/null,
          "checksum_or_value_different":    bool/null,
          "size_different":                 bool/null,
          "modification_time_different":    bool/null,
          "permissions_different":          bool/null,
          "owner_different":                bool/null,
          "group_different":                bool/null,
          "future":                         null,
          "acl_different":                  bool/null,
          "extended_attribute_different":   bool/null,
          "sent":                           integer,     # need to convert
          "received":                       integer,     # need to convert
          "bytes_sec":                      float,       # need to convert
          "total_size":                     integer,     # need to convert
          "speedup":                        float,       # need to convert
        ]
      }
    ]

Examples:

    $ rsync | jc --rsync -p
    []

    $ rsync | jc --rsync -p -r
    []
"""
import re
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`rsync` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'freebsd']
    magic_commands = ['rsync -i', 'rsync --itemize-changes']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    # int_list = ['sent', 'received', 'total_size']
    # float_list = ['bytes_sec', 'speedup']
    # for entry in proc_data:
    #     for key in entry:
    #         if key in int_list:
    #             entry[key] = jc.utils.convert_to_int(entry[key])
    #         if key in float_list:
    #             entry[key] = jc.utils.convert_to_float(entry[key])

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []
    rsync_run: Dict = {}

    last_process = ''

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
        '+': None
    }

    size_different = {
        's': True,
        '.': False,
        '+': None
    }

    modification_time_different = {
        't': True,
        '.': False,
        '+': None
    }

    permissions_different = {
        'p': True,
        '.': False,
        '+': None
    }

    owner_different = {
        'o': True,
        '.': False,
        '+': None
    }

    group_different = {
        'g': True,
        '.': False,
        '+': None
    }

    future = None

    acl_different = {
        'a': True,
        '.': False,
        '+': None
    }

    extended_attribute_different = {
        'x': True,
        '.': False,
        '+': None
    }

    if jc.utils.has_data(data):
        rsync_run.update({
            'summary': {},
            'items': []
        })

        file_line_re = re.compile(r'(?P<meta>[<>ch.*][fdlDS][c.+][s.+][t.+][p.+][o.+][g.+][u.+][a.+][x.+]) (?P<name>.+)')
        stat1_line_re = re.compile(r'(sent)\s+(?P<sent>[0-9,]+)\s+(bytes)\s+(received)\s+(?P<received>[0-9,]+)\s+(bytes)\s+(?P<bytes_sec>[0-9,.]+)\s+(bytes/sec)')
        stat2_line_re = re.compile(r'(total size is)\s+(?P<total_size>[0-9,]+)\s+(speedup is)\s+(?P<speedup>[0-9,.]+)')

        file_line_log_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+(?P<meta>[<>ch.*][fdlDS][c.+][s.+][t.+][p.+][o.+][g.+][u.+][a.+][x.+])\s+(?P<name>.+)')
        stat_line_log_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+sent\s+(?P<sent>[\d,]+)\s+bytes\s+received\s+(?P<received>[\d,]+)\s+bytes\s+total\s+size\s+(?P<total_size>[\d,]+)')

        stat1_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)]\s+total:\s+matches=(?P<matches>[\d,]+)\s+hash_hits=(?P<hash_hits>[\d,]+)\s+false_alarms=(?P<false_alarms>[\d,]+)\s+data=(?P<data>[\d,]+)')
        stat2_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+sent\s+(?P<sent>[\d,]+)\s+bytes\s+received\s+(?P<received>[\d,]+)\s+bytes\s+(?P<bytes_sec>[\d,.]+)\s+bytes/sec')
        stat3_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)]\s+total\s+size\s+is\s+(?P<total_size>[\d,]+)\s+speedup\s+is\s+(?P<speedup>[\d,.]+)')

        for line in filter(None, data.splitlines()):

            stat1_line_log_v = stat1_line_log_v_re.match(line)
            stat2_line_log_v = stat2_line_log_v_re.match(line)
            stat3_line_log_v = stat3_line_log_v_re.match(line)

            file_line = file_line_re.match(line)
            if file_line:
                filename = file_line.group('name')
                meta = file_line.group('meta')

                output_line = {
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
                    'future': future,
                    'acl_different': acl_different[meta[9]],
                    'extended_attribute_different': extended_attribute_different[meta[10]]
                }

                rsync_run['items'].append(output_line)
                continue

            file_line_log = file_line_log_re.match(line)
            if file_line_log:
                filename = file_line_log.group('name')
                date = file_line_log.group('date')
                time = file_line_log.group('time')
                process = file_line_log.group('process')
                meta = file_line_log.group('meta')

                if process != last_process:
                    if rsync_run:
                        raw_output.append(rsync_run)
                        rsync_run = {
                            'summary': {},
                            'items': []
                        }
                        last_process = process

                output_line = {
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
                    'future': future,
                    'acl_different': acl_different[meta[9]],
                    'extended_attribute_different': extended_attribute_different[meta[10]]
                }

                rsync_run['items'].append(output_line)
                continue

            stat1_line = stat1_line_re.match(line)
            if stat1_line:
                rsync_run['summary'] = {
                    'sent': stat1_line.group('sent'),
                    'received': stat1_line.group('received'),
                    'bytes_sec': stat1_line.group('bytes_sec')
                }
                continue

            stat2_line = stat2_line_re.match(line)
            if stat2_line:
                rsync_run['summary']['total_size'] = stat2_line.group('total_size')
                rsync_run['summary']['speedup'] = stat2_line.group('speedup')
                continue

            stat_line_log = stat_line_log_re.match(line)
            if stat_line_log:
                rsync_run['summary'] = {
                    'date': stat_line_log.group('date'),
                    'time': stat_line_log.group('time'),
                    'process': stat_line_log.group('process'),
                    'sent': stat_line_log.group('sent'),
                    'received': stat_line_log.group('received'),
                    'total_size': stat_line_log.group('total_size')
                }
                continue

    if rsync_run:
        raw_output.append(rsync_run)

    return raw_output if raw else _process(raw_output)
