r"""jc - JSON Convert `/proc/interrupts` file parser

Usage (cli):

    $ cat /proc/interrupts | jc --proc

or

    $ jc /proc/interrupts

or

    $ cat /proc/interrupts | jc --proc-interrupts

Usage (module):

    import jc
    result = jc.parse('proc', proc_interrupts_file)

or

    import jc
    result = jc.parse('proc_interrupts', proc_interrupts_file)

Schema:

    [
      {
        "irq":                      string,
        "cpu_num":                  integer,
        "interrupts": [
                                    integer
        ],
        "type":                     string,
        "device": [
                                    string
        ]
      }
    ]

Examples:

    $ cat /proc/interrupts | jc --proc -p
    [
      {
        "irq": "0",
        "cpu_num": 2,
        "interrupts": [
          18,
          0
        ],
        "type": "IO-APIC",
        "device": [
          "2-edge",
          "timer"
        ]
      },
      {
        "irq": "1",
        "cpu_num": 2,
        "interrupts": [
          0,
          73
        ],
        "type": "IO-APIC",
        "device": [
          "1-edge",
          "i8042"
        ]
      },
      ...
    ]

    $ cat /proc/interrupts | jc --proc-interrupts -p -r
    [
      {
        "irq": "0",
        "cpu_num": 2,
        "interrupts": [
          "18",
          "0"
        ],
        "type": "IO-APIC",
        "device": [
          "2-edge",
          "timer"
        ]
      },
      {
        "irq": "1",
        "cpu_num": 2,
        "interrupts": [
          "0",
          "73"
        ],
        "type": "IO-APIC",
        "device": [
          "1-edge",
          "i8042"
        ]
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/interrupts` file parser'
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
        entry['interrupts'] = [int(x) for x in entry['interrupts']]

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
        data_lines = data.splitlines()

        # get the number of cpus
        cpu_num = len(data_lines[0].split())

        for line in filter(None, data_lines):

            # skip non-data lines
            if not ':' in line:
                continue

            # process data lines
            split_line = line.split()
            irq = split_line.pop(0)[:-1]

            interrupts = []
            if irq == 'ERR' or irq == 'MIS':
                interrupts.extend(split_line)

            elif irq.isdigit():
                for _ in range(cpu_num):
                    interrupts.append(split_line.pop(0))

                interrupt_type = split_line.pop(0)
                device = split_line

            else:
                for _ in range(cpu_num):
                    interrupts.append(split_line.pop(0))

                interrupt_type = ' '.join(split_line)
                device = []

            raw_output.append(
                {
                    'irq': irq,
                    'cpu_num': cpu_num,
                    'interrupts': interrupts,
                    'type': interrupt_type,
                    'device': device or None
                }
            )

    return raw_output if raw else _process(raw_output)
