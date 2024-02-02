"""jc - JSON Convert `efibootmgr` command output parser

Only `efibootmgr -v` option is supported with the default output.

Usage (cli):

    $ sudo efibootmgr | jc --efibootmgr
    $ sudo efibootmgr -v | jc --efibootmgr

or

    $ sudo jc efibootmgr

Usage (module):

    import jc
    result = jc.parse('efibootmgr', efibootmgr_command_output)

Schema:

[
    {
        "boot_current": string,
        "timeout_seconds": number,
        "boot_order": [
            string,
            string,
            string
        ],
        mirrored_percentage_above_4g: number,
        mirror_memory_below_4gb: bool,
        "boot_options": [
            {
                "boot_option_reference": string,
                "display_name": string,
                "uefi_device_path": string,
                "boot_option_enabled": bool
            },
            {
                "boot_option_reference": string,
                "display_name": string,
                "uefi_device_path": string,
                "boot_option_enabled": bool
            },
            {
                "boot_option_reference": string,
                "display_name": string,
                "uefi_device_path": string,
                "boot_option_enabled": bool
            }
        ]
    }
]

Examples:

$ sudo efibootmgr -v | jc --efibootmgr --pretty
[
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
        "uefi_device_path": "HD(1,GPT,05b9944c-1c60-492b-a510-7bbedccdc602,0x800,0xfa000)/File(EFI\\boot\\bootx64.efi)",
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
        "uefi_device_path": "HD(1,GPT,c5d4f69d-6fc2-48c7-acee-af3f30336dc5,0x800,0x19000)/File(\\EFI\\opensuse\\shim.efi)",
        "boot_option_enabled": true
      }
    ]
  }
]

"""

import jc.utils
import jc.parsers.universal

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '0.1'
    description = '`efibootmgr -v` command parser'
    author = 'Yaofei Zheng'
    author_email = ['zyf26256@gmail.com','Yaofei.Zheng@dell.com']
    compatible = ['linux']
    magic_commands = ['efibootmgr']
    tags = ['command']

__version__ = info.version

def _process(proc_data):
    if 0 == len(proc_data):
        return proc_data
    proc_data[0]["timeout_seconds"] = int(proc_data[0]["timeout_seconds"].replace("seconds","").strip(), 10)
    proc_data[0]["boot_order"] = proc_data[0]["boot_order"].split(',')
    for boot_opt in proc_data[0]["boot_options"]:
        boot_opt["boot_option_enabled"] = boot_opt["boot_option_enabled"] == '*'
    proc_data[0]["mirrored_percentage_above_4g"] = float(proc_data[0]["mirrored_percentage_above_4g"])
    proc_data[0]["mirror_memory_below_4gb"] = not ("false" == proc_data[0]["mirror_memory_below_4gb"])
    return proc_data

def parse(data, raw=False, quiet=False):
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []

    if jc.utils.has_data(data):
        boot_opt_list = []
        efibootmgr_dict = {}
        for line in filter(None, data.splitlines()):
            if "BootCurrent" in line:
                efibootmgr_dict["boot_current"] = line.split(':')[1].strip()
            elif "Timeout" in line:
                efibootmgr_dict["timeout_seconds"] = line.split(':')[1].strip()
            elif "BootOrder" in line:
                efibootmgr_dict["boot_order"] = line.split(':')[1].strip()
            elif "Boot" in line:
                tmp_dict = {}
                boot_record = line.split("\t")
                tmp_dict["boot_option_reference"] = boot_record[0][0:8]
                tmp_dict["display_name"] = boot_record[0][10:].strip()
                if len(boot_record) > 1:
                    tmp_dict["uefi_device_path"] = boot_record[1].strip()
                tmp_dict["boot_option_enabled"] = boot_record[0][8]
                boot_opt_list.append(tmp_dict)
            elif "MirroredPercentageAbove4G" in line:
                efibootmgr_dict["mirrored_percentage_above_4g"] = line.split(':')[1].strip()
            elif "MirrorMemoryBelow4GB" in line:
                efibootmgr_dict["mirror_memory_below_4gb"] = line.split(':')[1].strip()
            else:
                # print(line)
                continue

        efibootmgr_dict["boot_options"] = boot_opt_list

        raw_output.append(efibootmgr_dict)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
