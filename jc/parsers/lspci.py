"""jc - JSON Convert `lspci -mmv` command output parser

This parser supports the following `lspci` options:
- `-mmv`
- `-nmmv`
- `-nnmmv`

Usage (cli):

    $ lspci -nnmmv | jc --lspci

or

    $ jc lspci -nnmmv

Usage (module):

    import jc
    result = jc.parse('lspci', lspci_command_output)

Schema:

    [
      {
        "slot":                         string,
        "domain":                       string,
        "domain_int":                   integer,
        "bus":                          string,
        "bus_int":                      integer,
        "dev":                          string,
        "dev_int":                      integer,
        "function":                     string,
        "function_int":                 integer,
        "class":                        string,
        "class_id":                     string,
        "class_id_int":                 integer,
        "vendor":                       string,
        "vendor_id":                    string,
        "vendor_id_int":                integer,
        "device":                       string,
        "device_id":                    string,
        "device_id_int":                integer,
        "svendor":                      string,
        "svendor_id":                   string,
        "svendor_id_int":               integer,
        "sdevice":                      string,
        "sdevice_id":                   string,
        "sdevice_id_int":               integer,
        "rev":                          string,
        "physlot":                      string,
        "physlot_int":                  integer,
        "progif":                       string,
        "progif_int":                   integer
      }
    ]

Examples:

    $ lspci -nnmmv | jc --lspci -p
    [
      {
        "slot": "ff:02:05.0",
        "domain": "ff",
        "domain_int": 255,
        "bus": "02",
        "bus_int": 2,
        "dev": "05",
        "dev_int": 5,
        "function": "0",
        "function_int": 0,
        "class": "SATA controller",
        "class_id": "0106",
        "class_id_int": 262,
        "vendor": "VMware",
        "vendor_id": "15ad",
        "vendor_id_int": 5549,
        "device": "SATA AHCI controller",
        "device_id": "07e0",
        "device_id_int": 2016,
        "svendor": "VMware",
        "svendor_id": "15ad",
        "svendor_id_int": 5549,
        "sdevice": "SATA AHCI controller",
        "sdevice_id": "07e0",
        "sdevice_id_int": 2016,
        "physlot": "37",
        "physlot_int": 55,
        "progif": "01",
        "progif_int": 1
      },
      ...
    ]

    $ lspci -nnmmv | jc --lspci -p -r
    [
      {
        "slot": "ff:02:05.0",
        "domain": "ff",
        "bus": "02",
        "dev": "05",
        "function": "0",
        "class": "SATA controller",
        "class_id": "0106",
        "vendor": "VMware",
        "vendor_id": "15ad",
        "device": "SATA AHCI controller",
        "device_id": "07e0",
        "svendor": "VMware",
        "svendor_id": "15ad",
        "sdevice": "SATA AHCI controller",
        "sdevice_id": "07e0",
        "physlot": "37",
        "progif": "01"
      },
      ...
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`lspci -mmv` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['lspci']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list: set[str] = {
        'domain', 'bus', 'dev', 'function', 'class_id', 'vendor_id', 'device_id',
        'svendor_id', 'sdevice_id', 'physlot', 'progif'
    }

    new_list: List[JSONDictType] = []

    for item in proc_data:
        output: Dict = {}
        for key, val in item.items():
            output[key] = val
            if key in int_list:
                output[key + '_int'] = int(val, 16)
        new_list.append(output)

    return new_list


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

    raw_output: List = []
    device_output: Dict = {}

    if jc.utils.has_data(data):
        item_id_p = re.compile(r'(?P<id>^[0-9a-f]{4}$)')
        item_id_bracket_p = re.compile(r' \[(?P<id>[0-9a-f]{4})\]$')

        for line in filter(None, data.splitlines()):
            if line.startswith('Slot:'):
                if device_output:
                    raw_output.append(device_output)
                    device_output = {}

                device_output['slot'] = line.split()[1]

                slot_info = line.split()[1]
                *domain, bus, dev_fun = slot_info.split(':')

                if domain:
                    dom = domain[0]
                else:
                    dom = "00"

                dev, fun = dev_fun.split('.')
                device_output['domain'] = dom
                device_output['bus'] = bus
                device_output['dev'] = dev
                device_output['function'] = fun
                continue

            key, val = line.split(maxsplit=1)
            key = key[:-1].lower()

            # numeric only (-nmmv)
            if item_id_p.match(val):
                device_output[key + '_id'] = val
                continue

            # string and numeric (-nnmmv)
            if item_id_bracket_p.search(val):
                string, idnum = val.rsplit(maxsplit=1)
                device_output[key] = string
                device_output[key + '_id'] = idnum[1:-1]
                continue

            # string only (-mmv)
            device_output[key] = val
            continue


        if device_output:
            raw_output.append(device_output)

    return raw_output if raw else _process(raw_output)
