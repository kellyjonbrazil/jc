"""jc - JSON CLI output utility `vmstat` command output parser

<<Short vmstat description and caveats>>

Usage (cli):

    $ vmstat | jc --vmstat

    or

    $ jc vmstat

Usage (module):

    import jc.parsers.vmstat
    result = jc.parsers.vmstat.parse(vmstat_command_output)

Schema:

    [
      {
        "vmstat":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ vmstat | jc --vmstat -p
    []

    $ vmstat | jc --vmstat -p -r
    []
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`vmstat` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['vmstat']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool conversions and timestamps

    # add epoch and epoch_utc when timestamp field is not null

    return proc_data


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

    raw_output = []
    output_line = {}
    procs = None
    buff_cache = None
    disk = None
    tstamp = None
    tz = None

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            # detect output type
            if not procs and not disk and line.startswith('procs'):
                procs = True
                tstamp = True if '-timestamp-' in line else False
                continue

            if not procs and not disk and line.startswith('disk'):
                disk = True
                tstamp = True if '-timestamp-' in line else False
                continue


            # skip header rows
            if 'swpd' in line and 'free' in line and 'buff' in line and  'cache' in line:
                buff_cache = True
                tz = line.strip().split()[-1] if tstamp else None
                continue

            elif 'swpd' in line and 'free' in line and 'inact' in line and  'active' in line:
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
                    'timestamp': line_list[17] if tstamp else None
                }

                raw_output.append(output_line)

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
                    'timestamp': line_list[11] if tstamp else None
                }

                raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
