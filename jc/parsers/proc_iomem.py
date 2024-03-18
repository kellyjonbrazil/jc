r"""jc - JSON Convert `/proc/iomem` file parser

Usage (cli):

    $ cat /proc/iomem | jc --proc

or

    $ jc /proc/iomem

or

    $ cat /proc/iomem | jc --proc-iomem

Usage (module):

    import jc
    result = jc.parse('proc', proc_iomem_file)

or

    import jc
    result = jc.parse('proc_iomem', proc_iomem_file)

Schema:

    [
      {
        "start":                   string,
        "end":                     string,
        "device":                  string
      }
    ]

Examples:

    $ cat /proc/iomem | jc --proc -p
    [
      {
        "start": "00000000",
        "end": "00000fff",
        "device": "Reserved"
      },
      {
        "start": "00001000",
        "end": "0009e7ff",
        "device": "System RAM"
      },
      {
        "start": "0009e800",
        "end": "0009ffff",
        "device": "Reserved"
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/iomem` file parser'
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

            colon_split = line.split(':', maxsplit=1)
            device = colon_split[1].strip()
            mem_split = colon_split[0].split('-', maxsplit=1)
            start = mem_split[0].strip()
            end = mem_split[1].strip()

            raw_output.append(
                {
                    'start': start,
                    'end': end,
                    'device': device
                }
            )

    return raw_output if raw else _process(raw_output)
