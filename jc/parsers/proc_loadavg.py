"""jc - JSON Convert `/proc/loadavg` file parser

Usage (cli):

    $ cat /proc/loadavg | jc --proc

or

    $ jc /proc/loadavg

or

    $ cat /proc/loadavg | jc --proc-loadavg

Usage (module):

    import jc
    result = jc.parse('proc', proc_loadavg_file)

or

    import jc
    result = jc.parse('proc_loadavg', proc_loadavg_file)

Schema:

All values are integers.

    {
      "load_1m":              float,
      "load_5m":              float,
      "load_15m":             float,
      "running":              integer,
      "available":            integer,
      "last_pid":             integer
    }

Examples:

    $ cat /proc/loadavg | jc --proc -p
    {
      "load_1m": 0.0,
      "load_5m": 0.01,
      "load_15m": 0.03,
      "running": 2,
      "available": 111,
      "last_pid": 2039
    }

    $ cat /proc/loadavg | jc --proc -p -r
    {
      "load_1m": "0.00",
      "load_5m": "0.01",
      "load_15m": "0.03",
      "running": "2",
      "available": "111",
      "last_pid": "2039"
    }
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/loadavg` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    float_list = {'load_1m', 'load_5m', 'load_15m'}
    int_list = {'running', 'available', 'last_pid'}

    for key in proc_data:
        if key in float_list:
            proc_data[key] = float(proc_data[key])

        if key in int_list:
            proc_data[key] = int(proc_data[key])

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}

    if jc.utils.has_data(data):

        load_1m, load_5m, load_15m, runnable, last_pid = data.split()
        running, available = runnable.split('/')

        raw_output = {
            'load_1m': load_1m,
            'load_5m': load_5m,
            'load_15m': load_15m,
            'running': running,
            'available': available,
            'last_pid': last_pid
        }

    return raw_output if raw else _process(raw_output)
