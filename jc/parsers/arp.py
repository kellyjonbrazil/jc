r"""jc - JSON Convert `arp` command output parser

Supports `arp` and `arp -a` output.

Usage (cli):

    $ arp | jc --arp

or

    $ jc arp

Usage (module):

    import jc
    result = jc.parse('arp', arp_command_output)

Schema:

    [
      {
        "name":         string,
        "address":      string,
        "hwtype":       string,
        "hwaddress":    string,
        "flags_mask":   string,
        "iface":        string,
        "permanent":    boolean,
        "expires":      integer
      }
    ]

Examples:

    $ arp | jc --arp -p
    [
      {
        "address": "192.168.71.254",
        "hwtype": "ether",
        "hwaddress": "00:50:56:f0:98:26",
        "flags_mask": "C",
        "iface": "ens33"
      },
      {
        "address": "gateway",
        "hwtype": "ether",
        "hwaddress": "00:50:56:f7:4a:fc",
        "flags_mask": "C",
        "iface": "ens33"
      }
    ]

    $ arp | jc --arp -p -r
    [
      {
        "address": "gateway",
        "hwtype": "ether",
        "hwaddress": "00:50:56:f7:4a:fc",
        "flags_mask": "C",
        "iface": "ens33"
      },
      {
        "address": "192.168.71.254",
        "hwtype": "ether",
        "hwaddress": "00:50:56:fe:7a:b4",
        "flags_mask": "C",
        "iface": "ens33"
      }
    ]

    $ arp -a | jc --arp -p
    [
      {
        "name": null,
        "address": "192.168.71.254",
        "hwtype": "ether",
        "hwaddress": "00:50:56:f0:98:26",
        "iface": "ens33"
        "permanent": false,
        "expires": 1182
      },
      {
        "name": "gateway",
        "address": "192.168.71.2",
        "hwtype": "ether",
        "hwaddress": "00:50:56:f7:4a:fc",
        "iface": "ens33"
        "permanent": false,
        "expires": 110
      }
    ]

    $ arp -a | jc --arp -p -r
    [
      {
        "name": "?",
        "address": "192.168.71.254",
        "hwtype": "ether",
        "hwaddress": "00:50:56:fe:7a:b4",
        "iface": "ens33"
        "permanent": false,
        "expires": "1182"
      },
      {
        "name": "_gateway",
        "address": "192.168.71.2",
        "hwtype": "ether",
        "hwaddress": "00:50:56:f7:4a:fc",
        "iface": "ens33"
        "permanent": false,
        "expires": "110"
      }
    ]
"""
from typing import List, Dict, Any
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.12'
    description = '`arp` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['arp']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema:
    """
    int_list = {'expires'}

    # in BSD style, change name to null if it is a question mark
    for entry in proc_data:
        if 'name' in entry and entry['name'] == '?':
            entry['name'] = None

        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        # remove final Entries row if -v was used
        if cleandata[-1].startswith('Entries:'):
            cleandata.pop(-1)

        # detect if freebsd/osx style was used
        if cleandata[0][-1] == ']':
            for line in cleandata:
                splitline = line.split()
                output_line: Dict[str, Any] = {
                    'name': splitline[0],
                    'address': splitline[1].lstrip('(').rstrip(')'),
                    'hwtype': splitline[-1].lstrip('[').rstrip(']'),
                    'hwaddress': splitline[3],
                    'iface': splitline[5]
                }

                if 'permanent' in splitline:
                    output_line['permanent'] = True
                else:
                    output_line['permanent'] = False

                if 'expires' in splitline:
                    output_line['expires'] = splitline[-3]

                raw_output.append(output_line)

        # detect if linux style was used
        elif cleandata[0].startswith('Address'):

            # fix header row to change Flags Mask to flags_mask
            cleandata[0] = cleandata[0].replace('Flags Mask', 'flags_mask')
            cleandata[0] = cleandata[0].lower()

            raw_output = jc.parsers.universal.simple_table_parse(cleandata)

        # otherwise, try bsd style
        else:
            for line in cleandata:
                splitline = line.split()

                # Ignore AIX bucket information
                if 'bucket:' in splitline[0]:
                    continue
                elif 'There' in splitline[0] and 'are' in splitline[1]:
                    continue

                # AIX uses (incomplete)
                elif '<incomplete>' not in splitline and '(incomplete)' not in splitline:
                    output_line = {
                        'name': splitline[0],
                        'address': splitline[1].lstrip('(').rstrip(')'),
                        'hwtype': splitline[4].lstrip('[').rstrip(']'),
                        'hwaddress': splitline[3],
                    }
                    # Handle permanence and ignore interface in AIX
                    if 'permanent' in splitline:
                        output_line['permanent'] = True
                    elif 'in' not in splitline[6]: # AIX doesn't show interface
                        output_line['iface'] = splitline[6]

                else:
                    output_line = {
                        'name': splitline[0],
                        'address': splitline[1].lstrip('(').rstrip(')'),
                        'hwtype': None,
                        'hwaddress': None,
                    }
                    # AIX doesn't show interface
                    if len(splitline) >= 5:
                        output_line['iface'] = splitline[5]

                raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
