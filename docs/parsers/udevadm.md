[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.udevadm"></a>

# jc.parsers.udevadm

jc - JSON Convert `udevadm info` command output parser

Usage (cli):

    $ udevadm info --query=all /dev/sda | jc --udevadm

or

    $ jc udevadm info --query=all /dev/sda

Usage (module):

    import jc
    result = jc.parse('udevadm', udevadm_command_output)

Schema:

    {
      "P":                    string,
      "N":                    string,
      "L":                    integer,
      "S": [
                              string
      ],
      "E": {
        "<key>":              string
      }
    }


Examples:

    $ udevadm info --query=all /dev/sda | jc --udevadm -p
    {
      "P": "/devices/pci0000:00/0000:00:10.0/host32/target32:0:0/32:0:0:0/block/sda",
      "N": "sda",
      "L": 0,
      "S": [
        "disk/by-path/pci-0000:00:10.0-scsi-0:0:0:0"
      ],
      "E": {
        "DEVPATH": "/devices/pci0000:00/0000:00:10.0/host32/target32:0:0/32:0:0:0/block/sda",
        "DEVNAME": "/dev/sda",
        "DEVTYPE": "disk",
        "MAJOR": "8",
        "MINOR": "0",
        "SUBSYSTEM": "block",
        "USEC_INITIALIZED": "6100111",
        "SCSI_TPGS": "0",
        "SCSI_TYPE": "disk",
        "SCSI_VENDOR": "VMware,",
        "SCSI_VENDOR_ENC": "VMware,\\x20",
        "SCSI_MODEL": "VMware_Virtual_S",
        "SCSI_MODEL_ENC": "VMware\\x20Virtual\\x20S",
        "SCSI_REVISION": "1.0",
        "ID_SCSI": "1",
        "ID_VENDOR": "VMware_",
        "ID_VENDOR_ENC": "VMware\\x2c\\x20",
        "ID_MODEL": "VMware_Virtual_S",
        "ID_MODEL_ENC": "VMware\\x20Virtual\\x20S",
        "ID_REVISION": "1.0",
        "ID_TYPE": "disk",
        "MPATH_SBIN_PATH": "/sbin",
        "ID_BUS": "scsi",
        "ID_PATH": "pci-0000:00:10.0-scsi-0:0:0:0",
        "ID_PATH_TAG": "pci-0000_00_10_0-scsi-0_0_0_0",
        "ID_PART_TABLE_UUID": "a5bd0c01-4210-46f2-b558-5c11c209a8f7",
        "ID_PART_TABLE_TYPE": "gpt",
        "DEVLINKS": "/dev/disk/by-path/pci-0000:00:10.0-scsi-0:0:0:0",
        "TAGS": ":systemd:"
      }
    }

    $ udevadm info --query=all /dev/sda | jc --udevadm -p -r
    {
      "P": "/devices/pci0000:00/0000:00:10.0/host32/target32:0:0/32:0:0:0/block/sda",
      "N": "sda",
      "L": "0",
      "S": [
        "disk/by-path/pci-0000:00:10.0-scsi-0:0:0:0"
      ],
      "E": {
        "DEVPATH": "/devices/pci0000:00/0000:00:10.0/host32/target32:0:0/32:0:0:0/block/sda",
        "DEVNAME": "/dev/sda",
        "DEVTYPE": "disk",
        "MAJOR": "8",
        "MINOR": "0",
        "SUBSYSTEM": "block",
        "USEC_INITIALIZED": "6100111",
        "SCSI_TPGS": "0",
        "SCSI_TYPE": "disk",
        "SCSI_VENDOR": "VMware,",
        "SCSI_VENDOR_ENC": "VMware,\\x20",
        "SCSI_MODEL": "VMware_Virtual_S",
        "SCSI_MODEL_ENC": "VMware\\x20Virtual\\x20S",
        "SCSI_REVISION": "1.0",
        "ID_SCSI": "1",
        "ID_VENDOR": "VMware_",
        "ID_VENDOR_ENC": "VMware\\x2c\\x20",
        "ID_MODEL": "VMware_Virtual_S",
        "ID_MODEL_ENC": "VMware\\x20Virtual\\x20S",
        "ID_REVISION": "1.0",
        "ID_TYPE": "disk",
        "MPATH_SBIN_PATH": "/sbin",
        "ID_BUS": "scsi",
        "ID_PATH": "pci-0000:00:10.0-scsi-0:0:0:0",
        "ID_PATH_TAG": "pci-0000_00_10_0-scsi-0_0_0_0",
        "ID_PART_TABLE_UUID": "a5bd0c01-4210-46f2-b558-5c11c209a8f7",
        "ID_PART_TABLE_TYPE": "gpt",
        "DEVLINKS": "/dev/disk/by-path/pci-0000:00:10.0-scsi-0:0:0:0",
        "TAGS": ":systemd:"
      }
    }

<a id="jc.parsers.udevadm.parse"></a>

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

Source: [`jc/parsers/udevadm.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/udevadm.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
