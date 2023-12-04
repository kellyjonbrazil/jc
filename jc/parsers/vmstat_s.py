"""jc - JSON Convert `vmstat` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Options supported: `-a`, `-w`, `-d`, `-t`

The `epoch` calculated timestamp field is naive. (i.e. based on the local
time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the timezone field is UTC.

Usage (cli):

    $ vmstat | jc --vmstat-s

> Note: When piping `jc` converted `vmstat` output to other processes it may
> appear the output is hanging due to the OS pipe buffers. This is because
> `vmstat` output is too small to quickly fill up the buffer. Use the `-u`
> option to unbuffer the `jc` output if you would like immediate output. See
> the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output)
> for more information.

Usage (module):

    import jc

    result = jc.parse('vmstat_s', vmstat_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "runnable_procs":                   integer,
      "uninterruptible_sleeping_procs":   integer,
      "virtual_mem_used":                 integer,
      "free_mem":                         integer,
      "buffer_mem":                       integer,
      "cache_mem":                        integer,
      "inactive_mem":                     integer,
      "active_mem":                       integer,
      "swap_in":                          integer,
      "swap_out":                         integer,
      "blocks_in":                        integer,
      "blocks_out":                       integer,
      "interrupts":                       integer,
      "context_switches":                 integer,
      "user_time":                        integer,
      "system_time":                      integer,
      "idle_time":                        integer,
      "io_wait_time":                     integer,
      "stolen_time":                      integer,
      "disk":                             string,
      "total_reads":                      integer,
      "merged_reads":                     integer,
      "sectors_read":                     integer,
      "reading_ms":                       integer,
      "total_writes":                     integer,
      "merged_writes":                    integer,
      "sectors_written":                  integer,
      "writing_ms":                       integer,
      "current_io":                       integer,
      "io_seconds":                       integer,
      "timestamp":                        string,
      "timezone":                         string,
      "epoch":                            integer,     # [0]
      "epoch_utc":                        integer      # [1]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":                        boolean,     # [2]
        "error":                          string,      # [3]
        "line":                           string       # [3]
      }
    }

    [0] naive timestamp if -t flag is used
    [1] aware timestamp if -t flag is used and UTC TZ
    [2] false if error parsing
    [3] exists if "success" is false

Examples:

    $ vmstat | jc --vmstat-s
    {"runnable_procs":2,"uninterruptible_sleeping_procs":0,"virtual_mem...}
    ...

    $ vmstat | jc --vmstat-s -r
    {"runnable_procs":"2","uninterruptible_sleeping_procs":"0","virtua...}
    ...
"""
import re
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError

PROCS_HEADER_RE = re.compile(r'^-*procs-* ')
DISK_HEADER_RE = re.compile(r'^-*disk-* ')


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`vmstat` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['command']
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
    int_list = {
        'runnable_procs', 'uninterruptible_sleeping_procs', 'virtual_mem_used', 'free_mem',
        'buffer_mem', 'cache_mem', 'inactive_mem', 'active_mem', 'swap_in', 'swap_out', 'blocks_in',
        'blocks_out', 'interrupts', 'context_switches', 'user_time', 'system_time', 'idle_time',
        'io_wait_time', 'stolen_time', 'total_reads', 'merged_reads', 'sectors_read', 'reading_ms',
        'total_writes', 'merged_writes', 'sectors_written', 'writing_ms', 'current_io', 'io_seconds'
    }

    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

    if proc_data['timestamp']:
        fmt_hint = (7250, 7255)
        ts = jc.utils.timestamp(f'{proc_data["timestamp"]} {proc_data["timezone"]}', format_hint=fmt_hint)
        proc_data['epoch'] = ts.naive
        proc_data['epoch_utc'] = ts.utc

    return proc_data


@add_jc_meta
def parse(data, raw=False, quiet=False, ignore_exceptions=False):
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

    procs = None
    buff_cache = None
    disk = None
    tstamp = None
    tz = None

    for line in data:
        try:
            streaming_line_input_type_check(line)
            output_line = {}

            # skip blank lines
            if not line.strip():
                continue

            # detect output type
            if not procs and not disk and PROCS_HEADER_RE.match(line):
                procs = True
                tstamp = '-timestamp-' in line
                continue

            if not procs and not disk and DISK_HEADER_RE.match(line):
                disk = True
                tstamp = '-timestamp-' in line
                continue

            # skip header rows
            if (procs or disk) and (PROCS_HEADER_RE.match(line) or DISK_HEADER_RE.match(line)):
                continue

            if 'swpd' in line and 'free' in line and 'buff' in line and 'cache' in line:
                buff_cache = True
                tz = line.strip().split()[-1] if tstamp else None
                continue

            if 'swpd' in line and 'free' in line and 'inact' in line and 'active' in line:
                buff_cache = False
                tz = line.strip().split()[-1] if tstamp else None
                continue

            if 'total' in line and 'merged' in line and 'sectors' in line:
                tz = line.strip().split()[-1] if tstamp else None
                continue

            # line parsing
            if procs:
                line_list = line.strip().split(maxsplit=17)

                output_line = {
                    'runnable_procs': line_list[0],
                    'uninterruptible_sleeping_procs': line_list[1],
                    'virtual_mem_used': line_list[2],
                    'free_mem': line_list[3],
                    'buffer_mem': line_list[4] if buff_cache else None,
                    'cache_mem': line_list[5] if buff_cache else None,
                    'inactive_mem': line_list[4] if not buff_cache else None,
                    'active_mem': line_list[5] if not buff_cache else None,
                    'swap_in': line_list[6],
                    'swap_out': line_list[7],
                    'blocks_in': line_list[8],
                    'blocks_out': line_list[9],
                    'interrupts': line_list[10],
                    'context_switches': line_list[11],
                    'user_time': line_list[12],
                    'system_time': line_list[13],
                    'idle_time': line_list[14],
                    'io_wait_time': line_list[15],
                    'stolen_time': line_list[16],
                    'timestamp': line_list[17] if tstamp else None,
                    'timezone': tz or None
                }

            if disk:
                line_list = line.strip().split(maxsplit=11)

                output_line = {
                    'disk': line_list[0],
                    'total_reads': line_list[1],
                    'merged_reads': line_list[2],
                    'sectors_read': line_list[3],
                    'reading_ms': line_list[4],
                    'total_writes': line_list[5],
                    'merged_writes': line_list[6],
                    'sectors_written': line_list[7],
                    'writing_ms': line_list[8],
                    'current_io': line_list[9],
                    'io_seconds': line_list[10],
                    'timestamp': line_list[11] if tstamp else None,
                    'timezone': tz or None
                }

            if output_line:
                yield output_line if raw else _process(output_line)
            else:
                raise ParseError('Not vmstat data')

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
