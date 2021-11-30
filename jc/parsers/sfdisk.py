"""jc - JSON CLI output utility `sfdisk` command output parser

Supports the following `sfdisk` options:
- `-l`
- `-F`
- `-d`   (deprecated - only for older versions of util-linux)
- `-uM`  (deprecated - only for older versions of util-linux)
- `-uC`  (deprecated - only for older versions of util-linux)
- `-uS`  (deprecated - only for older versions of util-linux)
- `-uB`  (deprecated - only for older versions of util-linux)

Usage (cli):

    # sfdisk -l | jc --sfdisk

    or

    # jc sfdisk -l

Usage (module):

    import jc.parsers.sfdisk
    result = jc.parsers.sfdisk.parse(sfdisk_command_output)

Schema:

    [
      {
        "disk":                     string,
        "disk_size":                string,
        "free_disk_size":           string,
        "bytes":                    integer,
        "free_bytes":               integer,
        "sectors":                  integer,
        "free_sectors":             integer,
        "cylinders":                integer,
        "heads":                    integer,
        "sectors_per_track":        integer,
        "units":                    string,
        "logical_sector_size":      integer,
        "physical_sector_size":     integer,
        "min_io_size":              integer,
        "optimal_io_size":          integer,
        "disk_label_type":          string,
        "disk_identifier":          string,
        "disk_model":               string,
        "partitions": [
          {
            "device":               string,
            "boot":                 boolean,
            "start":                integer,
            "end":                  integer,
            "size":                 string,    # Note: will be integer when using deprecated -d sfdisk option
            "cyls":                 integer,
            "mib":                  integer,
            "blocks":               integer,
            "sectors":              integer,
            "id":                   string,
            "system":               string,
            "type":                 string
          }
        ]
      }
    ]

Examples:

    # sfdisk -l | jc --sfdisk -p
    [
      {
        "disk": "/dev/sda",
        "cylinders": 2610,
        "heads": 255,
        "sectors_per_track": 63,
        "units": "cylinders of 8225280 bytes, blocks of 1024 bytes, counting from 0",
        "partitions": [
          {
            "device": "/dev/sda1",
            "boot": true,
            "start": 0,
            "end": 130,
            "cyls": 131,
            "blocks": 1048576,
            "id": "83",
            "system": "Linux"
          },
          {
            "device": "/dev/sda2",
            "boot": false,
            "start": 130,
            "end": 2610,
            "cyls": 2481,
            "blocks": 19921920,
            "id": "8e",
            "system": "Linux LVM"
          },
          {
            "device": "/dev/sda3",
            "boot": false,
            "start": 0,
            "end": null,
            "cyls": 0,
            "blocks": 0,
            "id": "0",
            "system": "Empty"
          },
          {
            "device": "/dev/sda4",
            "boot": false,
            "start": 0,
            "end": null,
            "cyls": 0,
            "blocks": 0,
            "id": "0",
            "system": "Empty"
          }
        ]
      },
      {
        "disk": "/dev/mapper/centos-root",
        "cylinders": 2218,
        "heads": 255,
        "sectors_per_track": 63
      },
      {
        "disk": "/dev/mapper/centos-swap",
        "cylinders": 261,
        "heads": 255,
        "sectors_per_track": 63
      }
    ]

    # sfdisk -l | jc --sfdisk -p -r
    [
      {
        "disk": "/dev/sda",
        "cylinders": "2610",
        "heads": "255",
        "sectors_per_track": "63",
        "units": "cylinders of 8225280 bytes, blocks of 1024 bytes, counting from 0",
        "partitions": [
          {
            "device": "/dev/sda1",
            "boot": "*",
            "start": "0+",
            "end": "130-",
            "cyls": "131-",
            "blocks": "1048576",
            "id": "83",
            "system": "Linux"
          },
          {
            "device": "/dev/sda2",
            "boot": null,
            "start": "130+",
            "end": "2610-",
            "cyls": "2481-",
            "blocks": "19921920",
            "id": "8e",
            "system": "Linux LVM"
          },
          {
            "device": "/dev/sda3",
            "boot": null,
            "start": "0",
            "end": "-",
            "cyls": "0",
            "blocks": "0",
            "id": "0",
            "system": "Empty"
          },
          {
            "device": "/dev/sda4",
            "boot": null,
            "start": "0",
            "end": "-",
            "cyls": "0",
            "blocks": "0",
            "id": "0",
            "system": "Empty"
          }
        ]
      },
      {
        "disk": "/dev/mapper/centos-root",
        "cylinders": "2218",
        "heads": "255",
        "sectors_per_track": "63"
      },
      {
        "disk": "/dev/mapper/centos-swap",
        "cylinders": "261",
        "heads": "255",
        "sectors_per_track": "63"
      }
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`sfdisk` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['sfdisk']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = ['cylinders', 'heads', 'sectors_per_track', 'start', 'end', 'cyls', 'mib',
                'blocks', 'sectors', 'bytes', 'logical_sector_size', 'physical_sector_size',
                'min_io_size', 'optimal_io_size', 'free_bytes', 'free_sectors']
    bool_list = ['boot']

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key].replace('-', ''))

        if 'partitions' in entry:
            for p in entry['partitions']:
                for key in p:
                    # legacy conversion for -d option
                    if key == 'size':
                        if p[key].isnumeric():
                            p[key] = jc.utils.convert_to_int(p[key])

                    # normal conversions
                    if key in int_list:
                        p[key] = jc.utils.convert_to_int(p[key].replace('-', ''))
                    if key in bool_list:
                        p[key] = jc.utils.convert_to_bool(p[key])

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []
    item = {}
    partitions = []
    option = ''
    section = ''

    if jc.utils.has_data(data):

        for line in data.splitlines():
            # deprecated - only for older versions of util-linux
            if line.startswith('# partition table of'):
                if item:
                    raw_output.append(item)

                item = {}
                partitions = []
                option = 'd'
                item['disk'] = line.split()[4]
                continue

            # deprecated - only for older versions of util-linux
            if option == 'd':
                if line.startswith('unit: '):
                    item['units'] = line.split()[1]
                    section = 'partitions'
                    continue

                if section == 'partitions' and line:
                    part = {}
                    part['device'] = line.split()[0]
                    line = line.replace(',', ' ').replace('=', ' ')
                    part['start'] = line.split()[3]
                    part['size'] = line.split()[5]
                    part['id'] = line.split()[7]
                    part['boot'] = '*' if 'bootable' in line else None
                    partitions.append(part)
                    item['partitions'] = partitions
                    continue

            else:
                # older versions of util-linux
                # Disk /dev/sda: 2610 cylinders, 255 heads, 63 sectors/track
                if line.startswith('Disk ') and 'sectors/track' in line:
                    if item:
                        raw_output.append(item)

                    item = {}
                    partitions = []
                    line = line.replace(':', '').replace(',', '')
                    fields = line.split()
                    item['disk'] = fields[1]
                    item['cylinders'] = fields[2]
                    item['heads'] = fields[4]
                    item['sectors_per_track'] = fields[6]
                    continue

                # util-linux v2.32.0+ (?)
                # Disk /dev/sda: 20 GiB, 21474836480 bytes, 41943040 sectors
                if line.startswith('Disk ') and line.endswith('sectors'):
                    if item:
                        raw_output.append(item)

                    item = {}
                    partitions = []
                    line = line.replace(':', '').replace(',', '')
                    fields = line.split()
                    item['disk'] = fields[1]
                    item['disk_size'] = ' '.join(fields[2:4])
                    item['bytes'] = fields[4]
                    item['sectors'] = fields[6]
                    continue

                if line.startswith('Disk model: '):
                    item['disk_model'] = line.split(':', maxsplit=1)[1].strip()
                    continue

                if line.startswith('Sector size (logical/physical)'):
                    fields = line.split()
                    item['logical_sector_size'] = fields[3]
                    item['physical_sector_size'] = fields[6]
                    continue

                if line.startswith('I/O size (minimum/optimal)'):
                    fields = line.split()
                    item['min_io_size'] = fields[3]
                    item['optimal_io_size'] = fields[6]
                    continue

                if line.startswith('Disklabel type'):
                    item['disk_label_type'] = line.split(':', maxsplit=1)[1].strip()
                    continue

                if line.startswith('Disk identifier'):
                    item['disk_identifier'] = line.split(':', maxsplit=1)[1].strip()
                    continue

                if line.startswith('Units: '):
                    item['units'] = line.split(':')[1].strip()
                    continue

                # sfdisk -F
                if line.startswith('Unpartitioned space'):
                    line = line.replace(':', '').replace(',', '')
                    fields = line.split()
                    item['disk'] = fields[2]
                    item['free_disk_size'] = ' '.join(fields[3:5])
                    item['free_bytes'] = fields[5]
                    item['free_sectors'] = fields[7]
                    continue

                # partition lines
                if 'Start' in line and 'End' in line and ('Sectors' in line or 'Device' in line):
                    section = 'partitions'
                    partitions.append(line.lower().replace('#', ' '))
                    continue

                if section == 'partitions' and line:
                    partitions.append(line)
                    continue

                if section == 'partitions' and line == '':
                    item['partitions'] = jc.parsers.universal.sparse_table_parse(partitions)
                    section = ''
                    partitions = []
                    continue

        # get final partitions if there are any left over
        if section == 'partitions' and option != 'd' and partitions:
            item['partitions'] = jc.parsers.universal.sparse_table_parse(partitions)

        if item:
            raw_output.append(item)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
