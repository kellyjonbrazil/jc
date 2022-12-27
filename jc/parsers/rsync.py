"""jc - JSON Convert `rsync` command output parser

Supports the `-i` or `--itemize-changes` options with all levels of
verbosity. This parser will process the `STDOUT` output or a log file
generated with the `--log-file` option.

Usage (cli):

    $ rsync -i -a source/ dest | jc --rsync

or

    $ jc rsync -i -a source/ dest

or

    $ cat rsync-backup.log | jc --rsync

Usage (module):

    import jc
    result = jc.parse('rsync', rsync_command_output)

Schema:

    [
      {
        "summary": {
          "date":                             string,
          "time":                             string,
          "process":                          integer,
          "sent":                             integer,
          "received":                         integer,
          "total_size":                       integer,
          "matches":                          integer,
          "hash_hits":                        integer,
          "false_alarms":                     integer,
          "data":                             integer,
          "bytes_sec":                        float,
          "speedup":                          float
        },
        "files": [
          {
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
          }
        ]
      }
    ]

    [0] 'file sent', 'file received', 'local change or creation',
        'hard link', 'not updated', 'message'
    [1] 'file', 'directory', 'symlink', 'device', 'special file'
    [2] naive timestamp if time and date fields exist and can be converted.

Examples:

    $ rsync -i -a source/ dest | jc --rsync -p
    [
      {
        "summary": {
          "sent": 1708,
          "received": 8209,
          "bytes_sec": 19834.0,
          "total_size": 235,
          "speedup": 0.02
        },
        "files": [
          {
            "filename": "./",
            "metadata": ".d..t......",
            "update_type": "not updated",
            "file_type": "directory",
            "checksum_or_value_different": false,
            "size_different": false,
            "modification_time_different": true,
            "permissions_different": false,
            "owner_different": false,
            "group_different": false,
            "acl_different": false,
            "extended_attribute_different": false
          },
          ...
        ]
      }
    ]

    $ rsync | jc --rsync -p -r
    [
      {
        "summary": {
          "sent": "1,708",
          "received": "8,209",
          "bytes_sec": "19,834.00",
          "total_size": "235",
          "speedup": "0.02"
        },
        "files": [
          {
            "filename": "./",
            "metadata": ".d..t......",
            "update_type": "not updated",
            "file_type": "directory",
            "checksum_or_value_different": false,
            "size_different": false,
            "modification_time_different": true,
            "permissions_different": false,
            "owner_different": false,
            "group_different": false,
            "acl_different": false,
            "extended_attribute_different": false
          },
          ...
        ]
      }
    ]
"""
import re
from copy import deepcopy
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`rsync` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['rsync -i', 'rsync --itemize-changes']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {
        'process', 'sent', 'received', 'total_size', 'matches', 'hash_hits',
        'false_alarms', 'data'
    }

    float_list = {'bytes_sec', 'speedup'}

    for item in proc_data:
        for key in item['summary']:
            if key in int_list:
                item['summary'][key] = jc.utils.convert_to_int(item['summary'][key])

            if key in float_list:
                item['summary'][key] = jc.utils.convert_to_float(item['summary'][key])

        for entry in item['files']:
            for key in entry:
                if key in int_list:
                    entry[key] = jc.utils.convert_to_int(entry[key])

            # add timestamp
            if 'date' in entry and 'time' in entry:
                date = entry['date'].replace('/', '-')
                date_time = f'{date} {entry["time"]}'
                ts = jc.utils.timestamp(date_time, format_hint=(7250,))
                entry['epoch'] = ts.naive

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

    rsync_run_new: Dict = {
        'summary': {},
        'files': []
    }

    rsync_run = deepcopy(rsync_run_new)

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

    file_line_log_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+(?P<meta>[<>ch.*][fdlDS][c.+ ?][s.+ ?][t.+ ?][p.+ ?][o.+ ?][g.+ ?][u.+ ?][a.+ ?][x.+ ?]) (?P<name>.+)')
    file_line_log_mac_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+(?P<meta>[<>ch.*][fdlDS][c.+ ?][s.+ ?][t.+ ?][p.+ ?][o.+ ?][g.+ ?][x.+ ?]) (?P<name>.+)')
    stat_line_log_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+sent\s+(?P<sent>[\d,]+)\s+bytes\s+received\s+(?P<received>[\d,]+)\s+bytes\s+total\s+size\s+(?P<total_size>[\d,]+)')

    stat1_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)]\s+total:\s+matches=(?P<matches>[\d,]+)\s+hash_hits=(?P<hash_hits>[\d,]+)\s+false_alarms=(?P<false_alarms>[\d,]+)\s+data=(?P<data>[\d,]+)')
    stat2_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)\]\s+sent\s+(?P<sent>[\d,]+)\s+bytes\s+received\s+(?P<received>[\d,]+)\s+bytes\s+(?P<bytes_sec>[\d,.]+)\s+bytes/sec')
    stat3_line_log_v_re = re.compile(r'(?P<date>\d\d\d\d/\d\d/\d\d)\s+(?P<time>\d\d:\d\d:\d\d)\s+\[(?P<process>\d+)]\s+total\s+size\s+is\s+(?P<total_size>[\d,]+)\s+speedup\s+is\s+(?P<speedup>[\d,.]+)')

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):

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
                    'acl_different': acl_different[meta[9]],
                    'extended_attribute_different': extended_attribute_different[meta[10]]
                }

                rsync_run['files'].append(output_line)
                continue

            file_line_mac = file_line_mac_re.match(line)
            if file_line_mac:
                filename = file_line_mac.group('name')
                meta = file_line_mac.group('meta')

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
                    'group_different': group_different[meta[7]]
                }

                rsync_run['files'].append(output_line)
                continue

            file_line_log = file_line_log_re.match(line)
            if file_line_log:
                filename = file_line_log.group('name')
                date = file_line_log.group('date')
                time = file_line_log.group('time')
                process = file_line_log.group('process')
                meta = file_line_log.group('meta')

                if process != last_process:
                    raw_output.append(rsync_run)
                    rsync_run = deepcopy(rsync_run_new)
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
                    'acl_different': acl_different[meta[9]],
                    'extended_attribute_different': extended_attribute_different[meta[10]]
                }
                rsync_run['files'].append(output_line)
                continue

            file_line_log_mac = file_line_log_mac_re.match(line)
            if file_line_log_mac:
                filename = file_line_log_mac.group('name')
                date = file_line_log_mac.group('date')
                time = file_line_log_mac.group('time')
                process = file_line_log_mac.group('process')
                meta = file_line_log_mac.group('meta')

                if process != last_process:
                    raw_output.append(rsync_run)
                    rsync_run = deepcopy(rsync_run_new)
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
                    'group_different': group_different[meta[7]]
                }
                rsync_run['files'].append(output_line)
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

            stat1_line_log_v = stat1_line_log_v_re.match(line)
            if stat1_line_log_v:
                rsync_run['summary'] = {
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
                rsync_run['summary']['sent'] = stat2_line_log_v.group('sent')
                rsync_run['summary']['received'] = stat2_line_log_v.group('received')
                rsync_run['summary']['bytes_sec'] = stat2_line_log_v.group('bytes_sec')
                continue

            stat3_line_log_v = stat3_line_log_v_re.match(line)
            if stat3_line_log_v:
                rsync_run['summary']['total_size'] = stat3_line_log_v.group('total_size')
                rsync_run['summary']['speedup'] = stat3_line_log_v.group('speedup')
                continue

    raw_output.append(rsync_run)

    # cleanup blank entries
    raw_output = [run for run in raw_output if run != rsync_run_new]

    return raw_output if raw else _process(raw_output)
