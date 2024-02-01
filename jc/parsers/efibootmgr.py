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
      "BootCurrent": "0000",
      "Timeout": "0 seconds",
      "BootOrder": ["0000","0001"],
      "BootOptions": [
        {
          "BootOptionReference": "Boot0000",
          "DisplayName": "opensuse-secureboot",
          "UefiDevicePath": "HD(1,GPT,e45dbd72-ba93-4810-9330-2c1c493ff08b,0x800,0x31800)/File(\EFI\opensuse\shim.efi)",
          "BootOptionEnabled": true
        }
      ]
    ]

Examples:


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

    raw_output=[]
    boot_opt_list=[]

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            if -1 != line.find("BootCurrent"):
                tmp_dict={}
                tmp_dict["BootCurrent"]=line.split(':')[1].strip()
                raw_output.append(tmp_dict)
            elif -1 != line.find("Timeout"):
                tmp_dict={}
                tmp_dict["Timeout"]=line.split(':')[1].strip()
                raw_output.append(tmp_dict)
            elif -1 != line.find("BootOrder"):
                tmp_dict={}
                tmp_dict["BootOrder"]=line.split(':')[1].strip().split(',')
                raw_output.append(tmp_dict)
            elif -1 != line.find("Boot"):
                tmp_dict={}
                boot_record=line.split("\t")
                tmp_dict["BootOptionReference"]=boot_record[0][0:8]
                tmp_dict["DisplayName"]=boot_record[0][10:-1]
                if len(boot_record) > 1:
                    tmp_dict["UefiDevicePath"]=boot_record[1]
                tmp_dict["BootOptionEnabled"]=boot_record[0][8] == '*'
                boot_opt_list.append(tmp_dict)
            else:
                # print(line)
                pass

    tmp_dict={}
    tmp_dict["BootOptions"]=boot_opt_list
    raw_output.append(tmp_dict)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
