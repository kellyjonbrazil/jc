"""jc - JSON Convert `/proc/interrupts` file parser

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
        "module":                   string,
        "size":                     integer,
        "used":                     integer,
        "used_by": [
                                    string
        ],
        "status":                   string,
        "location":                 string
      }
    ]

Examples:

    $ cat /proc/interrupts | jc --proc -p
    [
      {
        "module": "binfmt_misc",
        "size": 24576,
        "used": 1,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0ab4000"
      },
      {
        "module": "vsock_loopback",
        "size": 16384,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0a14000"
      },
      {
        "module": "vmw_vsock_virtio_transport_common",
        "size": 36864,
        "used": 1,
        "used_by": [
          "vsock_loopback"
        ],
        "status": "Live",
        "location": "0xffffffffc0a03000"
      },
      ...
    ]

    $ proc_interrupts | jc --proc_interrupts -p -r
    [
      {
        "module": "binfmt_misc",
        "size": "24576",
        "used": "1",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0ab4000"
      },
      {
        "module": "vsock_loopback",
        "size": "16384",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0a14000"
      },
      {
        "module": "vmw_vsock_virtio_transport_common",
        "size": "36864",
        "used": "1",
        "used_by": [
          "vsock_loopback"
        ],
        "status": "Live",
        "location": "0xffffffffc0a03000"
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
    int_list = {'size', 'used'}

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
                interrupt_info = split_line

            else:
                for _ in range(cpu_num):
                    interrupts.append(split_line.pop(0))

                interrupt_type = ' '.join(split_line)
                interrupt_info = []

            raw_output.append(
                {
                    'irq': irq,
                    'cpu_num': cpu_num,
                    'interrupts': interrupts,
                    'interrupt_type': interrupt_type,
                    'interrupt_info': interrupt_info or None
                }
            )

    return raw_output if raw else _process(raw_output)
