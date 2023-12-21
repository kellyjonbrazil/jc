[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.blkid"></a>

# jc.parsers.blkid

jc - JSON Convert `blkid` command output parser

Usage (cli):

    $ blkid | jc --blkid

or

    $ jc blkid

Usage (module):

    import jc
    result = jc.parse('blkid', blkid_command_output)

Schema:

    [
      {
        "device":                            string,
        "uuid":                              string,
        "type":                              string,
        "usage":                             string,
        "part_entry_scheme":                 string,
        "part_entry_type":                   string,
        "part_entry_flags":                  string,
        "part_entry_number":                 integer,
        "part_entry_offset":                 integer,
        "part_entry_size":                   integer,
        "part_entry_disk":                   string,
        "id_fs_uuid":                        string,
        "id_fs_uuid_enc":                    string,
        "id_fs_version":                     string,
        "id_fs_type":                        string,
        "id_fs_usage":                       string,
        "id_part_entry_scheme":              string,
        "id_part_entry_type":                string,
        "id_part_entry_flags":               string,
        "id_part_entry_number":              integer,
        "id_part_entry_offset":              integer,
        "id_part_entry_size":                integer,
        "id_iolimit_minimum_io_size":        integer,
        "id_iolimit_physical_sector_size":   integer,
        "id_iolimit_logical_sector_size":    integer,
        "id_part_entry_disk":                string,
        "minimum_io_size":                   integer,
        "physical_sector_size":              integer,
        "logical_sector_size":               integer
      }
    ]

Examples:

    $ blkid | jc --blkid -p
    [
      {
        "device": "/dev/sda1",
        "uuid": "05d927ab-5875-49e4-ada1-7f46cb32c932",
        "type": "xfs"
      },
      {
        "device": "/dev/sda2",
        "uuid": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
        "type": "LVM2_member"
      },
      {
        "device": "/dev/mapper/centos-root",
        "uuid": "07d718ff-950c-4e5b-98f0-42a1147c77d9",
        "type": "xfs"
      },
      {
        "device": "/dev/mapper/centos-swap",
        "uuid": "615eb89a-bcbf-46fd-80e3-c483ff5c931f",
        "type": "swap"
      }
    ]

    $ sudo blkid -o udev -ip /dev/sda2 | jc --blkid -p
    [
      {
        "id_fs_uuid": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
        "id_fs_uuid_enc": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
        "id_fs_version": "LVM2\\x20001",
        "id_fs_type": "LVM2_member",
        "id_fs_usage": "raid",
        "id_iolimit_minimum_io_size": 512,
        "id_iolimit_physical_sector_size": 512,
        "id_iolimit_logical_sector_size": 512,
        "id_part_entry_scheme": "dos",
        "id_part_entry_type": "0x8e",
        "id_part_entry_number": 2,
        "id_part_entry_offset": 2099200,
        "id_part_entry_size": 39843840,
        "id_part_entry_disk": "8:0"
      }
    ]

    $ sudo blkid -ip /dev/sda1 | jc --blkid -p -r
    [
      {
        "devname": "/dev/sda1",
        "uuid": "05d927bb-5875-49e3-ada1-7f46cb31c932",
        "type": "xfs",
        "usage": "filesystem",
        "minimum_io_size": "512",
        "physical_sector_size": "512",
        "logical_sector_size": "512",
        "part_entry_scheme": "dos",
        "part_entry_type": "0x83",
        "part_entry_flags": "0x80",
        "part_entry_number": "1",
        "part_entry_offset": "2048",
        "part_entry_size": "2097152",
        "part_entry_disk": "8:0"
      }
    ]

<a id="jc.parsers.blkid.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/blkid.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/blkid.py)

Version 1.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
