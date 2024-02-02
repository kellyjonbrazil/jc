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
        "BootCurrent": string,
        "Timeout": string,
        "BootOrder": [
            string,
            string,
            string
        ],
        "BootOptions": [
            {
                "BootOptionReference": string,
                "DisplayName": string,
                "UefiDevicePath": string,
                "BootOptionEnabled": bool
            },
            {
                "BootOptionReference": string,
                "DisplayName": string,
                "UefiDevicePath": string,
                "BootOptionEnabled": bool
            },
            {
                "BootOptionReference": string,
                "DisplayName": string,
                "UefiDevicePath": string,
                "BootOptionEnabled": bool
            }
        ]
    }
]

Examples:

$ sudo efibootmgr -v | jc --efibootmgr | jq
[
  {
    "BootCurrent": "0002",
    "Timeout": "0 seconds",
    "BootOrder": [
      "0002",
      "0000",
      "0001"
    ],
    "BootOptions": [
      {
        "BootOptionReference": "Boot0000",
        "DisplayName": "WARNADO",
        "UefiDevicePath": "HD(1,GPT,05b9944c-1c60-492b-a510-7bbedccdc602,0x800,0xfa000)/File(EFI\\boot\\bootx64.efi)",
        "BootOptionEnabled": true
      },
      {
        "BootOptionReference": "Boot0001",
        "DisplayName": "Embedded NIC 1 Port 1 Partition 1",
        "UefiDevicePath": "VenHw(3a191845-5f86-4e78-8fce-c4cff59f9daa)",
        "BootOptionEnabled": true
      },
      {
        "BootOptionReference": "Boot0002",
        "DisplayName": "opensuse-secureboot",
        "UefiDevicePath": "HD(1,GPT,c5d4f69d-6fc2-48c7-acee-af3f30336dc5,0x800,0x19000)/File(\\EFI\\opensuse\\shim.efi)",
        "BootOptionEnabled": true
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
                efibootmgr_dict["BootCurrent"] = line.split(':')[1].strip()
            elif "Timeout" in line:
                efibootmgr_dict["Timeout"] = line.split(':')[1].strip()
            elif "BootOrder" in line:
                efibootmgr_dict["BootOrder"] = line.split(':')[1].strip().split(',')
            elif "Boot" in line:
                tmp_dict = {}
                boot_record = line.split("\t")
                tmp_dict["BootOptionReference"] = boot_record[0][0:8]
                tmp_dict["DisplayName"] = boot_record[0][10:]
                if len(boot_record) > 1:
                    tmp_dict["UefiDevicePath"] = boot_record[1]
                tmp_dict["BootOptionEnabled"] = boot_record[0][8] == '*'
                boot_opt_list.append(tmp_dict)
            else:
                # print(line)
                continue

        efibootmgr_dict["BootOptions"] = boot_opt_list

        raw_output.append(efibootmgr_dict)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
