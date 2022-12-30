"""jc - JSON Convert `/proc/consoles` file parser

Usage (cli):

    $ cat /proc/consoles | jc --proc

or

    $ jc /proc/consoles

or

    $ cat /proc/consoles | jc --proc-consoles

Usage (module):

    import jc
    result = jc.parse('proc', proc_consoles_file)

or

    import jc
    result = jc.parse('proc_consoles', proc_consoles_file)

Schema:

    [
      {
        "device":                     string,
        "operations":                 string,
        "operations_list": [
                                      string  # [0]
        ],
        "flags":                      string,
        "flags_list": [
                                      string  # [1]
        ],
        "major":                      integer,
        "minor":                      integer
      }
    ]

    [0] Values: read, write, unblank
    [1] Values: enabled, preferred, primary boot, prink buffer,
                braille device, safe when CPU offline

Examples:

    $ cat /proc/consoles | jc --proc -p
    [
      {
        "device": "tty0",
        "operations": "-WU",
        "operations_list": [
          "write",
          "unblank"
        ],
        "flags": "ECp",
        "flags_list": [
          "enabled",
          "preferred",
          "printk buffer"
        ],
        "major": 4,
        "minor": 7
      },
      {
        "device": "ttyS0",
        "operations": "-W-",
        "operations_list": [
          "write"
        ],
        "flags": "Ep",
        "flags_list": [
          "enabled",
          "printk buffer"
        ],
        "major": 4,
        "minor": 64
      }
    ]
"""
import shlex
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/consoles` file parser'
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
    int_list = {'major', 'minor'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

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

    operations_map = {
        'R': 'read',
        'W': 'write',
        'U': 'unblank'
    }

    flags_map = {
        'E': 'enabled',
        'C': 'preferred',
        'B': 'primary boot',
        'p': 'printk buffer',
        'b': 'braille device',
        'a': 'safe when CPU offline'
    }

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            # since parens are acting like quotation marks, use shlex.split()
            # after converting parens to quotes.
            line = line.replace('(', '"'). replace(')', '"')
            device, operations, flags, maj_min = shlex.split(line)

            operations_str = operations.replace('-', '')
            operations_list = [operations_map[i] for i in operations_str]

            flags_str = flags.replace (' ', '')
            flags_list = [flags_map[i] for i in flags_str]

            raw_output.append(
                {
                    'device': device,
                    'operations': operations,
                    'operations_list': operations_list,
                    'flags': flags,
                    'flags_list': flags_list,
                    'major': maj_min.split(':')[0],
                    'minor': maj_min.split(':')[1]
                }
            )

    return raw_output if raw else _process(raw_output)
