"""jc - JSON Convert `/proc/diskstats` file parser

Usage (cli):

    $ cat /proc/diskstats | jc --proc

or

    $ jc /proc/diskstats

or

    $ cat /proc/diskstats | jc --proc-diskstats

Usage (module):

    import jc
    result = jc.parse('proc', proc_diskstats_file)

or

    import jc
    result = jc.parse('proc_diskstats', proc_diskstats_file)

Schema:

    [
      {
        "maj":                                          integer,
        "min":                                          integer,
        "device":                                       string,
        "reads_completed":                              integer,
        "reads_merged":                                 integer,
        "sectors_read":                                 integer,
        "read_time_ms":                                 integer,
        "writes_completed":                             integer,
        "writes_merged":                                integer,
        "sectors_written":                              integer,
        "write_time_ms":                                integer,
        "io_in_progress":                               integer,
        "io_time_ms":                                   integer,
        "weighted_io_time_ms":                          integer,
        "discards_completed_successfully":              integer,
        "discards_merged":                              integer,
        "sectors_discarded":                            integer,
        "discarding_time_ms":                           integer,
        "flush_requests_completed_successfully":        integer,
        "flushing_time_ms":                             integer
      }
    ]

Examples:

    $ cat /proc/diskstats | jc --proc -p
    [
      {
        "maj": 7,
        "min": 0,
        "device": "loop0",
        "reads_completed": 48,
        "reads_merged": 0,
        "sectors_read": 718,
        "read_time_ms": 19,
        "writes_completed": 0,
        "writes_merged": 0,
        "sectors_written": 0,
        "write_time_ms": 0,
        "io_in_progress": 0,
        "io_time_ms": 36,
        "weighted_io_time_ms": 19,
        "discards_completed_successfully": 0,
        "discards_merged": 0,
        "sectors_discarded": 0,
        "discarding_time_ms": 0,
        "flush_requests_completed_successfully": 0,
        "flushing_time_ms": 0
      },
      {
        "maj": 7,
        "min": 1,
        "device": "loop1",
        "reads_completed": 41,
        "reads_merged": 0,
        "sectors_read": 688,
        "read_time_ms": 17,
        "writes_completed": 0,
        "writes_merged": 0,
        "sectors_written": 0,
        "write_time_ms": 0,
        "io_in_progress": 0,
        "io_time_ms": 28,
        "weighted_io_time_ms": 17,
        "discards_completed_successfully": 0,
        "discards_merged": 0,
        "sectors_discarded": 0,
        "discarding_time_ms": 0,
        "flush_requests_completed_successfully": 0,
        "flushing_time_ms": 0
      },
      ...
    ]

    $ proc_diskstats | jc --proc_diskstats -p -r
    [
      {
        "maj": "7",
        "min": "0",
        "device": "loop0",
        "reads_completed": "48",
        "reads_merged": "0",
        "sectors_read": "718",
        "read_time_ms": "19",
        "writes_completed": "0",
        "writes_merged": "0",
        "sectors_written": "0",
        "write_time_ms": "0",
        "io_in_progress": "0",
        "io_time_ms": "36",
        "weighted_io_time_ms": "19",
        "discards_completed_successfully": "0",
        "discards_merged": "0",
        "sectors_discarded": "0",
        "discarding_time_ms": "0",
        "flush_requests_completed_successfully": "0",
        "flushing_time_ms": "0"
      },
      {
        "maj": "7",
        "min": "1",
        "device": "loop1",
        "reads_completed": "41",
        "reads_merged": "0",
        "sectors_read": "688",
        "read_time_ms": "17",
        "writes_completed": "0",
        "writes_merged": "0",
        "sectors_written": "0",
        "write_time_ms": "0",
        "io_in_progress": "0",
        "io_time_ms": "28",
        "weighted_io_time_ms": "17",
        "discards_completed_successfully": "0",
        "discards_merged": "0",
        "sectors_discarded": "0",
        "discarding_time_ms": "0",
        "flush_requests_completed_successfully": "0",
        "flushing_time_ms": "0"
      },
      {
        "maj": "7",
        "min": "2",
        "device": "loop2",
        "reads_completed": "119",
        "reads_merged": "0",
        "sectors_read": "2956",
        "read_time_ms": "18",
        "writes_completed": "0",
        "writes_merged": "0",
        "sectors_written": "0",
        "write_time_ms": "0",
        "io_in_progress": "0",
        "io_time_ms": "56",
        "weighted_io_time_ms": "18",
        "discards_completed_successfully": "0",
        "discards_merged": "0",
        "sectors_discarded": "0",
        "discarding_time_ms": "0",
        "flush_requests_completed_successfully": "0",
        "flushing_time_ms": "0"
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/diskstats` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for entry in proc_data:
        for key in entry:
            if key != 'device':
                entry[key] = int(entry[key])

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

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            split_line = line.split()

            output_line = {
                'maj': split_line[0],
                'min': split_line[1],
                'device': split_line[2],
                'reads_completed': split_line[3],
                'reads_merged': split_line[4],
                'sectors_read': split_line[5],
                'read_time_ms': split_line[6],
                'writes_completed': split_line[7],
                'writes_merged': split_line[8],
                'sectors_written': split_line[9],
                'write_time_ms': split_line[10],
                'io_in_progress': split_line[11],
                'io_time_ms': split_line[12],
                'weighted_io_time_ms': split_line[13]
            }

            if len(split_line) > 14:
                output_line['discards_completed_successfully'] = split_line[14]
                output_line['discards_merged'] = split_line[15]
                output_line['sectors_discarded'] = split_line[16]
                output_line['discarding_time_ms'] = split_line[17]

            if len(split_line) > 18:
                output_line['flush_requests_completed_successfully'] = split_line[18]
                output_line['flushing_time_ms'] = split_line[19]

            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
