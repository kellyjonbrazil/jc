r"""jc - JSON Convert `upsc` command output parser

Parses the output of the `upsc` command from Network UPS Tools (NUT).
The command queries a UPS device and returns key-value pairs representing
its current state. Values that are numeric are converted to the appropriate
type (int or float) in processed output.

Usage (cli):

    $ upsc ups@localhost | jc --upsc

or

    $ jc upsc ups@localhost

Usage (module):

    import jc
    result = jc.parse('upsc', upsc_command_output)

Schema:

    [
      {
        "name":     string,
        "value":    string
      }
    ]

Examples:

    $ upsc ups@localhost | jc --upsc -p
    [
      {
        "name": "battery.charge",
        "value": 100
      },
      {
        "name": "battery.runtime",
        "value": 4530
      },
      {
        "name": "battery.voltage",
        "value": 24.0
      },
      {
        "name": "ups.status",
        "value": "OL"
      },
      ...
    ]

    $ upsc ups@localhost | jc --upsc -p -r
    [
      {
        "name": "battery.charge",
        "value": "100"
      },
      {
        "name": "ups.status",
        "value": "OL"
      },
      ...
    ]
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`upsc` command parser (NUT - Network UPS Tools)'
    author = 'AYUSHPALLAV1'
    author_email = ''
    # details = 'Parses upsc output from Network UPS Tools (NUT)'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']

    # tags options: generic, standard, file, string, binary, command, slurpable
    tags = ['command']
    magic_commands = ['upsc']


__version__ = info.version


def _try_convert(value: str):
    """
    Attempt to convert a string value to int or float.
    Returns the original string if conversion is not possible.
    """
    try:
        int_val = int(value)
        return int_val
    except ValueError:
        pass

    try:
        float_val = float(value)
        return float_val
    except ValueError:
        pass

    return value


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    processed = []
    for entry in proc_data:
        proc_entry = {
            'name': entry['name'],
            'value': _try_convert(entry['value'])
        }
        processed.append(proc_entry)

    return processed


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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

    raw_output: List[Dict] = []

    if jc.utils.has_data(data):

        for line in data.splitlines():
            line = line.strip()

            # skip empty lines and lines that don't contain a colon separator
            if not line or ': ' not in line:
                continue

            # upsc output format: "key.name: value"
            name, _, value = line.partition(': ')
            name = name.strip()
            value = value.strip()

            if name:
                raw_output.append({
                    'name': name,
                    'value': value
                })

    return raw_output if raw else _process(raw_output)
