[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.mdadm"></a>

# jc.parsers.mdadm

jc - JSON Convert `mdadm` command output parser

Supports the `--query` and `--examine` options in `mdadm`.

Usage (cli):

    $ mdadm --query --detail /dev/md0 | jc --mdadm

or

    $ mdadm --examine -E /dev/sdb1 | jc --mdadm

or

    $ jc mdadm --query --detail /dev/md0

or

    $ jc mdadm --examine -E /dev/sdb1

Usage (module):

    import jc
    result = jc.parse('mdadm', mdadm_command_output)

Schema:

    {
      "device":                       string,
      "magic":                        string,
      "version":                      string,
      "feature_map":                  string,
      "array_uuid":                   string,
      "name":                         string,
      "name_val":                     string,
      "uuid":                         string,
      "uuid_val":                     string,
      "homehost":                     string,
      "container":                    string,
      "container_dev":                string,
      "container_member":             integer,
      "controller_guid":              string,
      "container_guid":               string,
      "seq":                          string,
      "redundant_hdr":                string,
      "virtual_disks":                integer,
      "creation_time":                string,
      "creation_time_epoch":          integer,  # naive timestamp
      "raid_level":                   string,
      "array_size":                   string,
      "array_size_num":               integer,
      "used_dev_size":                string,
      "used_dev_size_num":            integer,
      "raid_devices":                 integer,
      "avail_dev_size":               string,
      "avail_dev_size_num":           integer,
      "data_offset":                  integer,
      "super_offset":                 integer,
      "unused_space":                 string,
      "unused_space_before":          integer,
      "unused_space_after":           integer,
      "state":                        string,
      "state_list": [
                                      string
      ],
      "device_uuid":                  string,
      "flags":                        string,
      "flag_list": [
                                      string
      ],
      "update_time":                  string,
      "update_time_epoch":            integer,  # naive timestamp
      "bad_block_log":                string,
      "checksum":                     string,
      "checksum_val":                 string,
      "checksum_state":               string,
      "events":                       string,
      "events_num":                   integer,
      "events_maj":                   integer,
      "events_min":                   integer,
      "chunk_size":                   string,
      "chunk_size_num":               integer,
      "device_role":                  string,
      "array_state":                  string,
      "array_state_list": [
                                      string
      ],
      "member_arrays":                string,
      "member_arrays_list": [
                                      string
      ],
      "consistency_policy":           string,
      "rebuild_status":               string,
      "rebuild_status_percent":       integer,
      "resync_status":                string,
      "resync_status_percent":        integer,
      "check_status":                 string,
      "check_status_percent":         integer,
      "total_devices":                integer,
      "preferred_minor":              integer,
      "persistence":                  string,
      "active_devices":               integer,
      "working_devices":              integer,
      "failed_devices":               integer,
      "spare_devices":                integer,
      "physical_disks":               integer,
      "device_table": [
        {
          "number":                   integer/null,
          "major":                    integer/null,
          "minor":                    integer/null,
          "state": [
                                      string
          ],
          "device":                   string,
          "raid_device":              integer/null
        }
      ]
    }

    Any fields unspecified above will be string type.

Examples:

    $ mdadm --query --detail /dev/md0 | jc --mdadm -p
    {
      "device": "/dev/md0",
      "version": "1.1",
      "creation_time": "Tue Apr 13 23:22:16 2010",
      "raid_level": "raid1",
      "array_size": "5860520828 (5.46 TiB 6.00 TB)",
      "used_dev_size": "5860520828 (5.46 TiB 6.00 TB)",
      "raid_devices": 2,
      "total_devices": 2,
      "persistence": "Superblock is persistent",
      "intent_bitmap": "Internal",
      "update_time": "Tue Jul 26 20:16:31 2022",
      "state": "clean",
      "active_devices": 2,
      "working_devices": 2,
      "failed_devices": 0,
      "spare_devices": 0,
      "consistency_policy": "bitmap",
      "name": "virttest:0",
      "uuid": "85c5b164:d58a5ada:14f5fe07:d642e843",
      "events": 2193679,
      "device_table": [
        {
          "number": 3,
          "major": 8,
          "minor": 17,
          "state": [
            "active",
            "sync"
          ],
          "device": "/dev/sdb1",
          "raid_device": 0
        },
        {
          "number": 2,
          "major": 8,
          "minor": 33,
          "state": [
            "active",
            "sync"
          ],
          "device": "/dev/sdc1",
          "raid_device": 1
        }
      ],
      "array_size_num": 5860520828,
      "used_dev_size_num": 5860520828,
      "name_val": "virttest:0",
      "uuid_val": "85c5b164:d58a5ada:14f5fe07:d642e843",
      "state_list": [
        "clean"
      ],
      "creation_time_epoch": 1271226136,
      "update_time_epoch": 1658891791
    }

    $ mdadm --query --detail /dev/md0 | jc --mdadm -p -r
    {
      "device": "/dev/md0",
      "version": "1.1",
      "creation_time": "Tue Apr 13 23:22:16 2010",
      "raid_level": "raid1",
      "array_size": "5860520828 (5.46 TiB 6.00 TB)",
      "used_dev_size": "5860520828 (5.46 TiB 6.00 TB)",
      "raid_devices": "2",
      "total_devices": "2",
      "persistence": "Superblock is persistent",
      "intent_bitmap": "Internal",
      "update_time": "Tue Jul 26 20:16:31 2022",
      "state": "clean",
      "active_devices": "2",
      "working_devices": "2",
      "failed_devices": "0",
      "spare_devices": "0",
      "consistency_policy": "bitmap",
      "name": "virttest:0",
      "uuid": "85c5b164:d58a5ada:14f5fe07:d642e843",
      "events": "2193679",
      "device_table": [
        {
          "number": "3",
          "major": "8",
          "minor": "17",
          "state": "active sync",
          "device": "/dev/sdb1",
          "raid_device": "0"
        },
        {
          "number": "2",
          "major": "8",
          "minor": "33",
          "state": "active sync",
          "device": "/dev/sdc1",
          "raid_device": "1"
        }
      ]
    }

<a id="jc.parsers.mdadm.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
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

Source: [`jc/parsers/mdadm.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/mdadm.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
