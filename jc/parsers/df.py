r"""jc - JSON Convert `df` command output parser

Values are normalized to bytes when using `df -h`.

Usage (cli):

    $ df | jc --df

or

    $ jc df

Usage (module):

    import jc
    result = jc.parse('df', df_command_output)

Schema:

    [
      {
        "filesystem":        string,
        "size":              integer,
        "1k_blocks":         integer,
        "512_blocks":        integer,
        "used":              integer,
        "available":         integer,
        "capacity_percent":  integer,
        "ifree":             integer,
        "iused":             integer,
        "use_percent":       integer,
        "iused_percent":     integer,
        "mounted_on":        string
      }
    ]

Examples:

    $ df | jc --df -p
    [
      {
        "filesystem": "devtmpfs",
        "1k_blocks": 1918820,
        "used": 0,
        "available": 1918820,
        "use_percent": 0,
        "mounted_on": "/dev"
      },
      {
        "filesystem": "tmpfs",
        "1k_blocks": 1930668,
        "used": 0,
        "available": 1930668,
        "use_percent": 0,
        "mounted_on": "/dev/shm"
      },
      {
        "filesystem": "tmpfs",
        "1k_blocks": 1930668,
        "used": 11800,
        "available": 1918868,
        "use_percent": 1,
        "mounted_on": "/run"
      },
      ...
    ]

    $ df | jc --df -p -r
    [
      {
        "filesystem": "devtmpfs",
        "1k_blocks": "1918820",
        "used": "0",
        "available": "1918820",
        "use_percent": "0%",
        "mounted_on": "/dev"
      },
      {
        "filesystem": "tmpfs",
        "1k_blocks": "1930668",
        "used": "0",
        "available": "1930668",
        "use_percent": "0%",
        "mounted_on": "/dev/shm"
      },
      {
        "filesystem": "tmpfs",
        "1k_blocks": "1930668",
        "used": "11800",
        "available": "1918868",
        "use_percent": "1%",
        "mounted_on": "/run"
      },
      ...
    ]
"""
import hashlib
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.1'
    description = '`df` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['df']
    tags = ['command']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema:
    """
    int_list = {'use_percent', 'capacity_percent', 'ifree', 'iused', 'iused_percent'}
    size_list = {'size', 'used', 'available'}
    posix_mode = False

    for entry in proc_data:
        if 'avail' in entry:
            entry['available'] = entry.pop('avail')

        if 'use%' in entry:
            entry['use_percent'] = entry.pop('use%')
            posix_mode = True

        if 'capacity' in entry:
            entry['capacity_percent'] = entry.pop('capacity')

        if '%iused' in entry:
            entry['iused_percent'] = entry.pop('%iused')

        # change any entry for key with '_blocks' in the name to int
        for k in entry:
            if '_blocks' in str(k):
                entry[k] = jc.utils.convert_to_int(entry[k])

        # remove percent sign from 'use_percent', 'capacity_percent', and 'iused_percent'
        if 'use_percent' in entry:
            entry['use_percent'] = entry['use_percent'].rstrip('%')

        if 'capacity_percent' in entry:
            entry['capacity_percent'] = entry['capacity_percent'].rstrip('%')

        if 'iused_percent' in entry:
            entry['iused_percent'] = entry['iused_percent'].rstrip('%')

        # parse the size, used, and available fields to bytes
        for key in entry:
            if key in size_list:
                entry[key] = jc.utils.convert_size_to_int(entry[key], posix_mode=posix_mode)

        # convert integers
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def _long_filesystem_hash(header, line):
    """
    Returns truncated hash and value of the filesystem field if it is too
    long for the column.
    """
    filesystem_field = line.split()[0]

    # get length of filesystem column
    space_count = 0
    for char in header[10:]:
        if char == ' ':
            space_count += 1
            continue

        break

    filesystem_col_len = space_count + 9

    # return the hash and value if the field data is longer than the column length
    if len(filesystem_field) > filesystem_col_len:
        truncated_hash = hashlib.sha256(filesystem_field.encode('utf-8')).hexdigest()[:filesystem_col_len]
        return truncated_hash, filesystem_field

    return None, None


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

    # remove blank lines
    cleandata = list(filter(None, data.splitlines()))

    fix_data = []
    raw_output = []
    filesystem_map = {}

    if jc.utils.has_data(data):

        # fix headers
        cleandata[0] = cleandata[0].lower()
        cleandata[0] = cleandata[0].replace('-', '_')
        cleandata[0] = cleandata[0].replace('mounted on', 'mounted_on')

        # fix long filesystem data in some older versions of df
        header = cleandata[0]
        fix_data.append(header)
        for line in cleandata[1:]:
            field_hash, field_value = _long_filesystem_hash(header, line)
            if field_hash:
                filesystem_map.update({field_hash: field_value})
                newline = line.replace(field_value, field_hash)
                fix_data.append(newline)
            else:
                fix_data.append(line)

        # parse the data
        raw_output = jc.parsers.universal.sparse_table_parse(fix_data)

        # replace hash values with real values to fix long filesystem data
        # in some older versions of df
        for item in raw_output:
            if 'filesystem' in item:
                if item['filesystem'] in filesystem_map:
                    item['filesystem'] = filesystem_map[item['filesystem']]

    return raw_output if raw else _process(raw_output)
