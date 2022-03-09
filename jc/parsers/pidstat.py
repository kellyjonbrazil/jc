"""jc - JSON Convert `pidstat` command output parser

Must use the `-h` option in `pidstat`.

Usage (cli):

    $ pidstat | jc --pidstat

    or

    $ jc pidstat

Usage (module):

    import jc
    result = jc.parse('pidstat', pidstat_command_output)

    or

    import jc.parsers.pidstat
    result = jc.parsers.pidstat.parse(pidstat_command_output)

Schema:

    [
      {
        "time": "1646857494",
        "uid": "1000",
        "pid": "2201",
        "percent_usr": "0.00",
        "percent_system": "0.00",
        "percent_guest": "0.00",
        "percent_cpu": "0.00",
        "cpu": "0",
        "minflt_s": "0.09",
        "majflt_s": "0.00",
        "vsz": "108328",
        "rss": "1040",
        "percent_mem": "0.03",
        "stksize": "132",
        "stkref": "20",
        "kb_rd_s": "0.00",
        "kb_wr_s": "0.00",
        "kb_ccwr_s": "0.00",
        "cswch_s": "0.00",
        "nvcswch_s": "0.00",
        "command": "pidstat -dlrsuwh"
      }
    ]

Examples:

    $ pidstat | jc --pidstat -p
    []

    $ pidstat | jc --pidstat -p -r
    []
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`pidstat` command parser'
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

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

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

        # normalize headers
        data_list[0] = data_list[0].replace('#', ' ')\
                                   .replace('/', '_')\
                                   .replace('%', 'percent_')\
                                   .lower()

        # remove remaining header lines (e.g. pidstat -h 2 5)
        data_list = [i for i in data_list if not i.startswith('#')]

        raw_output = simple_table_parse(data_list)

    return raw_output if raw else _process(raw_output)
