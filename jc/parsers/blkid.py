r"""jc - JSON Convert `blkid` command output parser

Usage (cli):

    $ blkid | jc --blkid

or

    $ jc blkid

Usage (module):

    import jc
    result = jc.parse('blkid', blkid_command_output)

Schema:

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
import re
import jc.utils
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = '`blkid` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['blkid']
    tags = ['command']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    int_list = {
        'part_entry_number', 'part_entry_offset', 'part_entry_size', 'id_part_entry_number',
        'id_part_entry_offset', 'id_part_entry_size', 'minimum_io_size', 'physical_sector_size',
        'logical_sector_size', 'id_iolimit_minimum_io_size', 'id_iolimit_physical_sector_size',
        'id_iolimit_logical_sector_size'
    }

    for entry in proc_data:
        if 'devname' in entry:
            entry['device'] = entry.pop('devname')

        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


_UNESCAPE_RE = re.compile(r'\\(["\\])')


def _word_start(line, end):
    """Index where the word ending at line[end - 1] starts"""
    while end > 0 and line[end - 1] not in ' \t':
        end -= 1
    return end


def _parse_device_line(line):
    r"""
    Parse a `DEVICE: NAME="value" NAME="value" ...` line.

    blkid escapes `"` and `\` inside of values with a backslash, but prints
    the 0x1c and 0x9c characters as `^\` and `M-^\` without escaping that
    backslash. A `"` inside of a value always follows a backslash, so `="`
    can only start a value. The line is read from the end: the last `="`
    before a closing `"` starts that value. Unquoted `NAME=value` and
    single-quoted `NAME='value'` words are also accepted.
    """
    tags = []
    end = len(line)

    while True:
        while end > 0 and line[end - 1] in ' \t':
            end -= 1

        if end == 0:
            break

        if line[end - 1] == '"':
            value_start = line.rfind('="', 0, end - 1)
            if value_start == -1:
                raise ParseError('Unable to parse blkid line: ' + line)
            key_start = _word_start(line, value_start)
            value = _UNESCAPE_RE.sub(r'\1', line[value_start + 2:end - 1])

        elif line[end - 1] == "'" and line.rfind("='", 0, end - 1) != -1:
            # hand-written single-quoted value
            value_start = line.rfind("='", 0, end - 1)
            key_start = _word_start(line, value_start)
            value = line[value_start + 2:end - 1]

        else:
            key_start = _word_start(line, end)
            value_start = line.find('=', key_start, end)
            if value_start == -1 or key_start == 0:
                # no more NAME=value words: the rest is the device name
                break
            value = line[value_start + 1:end]

        if key_start == 0:
            raise ParseError('Unable to parse blkid line: ' + line)

        tags.append((line[key_start:value_start].lower(), value))
        end = key_start

    device = line[:end].lstrip(' \t')
    if not device.endswith(':'):
        raise ParseError('Unable to parse blkid line: ' + line)

    output_line = {'device': device[:-1]}
    for key, value in reversed(tags):
        output_line[key] = value

    return output_line


_TAG_START_RE = re.compile(r'[A-Z0-9_]+="')
_KEY_VALUE_RE = re.compile(r'[A-Z0-9_]+=')


def _is_device_format(data):
    """
    True for the default `DEVICE: KEY="value" ...` format, False for the
    `KEY=value` lines of `-o udev` and `-o export`. A value or a device name
    can contain `:` and spaces, so look at the structure of the first line.
    """
    first_line = ''
    for line in jc.utils.splitlines(data):
        if line.strip():
            first_line = line.strip()
            break

    # the device ends at the first `: ` and a quoted tag follows
    colon = first_line.find(': ')
    if colon != -1 and _TAG_START_RE.match(first_line, colon + 2):
        return True

    if _KEY_VALUE_RE.match(first_line):
        return False

    return first_line.split(maxsplit=1)[0].endswith(':')


def parse(data, raw=False, quiet=False):
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

    if jc.utils.has_data(data):

        # if the first line starts with a device, use normal parsing:
        if _is_device_format(data):
            linedata = jc.utils.splitlines(data)

            for line in linedata:
                if not line.strip(' \t'):
                    continue

                raw_output.append(_parse_device_line(line))

        # else use key/value per line parsing
        else:
            linedata = jc.utils.splitlines(data)
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
        return _process(raw_output)
