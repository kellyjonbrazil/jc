"""jc - JSON CLI output utility dmidecode Parser

Usage:

    specify --dmidecode as the first argument if the piped input is coming from dmidecode

Compatibility:

    'linux'

Examples:

    $ dmidecode | jc --dmidecode -p
    []

    $ dmidecode | jc --dmidecode -p -r
    []
"""
import jc.utils


class info():
    version = '1.0'
    description = 'dmidecode command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['dmidecode']


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
            "dmidecode":     string,
            "bar":     boolean,
            "baz":     integer
          }
        ]
    """

    # rebuild output for added semantic information
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

    item_header = False
    item_values = False
    value_list = False
    item = None
    attribute = None
    values = None
    raw_output = []

    for line in filter(None, data.replace('\t', '').splitlines()):

        # header
        if line.startswith('Handle ') and line.endswith('bytes'):
            item_header = True
            item_values = False
            value_list = False

            if item:
                if values:
                    item['values'][attribute] = values
                    values = []
                raw_output.append(item)

            # Handle 0x0000, DMI type 0, 24 bytes
            header = line.replace(',', ' ').split()
            item = {
                'handle': header[1],
                'type': header[4],
                'bytes': header[5]
            }
            continue

        # description
        if item_header:
            item_header = False
            item_values = True
            value_list = False

            item['description'] = line
            item['values'] = {}
            continue

        # keys and values
        if item_values and not value_list and not line.strip().endswith(':'):
            item_header = False
            item_values = True
            value_list = False

            if values:
                item['values'][attribute] = values
                values = []

            if len(line.split(':', maxsplit=1)) == 2:
                key = line.split(':', maxsplit=1)[0].strip().lower().replace(' ', '_')
                val = line.split(':', maxsplit=1)[1].strip()
                item['values'].update({key: val})
            else:
                pass
            continue

        # back to keys and values when inside multi-line key
        if item_values and value_list and len(line.split(':', maxsplit=1)) == 2:
            item_header = False
            item_values = True
            value_list = False

            if values:
                item['values'][attribute] = values
                values = []

            key = line.split(':', maxsplit=1)[0].strip().lower().replace(' ', '_')
            val = line.split(':', maxsplit=1)[1].strip()
            item['values'].update({key: val})
            continue

        # multi-line key
        if item_values and line.strip().endswith(':'):
            item_header = False
            item_values = True
            value_list = True

            if values:
                item['values'][attribute] = values

            attribute = line[:-1].strip().lower().replace(' ', '_')
            values = []
            continue

        # multi-line values
        if value_list:
            values.append(line.strip())
            continue

    if item:
        raw_output.append(item)

    if raw:
        return raw_output
    else:
        return process(raw_output)
