"""jc - JSON CLI output utility `sfdisk` command output parser

Supports the following `sfdisk` options:
- `-l`
- `-d`
- `-uM`
- `-uC`
- `-uS`
- `-uB`

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
        "disk":                 string,
        "cylinders":            integer,
        "heads":                integer,
        "sectors_per_track":    integer,
        "units":                string,
        "partitions": [
          {
            "device":           string,
            "boot":             boolean,
            "start":            integer,
            "end":              integer,
            "size":             integer,
            "cyls":             integer,
            "mib":              integer,
            "blocks":           integer,
            "sectors":          integer,
            "id":               string,
            "system":           string
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

    # sfdisk | jc --sfdisk -p -r
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
    version = '1.0'
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
    int_list = ['cylinders', 'heads', 'sectors_per_track', 'start', 'end', 'size', 'cyls', 'mib',
                'blocks', 'sectors']
    bool_list = ['boot']

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key].replace('-', ''))

        if 'partitions' in entry:
            for p in entry['partitions']:
                for key in p:
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
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    item = {}
    partitions = []
    option = ''
    section = ''

    if jc.utils.has_data(data):

        for line in data.splitlines():
            if line.startswith('# partition table of'):
                if item:
                    raw_output.append(item)

                item = {}
                partitions = []
                option = 'd'
                item['disk'] = line.split()[4]
                continue

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
                if line.startswith('Disk '):
                    if item:
                        raw_output.append(item)

                    item = {}
                    partitions = []
                    line = line.replace(':', '').replace(',', '')
                    item['disk'] = line.split()[1]
                    item['cylinders'] = line.split()[2]
                    item['heads'] = line.split()[4]
                    item['sectors_per_track'] = line.split()[6]
                    continue

                if line.startswith('Units: '):
                    item['units'] = line.split(':')[1].strip()
                    continue

                if 'Device' in line and 'Boot' in line and 'Start' in line and 'End' in line:
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

        if item:
            raw_output.append(item)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
