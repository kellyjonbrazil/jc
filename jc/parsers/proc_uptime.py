r"""jc - JSON Convert `/proc/uptime` file parser

Usage (cli):

    $ cat /proc/uptime | jc --proc

or

    $ jc /proc/uptime

or

    $ cat /proc/uptime | jc --proc-uptime

Usage (module):

    import jc
    result = jc.parse('proc', proc_uptime_file)

or

    import jc
    result = jc.parse('proc_uptime', proc_uptime_file)

Schema:

    {
      "up_time":                    float,
      "idle_time":                  float
    }

Examples:

    $ cat /proc/uptime | jc --proc -p
    {
      "up_time": 46901.13,
      "idle_time": 46856.66
    }
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/uptime` file parser'
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

        uptime, idletime = data.split()

        raw_output = {
            'up_time': float(uptime),
            'idle_time': float(idletime)
        }

    return raw_output if raw else _process(raw_output)
