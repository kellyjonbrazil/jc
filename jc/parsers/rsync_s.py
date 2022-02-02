"""jc - JSON CLI output utility `rsync` command output streaming parser

> This streaming parser outputs JSON Lines

<<Short rsync description and caveats>>

Usage (cli):

    $ rsync | jc --rsync-s

Usage (module):

    import jc
    # result is an iterable object (generator)
    result = jc.parse('rsync_s', rsync_command_output.splitlines())
    for item in result:
        # do something

    or

    import jc.parsers.rsync_s
    # result is an iterable object (generator)
    result = jc.parsers.rsync_s.parse(rsync_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "rsync":            string,

      # Below object only exists if using -qq or ignore_exceptions=True

      "_jc_meta":
        {
          "success":    boolean,     # false if error parsing
          "error":      string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ rsync | jc --rsync-s
    {example output}
    ...

    $ rsync | jc --rsync-s -r
    {example output}
    ...
"""
import re
from typing import Dict, Iterable
import jc.utils
from jc.utils import stream_success, stream_error
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`rsync` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
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

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float,
    # bool conversions and timestamps

    return proc_data


def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Iterable[Dict]:
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

        Iterator object
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.streaming_input_type_check(data)

    for line in data:
        output_line: Dict = {}
        summary: Dict = {}

        try:
            jc.utils.streaming_line_input_type_check(line)

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

            file_line_log = file_line_log_re.match(line)
            if file_line_log:
                filename = file_line_log.group('name')
                date = file_line_log.group('date')
                time = file_line_log.group('time')
                process = file_line_log.group('process')
                meta = file_line_log.group('meta')

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

            file_line_log_mac = file_line_log_mac_re.match(line)
            if file_line_log_mac:
                filename = file_line_log_mac.group('name')
                date = file_line_log_mac.group('date')
                time = file_line_log_mac.group('time')
                process = file_line_log_mac.group('process')
                meta = file_line_log_mac.group('meta')

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

            stat1_line = stat1_line_re.match(line)
            if stat1_line:
                summary = {
                    'sent': stat1_line.group('sent'),
                    'received': stat1_line.group('received'),
                    'bytes_sec': stat1_line.group('bytes_sec')
                }

            stat2_line = stat2_line_re.match(line)
            if stat2_line:
                summary['total_size'] = stat2_line.group('total_size')
                summary['speedup'] = stat2_line.group('speedup')

            stat_line_log = stat_line_log_re.match(line)
            if stat_line_log:
                summary = {
                    'date': stat_line_log.group('date'),
                    'time': stat_line_log.group('time'),
                    'process': stat_line_log.group('process'),
                    'sent': stat_line_log.group('sent'),
                    'received': stat_line_log.group('received'),
                    'total_size': stat_line_log.group('total_size')
                }

            stat1_line_log_v = stat1_line_log_v_re.match(line)
            if stat1_line_log_v:
                summary = {
                    'date': stat1_line_log_v.group('date'),
                    'time': stat1_line_log_v.group('time'),
                    'process': stat1_line_log_v.group('process'),
                    'matches': stat1_line_log_v.group('matches'),
                    'hash_hits': stat1_line_log_v.group('hash_hits'),
                    'false_alarms': stat1_line_log_v.group('false_alarms'),
                    'data': stat1_line_log_v.group('data')
                }

            stat2_line_log_v = stat2_line_log_v_re.match(line)
            if stat2_line_log_v:
                summary['sent'] = stat2_line_log_v.group('sent')
                summary['received'] = stat2_line_log_v.group('received')
                summary['bytes_sec'] = stat2_line_log_v.group('bytes_sec')

            stat3_line_log_v = stat3_line_log_v_re.match(line)
            if stat3_line_log_v:
                summary['total_size'] = stat3_line_log_v.group('total_size')
                summary['speedup'] = stat3_line_log_v.group('speedup')

            if output_line:
                yield stream_success(output_line, ignore_exceptions) if raw else stream_success(_process(output_line), ignore_exceptions)
            else:
                continue

        except Exception as e:
            yield stream_error(e, ignore_exceptions, line)
