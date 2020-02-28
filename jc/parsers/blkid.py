"""jc - JSON CLI output utility blkid Parser

Usage:

    specify --blkid as the first argument if the piped input is coming from blkid

Compatibility:

    'linux'

Examples:

    $ blkid | jc --blkid -p
    []

    $ blkid | jc --blkid -p -r
    []
"""
import jc.utils


class info():
    version = '1.0'
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
            "device":               string,
            "uuid":                 string,
            "type":                 string,
            "usage":                string,
            "part_entry_scheme":    string,
            "part_entry_type":      string,
            "part_entry_flags":     string,
            "part_entry_number":    integer,
            "part_entry_offset":    integer,
            "part_entry_size":      integer,
            "part_entry_disk":      string
            "id_fs_uuid":           string,
            "id_fs_uuid_enc":       string,
            "id_fs_type":           string,
            "id_fs_usage":          string,
            "id_part_entry_scheme": string,
            "id_part_entry_type":   string,
            "id_part_entry_flags":  string,
            "id_part_entry_number": integer,
            "id_part_entry_offset": integer,
            "id_part_entry_size":   integer,
            "id_part_entry_disk":   string
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

    raw_output = []

    if data:
        # if the first field is a device, use normal parsing:
        if data.split(maxsplit=1)[0][-1] == ':':
            linedata = data.splitlines()

            for line in linedata:
                output_line = {}
                entries = line.split()
                output_line['device'] = entries.pop(0)[:-1]

                for entry in entries:
                    key = entry.split('=')[0].lower()
                    value = entry.split('=')[1].replace('"', '')
                    output_line[key] = value

                raw_output.append(output_line)

        # else use key/value per line parsing
        else:
            linedata = data.splitlines()
            output_line = {}
            for line in linedata:
                key = line.split('=')[0].lower()
                value = line.split('=')[1]
                output_line[key] = value

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
