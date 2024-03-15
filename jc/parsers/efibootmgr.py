r"""jc - JSON Convert `efibootmgr` command output parser

The `-v` option is also supported.

Usage (cli):

    $ sudo efibootmgr | jc --efibootmgr
    $ sudo efibootmgr -v | jc --efibootmgr

or

    $ sudo jc efibootmgr

Usage (module):

    import jc
    result = jc.parse('efibootmgr', efibootmgr_command_output)

Schema:

    {
        "boot_current":                     string,
        "timeout_seconds":                  integer,
        "boot_order": [
                                            string
        ],
        mirrored_percentage_above_4g:       float,
        mirror_memory_below_4gb:            boolean,
        "boot_options": [
            {
                "boot_option_reference":    string,
                "display_name":             string,
                "uefi_device_path":         string,
                "boot_option_enabled":      boolean
            }
        ]
    }

Examples:

    $ sudo efibootmgr -v | jc --efibootmgr --p
    {
      "boot_current": "0002",
      "timeout_seconds": 0,
      "boot_order": [
        "0002",
        "0000",
        "0001"
      ],
      "mirrored_percentage_above_4g": 0.0,
      "mirror_memory_below_4gb": false,
      "boot_options": [
        {
          "boot_option_reference": "Boot0000",
          "display_name": "WARNADO",
          "uefi_device_path": "HD(1,GPT,05b9944c-1c60-492b-a510-7bbedccdc...",
          "boot_option_enabled": true
        },
        {
          "boot_option_reference": "Boot0001",
          "display_name": "Embedded NIC 1 Port 1 Partition 1",
          "uefi_device_path": "VenHw(3a191845-5f86-4e78-8fce-c4cff59f9daa)",
          "boot_option_enabled": true
        },
        {
          "boot_option_reference": "Boot0002",
          "display_name": "opensuse-secureboot",
          "uefi_device_path": "HD(1,GPT,c5d4f69d-6fc2-48c7-acee-af3f30336...",
          "boot_option_enabled": true
        }
      ]
    }
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`efibootmgr` command parser'
    author = 'Yaofei Zheng'
    author_email = "zyf26256@gmail.com, Yaofei.Zheng@dell.com"
    compatible = ['linux']
    magic_commands = ['efibootmgr']
    tags = ['command']

__version__ = info.version

def _process(proc_data: JSONDictType) -> JSONDictType:
    if 'timeout_seconds' in proc_data:
        proc_data["timeout_seconds"] = jc.utils.convert_to_int(proc_data["timeout_seconds"])

    if 'boot_order' in proc_data:
        proc_data["boot_order"] = proc_data["boot_order"].split(',')

    if 'boot_options' in proc_data:
        for boot_opt in proc_data["boot_options"]:
            boot_opt["boot_option_enabled"] = bool(boot_opt["boot_option_enabled"] == '*')

    if 'mirrored_percentage_above_4g' in proc_data:
        proc_data["mirrored_percentage_above_4g"] = float(proc_data["mirrored_percentage_above_4g"])

    if 'mirror_memory_below_4gb' in proc_data:
        proc_data["mirror_memory_below_4gb"] = not (proc_data["mirror_memory_below_4gb"] == "false")

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
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
        boot_opt_list: List = []

        for line in filter(None, data.splitlines()):

            if "BootCurrent" in line:
                raw_output["boot_current"] = line.split(':')[1].strip()

            elif "Timeout" in line:
                raw_output["timeout_seconds"] = line.split(':')[1].strip()

            elif "BootOrder" in line:
                raw_output["boot_order"] = line.split(':')[1].strip()

            elif "Boot" in line:
                tmp_dict: Dict = {}
                boot_record = line.split("\t")
                tmp_dict["boot_option_reference"] = boot_record[0][0:8]
                tmp_dict["display_name"] = boot_record[0][10:].strip()

                if len(boot_record) > 1:
                    tmp_dict["uefi_device_path"] = boot_record[1].strip()

                tmp_dict["boot_option_enabled"] = boot_record[0][8]
                boot_opt_list.append(tmp_dict)

            elif "MirroredPercentageAbove4G" in line:
                raw_output["mirrored_percentage_above_4g"] = line.split(':')[1].strip()

            elif "MirrorMemoryBelow4GB" in line:
                raw_output["mirror_memory_below_4gb"] = line.split(':')[1].strip()

        raw_output["boot_options"] = boot_opt_list

    return raw_output if raw else _process(raw_output)
