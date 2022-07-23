"""jc - JSON Convert `pidstat -h` command output parser

Must use the `-h` option in `pidstat`. All other `pidstat` options are
supported in combination with `-h`.

Usage (cli):

    $ pidstat -h | jc --pidstat

    or

    $ jc pidstat -h

Usage (module):

    import jc
    result = jc.parse('pidstat', pidstat_command_output)

Schema:

    [
      {
        "time":             integer,
        "uid":              integer,
        "pid":              integer,
        "percent_usr":      float,
        "percent_system":   float,
        "percent_guest":    float,
        "percent_cpu":      float,
        "cpu":              integer,
        "minflt_s":         float,
        "majflt_s":         float,
        "vsz":              integer,
        "rss":              integer,
        "percent_mem":      float,
        "stksize":          integer,
        "stkref":           integer,
        "kb_rd_s":          float,
        "kb_wr_s":          float,
        "kb_ccwr_s":        float,
        "cswch_s":          float,
        "nvcswch_s":        float,
        "command":          string
      }
    ]

Examples:

    $ pidstat -hl | jc --pidstat -p
    [
      {
        "time": 1646859134,
        "uid": 0,
        "pid": 1,
        "percent_usr": 0.0,
        "percent_system": 0.03,
        "percent_guest": 0.0,
        "percent_cpu": 0.03,
        "cpu": 0,
        "command": "/usr/lib/systemd/systemd --switched-root --system..."
      },
      {
        "time": 1646859134,
        "uid": 0,
        "pid": 6,
        "percent_usr": 0.0,
        "percent_system": 0.0,
        "percent_guest": 0.0,
        "percent_cpu": 0.0,
        "cpu": 0,
        "command": "ksoftirqd/0"
      },
      {
        "time": 1646859134,
        "uid": 0,
        "pid": 2263,
        "percent_usr": 0.0,
        "percent_system": 0.0,
        "percent_guest": 0.0,
        "percent_cpu": 0.0,
        "cpu": 0,
        "command": "kworker/0:0"
      }
    ]

    $ pidstat -hl | jc --pidstat -p -r
    [
      {
        "time": "1646859134",
        "uid": "0",
        "pid": "1",
        "percent_usr": "0.00",
        "percent_system": "0.03",
        "percent_guest": "0.00",
        "percent_cpu": "0.03",
        "cpu": "0",
        "command": "/usr/lib/systemd/systemd --switched-root --system..."
      },
      {
        "time": "1646859134",
        "uid": "0",
        "pid": "6",
        "percent_usr": "0.00",
        "percent_system": "0.00",
        "percent_guest": "0.00",
        "percent_cpu": "0.00",
        "cpu": "0",
        "command": "ksoftirqd/0"
      },
      {
        "time": "1646859134",
        "uid": "0",
        "pid": "2263",
        "percent_usr": "0.00",
        "percent_system": "0.00",
        "percent_guest": "0.00",
        "percent_cpu": "0.00",
        "cpu": "0",
        "command": "kworker/0:0"
      }
    ]
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`pidstat -h` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['pidstat']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'time', 'uid', 'pid', 'cpu', 'vsz', 'rss', 'stksize', 'stkref'}

    float_list = {'percent_usr', 'percent_system', 'percent_guest', 'percent_cpu',
                  'minflt_s', 'majflt_s', 'percent_mem', 'kb_rd_s', 'kb_wr_s',
                  'kb_ccwr_s', 'cswch_s', 'nvcswch_s'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

            if key in float_list:
                entry[key] = jc.utils.convert_to_float(entry[key])

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

        # check for line starting with # as the start of the table
        data_list = list(filter(None, data.splitlines()))
        for line in data_list.copy():
            if line.startswith('#'):
                break
            else:
                data_list.pop(0)

        if not data_list:
            raise ParseError('Could not parse pidstat output. Make sure to use "pidstat -h".')

        # normalize header
        data_list[0] = data_list[0].replace('#', ' ')\
                                   .replace('/', '_')\
                                   .replace('%', 'percent_')\
                                   .lower()

        # remove remaining header lines (e.g. pidstat -h 2 5)
        data_list = [i for i in data_list if not i.startswith('#')]

        raw_output = simple_table_parse(data_list)

    return raw_output if raw else _process(raw_output)
