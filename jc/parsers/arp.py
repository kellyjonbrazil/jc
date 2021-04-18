"""jc - JSON CLI output utility `arp` command output parser

Supports `arp` and `arp -a` output.

Usage (cli):

    $ arp | jc --arp

    or

    $ jc arp

Usage (module):

    import jc.parsers.arp
    result = jc.parsers.arp.parse(arp_command_output)

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
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = '`arp` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['arp']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema:
    """

    # in BSD style, change name to null if it is a question mark
    for entry in proc_data:
        if 'name' in entry and entry['name'] == '?':
            entry['name'] = None

        int_list = ['expires']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

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
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        # remove final Entries row if -v was used
        if cleandata[-1].startswith('Entries:'):
            cleandata.pop(-1)

        # detect if freebsd/osx style was used
        if cleandata[0][-1] == ']':
            for line in cleandata:
                splitline = line.split()
                output_line = {
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

            if raw:
                return raw_output
            else:
                return _process(raw_output)

        # detect if linux style was used
        elif cleandata[0].startswith('Address'):

            # fix header row to change Flags Mask to flags_mask
            cleandata[0] = cleandata[0].replace('Flags Mask', 'flags_mask')
            cleandata[0] = cleandata[0].lower()

            raw_output = jc.parsers.universal.simple_table_parse(cleandata)

        # otherwise, try bsd style
        else:
            for line in cleandata:
                line = line.split()
                output_line = {
                    'name': line[0],
                    'address': line[1].lstrip('(').rstrip(')'),
                    'hwtype': line[4].lstrip('[').rstrip(']'),
                    'hwaddress': line[3],
                    'iface': line[6],
                }
                raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
