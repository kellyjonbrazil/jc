"""jc - JSON CLI output utility `hciconfig` command output parser

Usage (cli):

    $ hciconfig | jc --hciconfig

    or

    $ jc hciconfig

Usage (module):

    import jc.parsers.hciconfig
    result = jc.parsers.hciconfig.parse(hciconfig_command_output)

Schema:

    [
      {
        "device":               string,
        "type":                 string,
        "bus":                  string,
        "bd_address":           string,
        "acl_mtu":              integer,
        "acl_mtu_packets":      integer,
        "sco_mtu":              integer,
        "sco_mtu_packets":      integer,
        "state": [
                                string
        ],
        "rx_bytes":             integer,
        "rx_acl":               integer,
        "rx_sco":               integer,
        "rx_events":            integer,
        "rx_errors":            integer,
        "tx_bytes":             integer,
        "tx_acl":               integer,
        "tx_sco":               integer,
        "tx_commands":          integer,
        "tx_errors":            integer,
        "features": [
                                string
        ],
        "packet_type": [
                                string
        ],
        "link_policy": [
                                string
        ],
        "link_mode": [
                                string
        ],
        "name":                 string,
        "class":                string,
        "service_classes": [
                                string       # 'Unspecified' is null
        ],
        "device_class":         string,
        "hci_version":          string,
        "hci_revision":         string,
        "lmp_version":          string,
        "lmp_subversion":       string,
        "manufacturer":         string
      }
    ]

Examples:

    $ hciconfig -a | jc --hciconfig -p
    [
      {
        "device": "hci0",
        "type": "Primary",
        "bus": "USB",
        "bd_address": "00:1A:7D:DA:71:13",
        "acl_mtu": 310,
        "acl_mtu_packets": 10,
        "sco_mtu": 64,
        "sco_mtu_packets": 8,
        "state": [
          "UP",
          "RUNNING"
        ],
        "rx_bytes": 13905869,
        "rx_acl": 0,
        "rx_sco": 0,
        "rx_events": 393300,
        "rx_errors": 0,
        "tx_bytes": 62629,
        "tx_acl": 0,
        "tx_sco": 0,
        "tx_commands": 3893,
        "tx_errors": 0,
        "features": [
          "0xff",
          "0xff",
          "0x8f",
          "0xfe",
          "0xdb",
          "0xff",
          "0x5b",
          "0x87"
        ],
        "packet_type": [
          "DM1",
          "DM3",
          "DM5",
          "DH1",
          "DH3",
          "DH5",
          "HV1",
          "HV2",
          "HV3"
        ],
        "link_policy": [
          "RSWITCH",
          "HOLD",
          "SNIFF",
          "PARK"
        ],
        "link_mode": [
          "SLAVE",
          "ACCEPT"
        ],
        "name": "CSR8510 A10",
        "class": "0x000000",
        "service_classes": null,
        "device_class": "Miscellaneous",
        "hci_version": "4.0 (0x6)",
        "hci_revision": "0x22bb",
        "lmp_version": "4.0 (0x6)",
        "lmp_subversion": "0x22bb",
        "manufacturer": "Cambridge Silicon Radio (10)"
      },
      {
        "device": "hci1",
        "type": "Primary",
        "bus": "USB",
        "bd_address": "00:1A:7D:DA:71:13",
        "acl_mtu": 310,
        "acl_mtu_packets": 10,
        "sco_mtu": 64,
        "sco_mtu_packets": 8,
        "state": [
          "DOWN"
        ],
        "rx_bytes": 4388363,
        "rx_acl": 0,
        "rx_sco": 0,
        "rx_events": 122021,
        "rx_errors": 0,
        "tx_bytes": 52350,
        "tx_acl": 0,
        "tx_sco": 0,
        "tx_commands": 3480,
        "tx_errors": 2,
        "features": [
          "0xff",
          "0xff",
          "0x8f",
          "0xfe",
          "0xdb",
          "0xff",
          "0x5b",
          "0x87"
        ],
        "packet_type": [
          "DM1",
          "DM3",
          "DM5",
          "DH1",
          "DH3",
          "DH5",
          "HV1",
          "HV2",
          "HV3"
        ],
        "link_policy": [
          "RSWITCH",
          "HOLD",
          "SNIFF",
          "PARK"
        ],
        "link_mode": [
          "SLAVE",
          "ACCEPT"
        ]
      }
    ]

    $ hciconfig -a | jc --hciconfig -p -r
    [
      {
        "device": "hci0",
        "type": "Primary",
        "bus": "USB",
        "bd_address": "00:1A:7D:DA:71:13",
        "acl_mtu": "310",
        "acl_mtu_packets": "10",
        "sco_mtu": "64",
        "sco_mtu_packets": "8",
        "state": [
          "UP",
          "RUNNING"
        ],
        "rx_bytes": "13905869",
        "rx_acl": "0",
        "rx_sco": "0",
        "rx_events": "393300",
        "rx_errors": "0",
        "tx_bytes": "62629",
        "tx_acl": "0",
        "tx_sco": "0",
        "tx_commands": "3893",
        "tx_errors": "0",
        "features": [
          "0xff",
          "0xff",
          "0x8f",
          "0xfe",
          "0xdb",
          "0xff",
          "0x5b",
          "0x87"
        ],
        "packet_type": [
          "DM1",
          "DM3",
          "DM5",
          "DH1",
          "DH3",
          "DH5",
          "HV1",
          "HV2",
          "HV3"
        ],
        "link_policy": [
          "RSWITCH",
          "HOLD",
          "SNIFF",
          "PARK"
        ],
        "link_mode": [
          "SLAVE",
          "ACCEPT"
        ],
        "name": "CSR8510 A10",
        "class": "0x000000",
        "service_classes": [
          "Unspecified"
        ],
        "device_class": "Miscellaneous",
        "hci_version": "4.0 (0x6)",
        "hci_revision": "0x22bb",
        "lmp_version": "4.0 (0x6)",
        "lmp_subversion": "0x22bb",
        "manufacturer": "Cambridge Silicon Radio (10)"
      },
      {
        "device": "hci1",
        "type": "Primary",
        "bus": "USB",
        "bd_address": "00:1A:7D:DA:71:13",
        "acl_mtu": "310",
        "acl_mtu_packets": "10",
        "sco_mtu": "64",
        "sco_mtu_packets": "8",
        "state": [
          "DOWN"
        ],
        "rx_bytes": "4388363",
        "rx_acl": "0",
        "rx_sco": "0",
        "rx_events": "122021",
        "rx_errors": "0",
        "tx_bytes": "52350",
        "tx_acl": "0",
        "tx_sco": "0",
        "tx_commands": "3480",
        "tx_errors": "2",
        "features": [
          "0xff",
          "0xff",
          "0x8f",
          "0xfe",
          "0xdb",
          "0xff",
          "0x5b",
          "0x87"
        ],
        "packet_type": [
          "DM1",
          "DM3",
          "DM5",
          "DH1",
          "DH3",
          "DH5",
          "HV1",
          "HV2",
          "HV3"
        ],
        "link_policy": [
          "RSWITCH",
          "HOLD",
          "SNIFF",
          "PARK"
        ],
        "link_mode": [
          "SLAVE",
          "ACCEPT"
        ]
      }
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`hciconfig` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['hciconfig']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    for entry in proc_data:

        int_list = ['acl_mtu', 'acl_mtu_packets', 'sco_mtu', 'sco_mtu_packets', 'rx_bytes', 'rx_acl', 'rx_sco',
                    'rx_events', 'rx_errors', 'tx_bytes', 'tx_acl', 'tx_sco', 'tx_commands', 'tx_errors']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        if 'service_classes' in entry and len(entry['service_classes']) == 1 and 'Unspecified' in entry['service_classes']:
            entry['service_classes'] = None

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
    device_object = {}
    line_count = 0

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            line_count += 1

            # start of a new device object
            # hci0:   Type: Primary  Bus: USB
            if not line[0].isspace():
                if device_object:
                    raw_output.append(device_object)
                    device_object = {}
                    line_count = 1

                line = line.replace(':', '')
                line = line.split()
                device_object['device'] = line[0]
                device_object['type'] = line[2]
                device_object['bus'] = line[4]

                continue

            # BD Address: 00:50:56:E7:46:1A  ACL MTU: 8192:128  SCO MTU: 64:128
            if line[0].isspace() and line.lstrip().startswith('BD Address:'):
                line = line.split()
                device_object['bd_address'] = line[2]
                device_object['acl_mtu'] = line[5].split(':')[0]
                device_object['acl_mtu_packets'] = line[5].split(':')[1]
                device_object['sco_mtu'] = line[8].split(':')[0]
                device_object['sco_mtu_packets'] = line[8].split(':')[1]

                continue

            # UP RUNNING        (always line 3)
            if line_count == 3:
                device_object['state'] = line.split()

                continue

            # RX bytes:1307 acl:0 sco:0 events:51 errors:0
            if line[0].isspace() and line.lstrip().startswith('RX bytes:'):
                line = line.replace(':', ' ')
                line = line.split()
                device_object['rx_bytes'] = line[2]
                device_object['rx_acl'] = line[4]
                device_object['rx_sco'] = line[6]
                device_object['rx_events'] = line[8]
                device_object['rx_errors'] = line[10]

                continue

            # TX bytes:1200 acl:0 sco:0 commands:51 errors:0
            if line[0].isspace() and line.lstrip().startswith('TX bytes:'):
                line = line.replace(':', ' ')
                line = line.split()
                device_object['tx_bytes'] = line[2]
                device_object['tx_acl'] = line[4]
                device_object['tx_sco'] = line[6]
                device_object['tx_commands'] = line[8]
                device_object['tx_errors'] = line[10]

                continue

            # Features: 0xff 0xff 0x8f 0xfe 0x83 0xe1 0x08 0x80
            if line[0].isspace() and line.lstrip().startswith('Features:'):
                device_object['features'] = line.split()[1:]

                continue

            # Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3
            if line[0].isspace() and line.lstrip().startswith('Packet type:'):
                device_object['packet_type'] = line.split()[2:]

                continue

            # Link policy: RSWITCH HOLD SNIFF PARK
            if line[0].isspace() and line.lstrip().startswith('Link policy:'):
                device_object['link_policy'] = line.split()[2:]

                continue

            # Link mode: SLAVE ACCEPT
            if line[0].isspace() and line.lstrip().startswith('Link mode:'):
                device_object['link_mode'] = line.split()[2:]

                continue

            # Name: 'kbrazil-ubuntu'
            if line[0].isspace() and line.lstrip().startswith('Name:'):
                device_object['name'] = line.split(maxsplit=1)[1][1:-1]

                continue

            # Class: 0x000000
            if line[0].isspace() and line.lstrip().startswith('Class:'):
                device_object['class'] = line.split(maxsplit=1)[1]

                continue

            # Service Classes: Unspecified
            if line[0].isspace() and line.lstrip().startswith('Service Classes:'):
                device_object['service_classes'] = line.split()[2:]

                continue

            # Device Class: Miscellaneous,
            if line[0].isspace() and line.lstrip().startswith('Device Class:'):
                dev_class = line.split()[2]
                if dev_class.endswith(','):
                    dev_class = dev_class[0:-1]

                device_object['device_class'] = dev_class

                continue

            # HCI Version: 4.0 (0x6)  Revision: 0x22bb
            if line[0].isspace() and line.lstrip().startswith('HCI Version:'):
                line = line.split()
                device_object['hci_version'] = ' '.join(line[2:4])
                device_object['hci_revision'] = line[5]

                continue

            # LMP Version: 4.0 (0x6)  Subversion: 0x22bb
            if line[0].isspace() and line.lstrip().startswith('LMP Version:'):
                line = line.split()
                device_object['lmp_version'] = ' '.join(line[2:4])
                device_object['lmp_subversion'] = line[5]

                continue

            # Manufacturer: Cambridge Silicon Radio (10)
            if line[0].isspace() and line.lstrip().startswith('Manufacturer:'):
                device_object['manufacturer'] = line.split(maxsplit=1)[1]

                continue

    if device_object:
        raw_output.append(device_object)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
