[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.efibootmgr"></a>

# jc.parsers.efibootmgr

jc - JSON Convert `efibootmgr` command output parser

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

<a id="jc.parsers.efibootmgr.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/efibootmgr.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/efibootmgr.py)

Version 1.0 by Yaofei Zheng (zyf26256@gmail.com, Yaofei.Zheng@dell.com)
