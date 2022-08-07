"""jc - JSON Convert `mdadm` command output parser

<<Short mdadm description and caveats>>

Usage (cli):

    $ mdadm | jc --mdadm

    or

    $ jc mdadm

Usage (module):

    import jc
    result = jc.parse('mdadm', mdadm_command_output)

Schema:

    [
      {
        "mdadm":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ mdadm | jc --mdadm -p
    []

    $ mdadm | jc --mdadm -p -r
    []
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import sparse_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`mdadm` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['mdadm']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'array_size_num', 'used_dev_size_num', 'raid_devices', 'total_devices',
                'active_devices', 'working_devices', 'failed_devices', 'spare_devices',
                'events', 'number', 'major', 'minor', 'raid_device', 'avail_dev_size_num',
                'data_offset', 'super_offset', 'unused_space_before', 'unused_space_after',
                'chunk_size', 'preferred_minor', 'check_status_percent', 'resync_status_percent'}

    array_state_map = {
        'A': 'active',
        '.': 'missing',
        'R': 'replacing'
    }

    # split combined values
    if 'array_size' in proc_data:
        proc_data['array_size_num'] = proc_data['array_size'].split(maxsplit=1)[0]

    if 'used_dev_size' in proc_data:
        proc_data['used_dev_size_num'] = proc_data['used_dev_size'].split(maxsplit=1)[0]

    if 'avail_dev_size' in proc_data:
        proc_data['avail_dev_size_num'] = proc_data['avail_dev_size'].split(maxsplit=1)[0]

    if 'data_offset' in proc_data:
        proc_data['data_offset'] = proc_data['data_offset'].split()[0]

    if 'super_offset' in proc_data:
        proc_data['super_offset'] = proc_data['super_offset'].split()[0]

    if 'unused_space' in proc_data:
        unused_space_list = proc_data['unused_space'].split(',')
        before_text = unused_space_list[0].strip()
        after_text = unused_space_list[1].strip()
        before = before_text.split('=')[1].split()[0]
        after = after_text.split('=')[1].split()[0]
        proc_data['unused_space_before'] = before
        proc_data['unused_space_after'] = after

    if 'name' in proc_data:
        proc_data['name_val'] = proc_data['name'].split(maxsplit=1)[0]

    if 'checksum' in proc_data:
        proc_data['checksum_val'] = proc_data['checksum'].split(maxsplit=1)[0]
        proc_data['checksum_state'] = proc_data['checksum'].split()[-1]

    if 'state' in proc_data:
        state_list = [x.strip() for x in proc_data['state'].split(',')]
        proc_data['state_list'] = state_list

    if 'flags' in proc_data:
        proc_data['flag_list'] = proc_data['flags'].split()

    if 'array_state' in proc_data:
        array_state_list = []
        array_state_text = proc_data['array_state'].split(maxsplit=1)[0]

        for item in array_state_text:
            array_state_list.append(array_state_map[item])

        proc_data['array_state_list'] = array_state_list

    if 'resync_status' in proc_data:
        proc_data['resync_status_percent'] = proc_data['resync_status'].split('%')[0]

    if 'check_status' in proc_data:
        proc_data['check_status_percent'] = proc_data['check_status'].split('%')[0]

    # add timestamp fields
    if 'creation_time' in proc_data:
        dt = jc.utils.timestamp(proc_data['creation_time'], format_hint=(1000,))
        proc_data['creation_time_epoch'] = dt.naive

    if 'update_time' in proc_data:
        dt = jc.utils.timestamp(proc_data['update_time'], format_hint=(1000,))
        proc_data['update_time_epoch'] = dt.naive

    # convert ints
    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc .utils.convert_to_int(proc_data[key])

    # table items
    if 'device_table' in proc_data:
        for item in proc_data['device_table']:
            if 'state' in item:
                item['state'] = item['state'].split()

            # convert ints
            for key in item:
                if key in int_list:
                    item[key] = jc.utils.convert_to_int(item[key])

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
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

    raw_output = {}
    device_table = False
    device_table_list = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            # device line
            if line.startswith('/') and line.endswith(':'):
                raw_output['device'] = line[:-1]
                continue

            # key/value lines
            if ' : ' in line:
                key, value = line.split(' : ')
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                raw_output[key] = value
                continue

            # device table header
            if '    Number   Major   Minor   RaidDevice State' in line:
                device_table_list.append('    number   major   minor   RaidDevice state         device')
                device_table = True
                continue

            # device table lines
            if device_table == True:
                device_table_list.append(line)
                continue

        if device_table_list:
            d_table = sparse_table_parse(device_table_list)
            for item in d_table:
                if 'RaidDevice' in item:
                    item['raid_device'] = item.pop('RaidDevice')

            raw_output['device_table'] = d_table



    return raw_output if raw else _process(raw_output)
