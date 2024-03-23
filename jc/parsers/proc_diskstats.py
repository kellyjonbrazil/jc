r"""jc - JSON Convert `/proc/diskstats` file parser

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

    $ cat /proc/diskstats | jc --proc_diskstats -p -r
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
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/diskstats` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
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

        header = (
            'maj min device reads_completed reads_merged sectors_read read_time_ms '
            'writes_completed writes_merged sectors_written write_time_ms io_in_progress '
            'io_time_ms weighted_io_time_ms discards_completed_successfully discards_merged '
            'sectors_discarded discarding_time_ms flush_requests_completed_successfully '
            'flushing_time_ms\n'
        )
        data = header + data
        cleandata = filter(None, data.splitlines())
        raw_output = simple_table_parse(cleandata)

    return raw_output if raw else _process(raw_output)
