r"""jc - JSON Convert `/proc/modules` file parser

Usage (cli):

    $ cat /proc/modules | jc --proc

or

    $ jc /proc/modules

or

    $ cat /proc/modules | jc --proc-modules

Usage (module):

    import jc
    result = jc.parse('proc', proc_modules_file)

or

    import jc
    result = jc.parse('proc_modules', proc_modules_file)

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
        "location":                 string,
        "taint_state": [
                                    string
        ],
        "taint_state_verbose": [
                                    string
        ]
      }
    ]

Examples:

    $ cat /proc/modules | jc --proc -p
    [
      {
        "module": "i2c_piix4",
        "size": 28672,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0222000"
      },
      {
        "module": "pata_acpi",
        "size": 16384,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc021a000"
      },
      {
        "module": "falcon_lsm_serviceable",
        "size": 87169,
        "used": 1,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc056f000",
        "taint_state": [
          "P",
          "E"
        ],
        "taint_state_verbose": [
          "Proprietary or non-GPL-compatible module loaded",
          "Unsigned module loaded"
        ]
      },
      {
        "module": "nic_driver",
        "size": 16384,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc011a000",
        "taint_state": [
          "O"
        ],
        "taint_state_verbose": [
          "Out-of-tree (externally built) module loaded"
        ]
      }
    ]

    $ cat /proc/modules | jc --proc-modules -p -r
    [
      {
        "module": "i2c_piix4",
        "size": "28672",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0222000"
      },
      {
        "module": "pata_acpi",
        "size": "16384",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc021a000"
      },
      {
        "module": "falcon_lsm_serviceable",
        "size": "87169",
        "used": "1",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc056f000",
        "taint_state": "(PE)"
      },
      {
        "module": "nic_driver",
        "size": "16384",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc011a000",
        "taint_state": "(O)"
      }
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`/proc/modules` file parser'
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
    int_list = {'size', 'used'}

    taint_map = {
        "P": "Proprietary or non-GPL-compatible module loaded",
        "O": "Out-of-tree (externally built) module loaded",
        "E": "Unsigned module loaded",
        "F": "Module was force-loaded"
    }

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    for entry in proc_data:
        taint_pretty = {}
        for key in entry:
            if 'taint_state' in key:
                taint_pretty[key] = entry[key][1:-1]
                taint_pretty[key] = list(taint_pretty[key])
                taint_pretty['taint_state_verbose'] = [taint_map[x] for x in taint_pretty[key]]
        entry.update(taint_pretty)

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

            module_info = line.split()
            module, size, used, used_by, status, location = module_info[:6]
            taint_state = module_info[6] if len(module_info) > 6 else None
            used_by_list = used_by.split(',')[:-1]

            out = {
                'module': module,
                'size': size,
                'used': used,
                'used_by': used_by_list,
                'status': status,
                'location': location
            }

            if taint_state:
                out['taint_state'] = taint_state

            raw_output.append(out)

    return raw_output if raw else _process(raw_output)
