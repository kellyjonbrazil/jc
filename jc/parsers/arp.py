"""jc - JSON CLI output utility arp Parser

Usage:

    specify --arp as the first argument if the piped input is coming from:

    arp
      or
    arp -a

Compatibility:

    'linux', 'aix', 'freebsd', 'darwin'

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
    version = '1.6'
    description = 'arp command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['arp']


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
            "name":       string,
            "address":    string,
            "hwtype":     string,
            "hwaddress":  string,
            "flags_mask": string,
            "iface":      string,
            "permanent":  boolean,
            "expires":    integer
          }
        ]
    """

    # in BSD style, change name to null if it is a question mark
    for entry in proc_data:
        if 'name' in entry and entry['name'] == '?':
            entry['name'] = None

        int_list = ['expires']
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
                return process(raw_output)

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
        return process(raw_output)
