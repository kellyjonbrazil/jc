"""jc - JSON CLI output utility blkid Parser

Usage:

    specify --blkid as the first argument if the piped input is coming from blkid

Compatibility:

    'linux'

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
"""
import shlex
import jc.utils


class info():
    version = '1.2'
    description = 'blkid command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['blkid']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

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
    """
    for entry in proc_data:
        if 'devname' in entry:
            entry['device'] = entry.pop('devname')

        int_list = ['part_entry_number', 'part_entry_offset', 'part_entry_size', 'id_part_entry_number',
                    'id_part_entry_offset', 'id_part_entry_size', 'minimum_io_size', 'physical_sector_size',
                    'logical_sector_size', 'id_iolimit_minimum_io_size', 'id_iolimit_physical_sector_size',
                    'id_iolimit_logical_sector_size']
        for key in int_list:
            if key in entry:
                try:
                    entry[key] = int(entry[key])
                except (ValueError):
                    entry[key] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        # if the first field is a device, use normal parsing:
        if data.split(maxsplit=1)[0][-1] == ':':
            linedata = data.splitlines()

            for line in linedata:
                output_line = {}
                entries = shlex.split(line)
                output_line['device'] = entries.pop(0)[:-1]

                for entry in entries:
                    key = entry.split('=', maxsplit=1)[0].lower()
                    value = entry.split('=', maxsplit=1)[1]
                    output_line[key] = value

                raw_output.append(output_line)

        # else use key/value per line parsing
        else:
            linedata = data.splitlines()
            output_line = {}
            for line in linedata:
                if line == '':
                    if output_line:
                        raw_output.append(output_line)
                        output_line = {}
                        continue
                    continue

                key = line.split('=', maxsplit=1)[0].lower()
                value = line.split('=', maxsplit=1)[1]
                output_line[key] = value

            if output_line:
                raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
