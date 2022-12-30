"""jc - JSON Convert `/proc/<pid>/statm` file parser

Usage (cli):

    $ cat /proc/1/statm | jc --proc

or

    $ jc /proc/1/statm

or

    $ cat /proc/1/statm | jc --proc-pid-statm

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_statm_file)

or

    import jc
    result = jc.parse('proc_pid_statm', proc_pid_statm_file)

Schema:

    {
      "size":                   integer,
      "resident":               integer,
      "shared":                 integer,
      "text":                   integer,
      "lib":                    integer,
      "data":                   integer,
      "dt":                     integer
    }

Examples:

    $ cat /proc/1/statm | jc --proc -p
    {
      "size": 42496,
      "resident": 3313,
      "shared": 2169,
      "text": 202,
      "lib": 0,
      "data": 5180,
      "dt": 0
    }
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/<pid>/statm` file parser'
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

        size, resident, shared, text, lib, data_, dt = data.split()

        raw_output = {
            'size': int(size),
            'resident': int(resident),
            'shared': int(shared),
            'text': int(text),
            'lib': int(lib),
            'data': int(data_),
            'dt': int(dt)
        }

    return raw_output if raw else _process(raw_output)
