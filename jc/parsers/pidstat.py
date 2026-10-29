r"""jc - JSON Convert `pidstat -H` command output parser

Must use the `-H` (or `-h`, if `-H` is not available) option in `pidstat`.
All other `pidstat` options are supported in combination with this option.

Usage (cli):

    $ pidstat -H | jc --pidstat

or

    $ jc pidstat -H

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
        "usr_ms":           integer,
        "system_ms":        integer,
        "guest_ms":         integer,
        "command":          string
      }
    ]

Examples:

    $ pidstat -Hl | jc --pidstat -p
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

    $ pidstat -Hl | jc --pidstat -p -r
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
    version = '1.4'
    description = '`pidstat -H` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['pidstat']
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
        'time', 'uid', 'pid', 'cpu', 'vsz', 'rss', 'stksize', 'stkref',
        'usr_ms', 'system_ms', 'guest_ms'
    }

    float_list = {
        'percent_usr', 'percent_system', 'percent_guest', 'percent_cpu',
        'minflt_s', 'majflt_s', 'percent_mem', 'kb_rd_s', 'kb_wr_s',
        'kb_ccwr_s', 'cswch_s', 'nvcswch_s', 'percent_wait'
    }

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

            if key in float_list:
                entry[key] = jc.utils.convert_to_float(entry[key])

    return proc_data


# id columns: one of these is in every pidstat header
_ID_COLUMNS = {'PID', 'UID', 'TGID', 'TID', 'USER'}


def _is_header(line: str) -> bool:
    """
    True for a pidstat -h header line such as
    '#      Time   UID       PID    %usr ... Command'. Other lines that start
    with '#' (e.g. part of a command name) are not headers.
    """
    if not line.startswith('#'):
        return False

    words = line[1:].split()
    return (
        len(words) > 2
        and words[0] == 'Time'
        and words[-1] == 'Command'
        and any(w in _ID_COLUMNS for w in words)
    )


def normalize_header(header: str) -> str:
    return header.replace('#', ' ')\
                 .replace('-', '_')\
                 .replace('/', '_')\
                 .replace('%', 'percent_')\
                 .lower()


def _check_row(header: str, line: str) -> None:
    """
    The last column (Command) takes the rest of the line, so a row can have
    more fields than the header, and may have no Command at all, but it
    cannot have fewer fields than that. The Time column of `pidstat -h` is
    always an epoch integer.
    """
    fields = line.split()
    if len(fields) < len(header.split()) - 1 or not fields[0].isdecimal():
        raise ParseError('Not pidstat data')


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
    table_list: List = []
    header_found = False

    if jc.utils.has_data(data):

        for line in jc.utils.splitlines(data):
            # skip blank lines
            if not line.strip():
                continue

            if _is_header(line):
                header_found = True
                if len(table_list) > 1:
                    raw_output.extend(simple_table_parse(table_list))
                table_list = [normalize_header(line)]
                continue

            # a data row never starts with '#'
            if header_found and not line.startswith('#'):
                _check_row(table_list[0], line)
                table_list.append(line)

        if len(table_list) > 1:
            raw_output.extend(simple_table_parse(table_list))

        if not header_found:
            raise ParseError('Could not parse pidstat output. Make sure to use "pidstat -h".')

    return raw_output if raw else _process(raw_output)
