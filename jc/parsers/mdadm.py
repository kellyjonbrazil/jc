"""jc - JSON Convert `mdadm` command output parser

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
"""
from typing import Dict
import re
import jc.utils
from jc.parsers.universal import sparse_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`mdadm` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['mdadm']
    tags = ['command']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list = {'array_size_num', 'used_dev_size_num', 'raid_devices', 'total_devices', 'Number',
                'active_devices', 'working_devices', 'failed_devices', 'spare_devices', 'physical_disks',
                'number', 'major', 'minor', 'raid_device', 'avail_dev_size_num', 'virtual_disks',
                'data_offset', 'super_offset', 'unused_space_before', 'unused_space_after',
                'chunk_size_num', 'preferred_minor', 'check_status_percent', 'resync_status_percent',
                'rebuild_status_percent', 'events_num', 'events_maj', 'events_min', 'container_member'}

    array_state_map = {
        'A': 'active',
        '.': 'missing',
        'R': 'replacing'
    }

    # split combined values
    if 'array_size' in proc_data:
        proc_data['array_size_num'] = proc_data['array_size'].split(maxsplit=1)[0]

    if 'used_dev_size' in proc_data:
        proc_data['used_dev_size_num'] = proc_data['used_dev_size'].split(maxsplit=1)[0]

    if 'avail_dev_size' in proc_data:
        proc_data['avail_dev_size_num'] = proc_data['avail_dev_size'].split(maxsplit=1)[0]

    if 'data_offset' in proc_data:
        proc_data['data_offset'] = proc_data['data_offset'].split()[0]

    if 'super_offset' in proc_data:
        proc_data['super_offset'] = proc_data['super_offset'].split()[0]

    if 'unused_space' in proc_data:
        unused_space_list = proc_data['unused_space'].split(',')
        before_text = unused_space_list[0].strip()
        after_text = unused_space_list[1].strip()
        before = before_text.split('=')[1].split()[0]
        after = after_text.split('=')[1].split()[0]
        proc_data['unused_space_before'] = before
        proc_data['unused_space_after'] = after

    if 'name' in proc_data:
        proc_data['name_val'] = proc_data['name'].split(maxsplit=1)[0]
        if proc_data['name'].endswith(')'):
            proc_data['homehost'] = proc_data['name'].rsplit(maxsplit=1)[1][0:-1]

    if 'uuid' in proc_data:
        proc_data['uuid_val'] = proc_data['uuid'].split(maxsplit=1)[0]
        if proc_data['uuid'].endswith(')'):
            proc_data['homehost'] = proc_data['uuid'].rsplit(maxsplit=1)[1][0:-1]

    if 'container' in proc_data:
        if ', member ' in proc_data['container']:
            proc_data['container_dev'] = proc_data['container'].split(',')[0]
            proc_data['container_member'] = proc_data['container'].rsplit(maxsplit=1)[-1]

    if 'chunk_size' in proc_data:
        proc_data['chunk_size_num'] = proc_data['chunk_size']

    if 'events' in proc_data:
        if '.' in proc_data['events']:
            events_maj, events_min = proc_data['events'].split('.', maxsplit=1)
            proc_data['events_maj'] = events_maj
            proc_data['events_min'] = events_min
        else:
            proc_data['events_num'] = proc_data['events']

    if 'checksum' in proc_data:
        proc_data['checksum_val'] = proc_data['checksum'].split(maxsplit=1)[0]
        proc_data['checksum_state'] = proc_data['checksum'].split()[-1]

    if 'state' in proc_data:
        state_list = [x.strip() for x in proc_data['state'].split(',')]
        proc_data['state_list'] = state_list

    if 'flags' in proc_data:
        proc_data['flag_list'] = proc_data['flags'].split()

    if 'member_arrays' in proc_data:
        proc_data['member_arrays_list'] = proc_data['member_arrays'].split()

    if 'array_state' in proc_data:
        array_state_list = []
        array_state_text = proc_data['array_state'].split(maxsplit=1)[0]

        for item in array_state_text:
            array_state_list.append(array_state_map[item])

        proc_data['array_state_list'] = array_state_list

    if 'resync_status' in proc_data:
        proc_data['resync_status_percent'] = proc_data['resync_status'].split('%')[0]

    if 'check_status' in proc_data:
        proc_data['check_status_percent'] = proc_data['check_status'].split('%')[0]

    if 'rebuild_status' in proc_data:
        proc_data['rebuild_status_percent'] = proc_data['rebuild_status'].split('%')[0]

    # add timestamp fields
    if 'creation_time' in proc_data:
        dt = jc.utils.timestamp(proc_data['creation_time'], format_hint=(1000,))
        proc_data['creation_time_epoch'] = dt.naive

    if 'update_time' in proc_data:
        dt = jc.utils.timestamp(proc_data['update_time'], format_hint=(1000,))
        proc_data['update_time_epoch'] = dt.naive

    # convert ints/floats
    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc .utils.convert_to_int(proc_data[key])

    # table items
    if 'device_table' in proc_data:
        for item in proc_data['device_table']:
            if 'state' in item:
                item['state'] = item['state'].split()

            # convert ints
            for key in item:
                if key in int_list:
                    item[key] = jc.utils.convert_to_int(item[key])

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
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

    raw_output = {}
    device_table = False
    device_table_list = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            # device line
            if line.startswith('/') and line.endswith(':'):
                raw_output['device'] = line[:-1]
                continue

            # key/value lines
            if ' : ' in line:
                key, value = line.split(' : ', maxsplit=1)
                key = key.strip().lower()
                key = re.sub(r'[^a-z0-9]', '_', key)
                key = key.strip('_')
                value = value.strip()
                raw_output[key] = value
                continue

            # device table header
            if '    Number   Major   Minor   RaidDevice State' in line:
                device_table_list.append('    number   major   minor   RaidDevice state         device')
                device_table = True
                continue

            elif '    Number   Major   Minor   RaidDevice' in line:
                device_table_list.append('    number   major   minor   RaidDevice device')
                device_table = True
                continue

            elif '      Number    RefNo      Size       Device      Type/State' in line:
                device_table_list.append('      Number    RefNo      Size       Device      Type/State')
                device_table = True
                continue

            # device table lines
            if device_table == True:
                device_table_list.append(line)
                continue

        if device_table_list:
            d_table = sparse_table_parse(device_table_list)
            for item in d_table:
                if 'RaidDevice' in item:
                    item['raid_device'] = item.pop('RaidDevice')

                if 'device' in item and item['device']:
                    if not item['device'].startswith('/'):
                        flags, dev = item['device'].rsplit(maxsplit=1)
                        item['device'] = dev
                        item['state'] = item['state'] + ' ' + flags

            raw_output['device_table'] = d_table    # type: ignore

    return raw_output if raw else _process(raw_output)
