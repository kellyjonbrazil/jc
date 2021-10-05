"""jc - JSON CLI output utility `lsusb` command output parser

<<Short lsusb description and caveats>>

Usage (cli):

    $ lsusb -v | jc --lsusb

    or

    $ jc lsusb -v

Usage (module):

    import jc.parsers.lsusb
    result = jc.parsers.lsusb.parse(lsusb_command_output)

Schema:

    [
      {
        "lsusb":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ lsusb | jc --lsusb -p
    []

    $ lsusb | jc --lsusb -p -r
    []
"""
import jc.utils
from jc.parsers.universal import sparse_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`lsusb` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['lsusb']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool conversions and timestamps

    return proc_data


def _count_indent(line):
    indent = 0
    for char in line:
        if char == ' ':
            indent += 1
            continue
        else:
            break
    return indent


def _add_attributes(line):
    indent = _count_indent(line)
    # section header is formatted with the correct spacing to be used with jc.parsers.universal.sparse_table_parse()
    # pad end of string to be at least len of 25
    section_header = 'key                   val description'

    line_obj = [section_header, line.strip() + (' ' * 25)]
    line_obj = sparse_table_parse(line_obj)
    line_obj[0].update({'indent': indent})

    return line_obj[0]


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
    output_line = {}
    section = ''
    device_descriptor_list = []
    configuration_descriptor_list = []
    interface_descriptor_list = []
    cdc_header_list = []
    cdc_call_management_list = []
    cdc_acm_list = []
    cdc_union_list = []
    endpoint_descriptor_list = []
    hid_device_descriptor_list = []
    report_descriptors_list = []
    hub_descriptor_list = []
    hub_port_status_list = []

    if jc.utils.has_data(data):

        for line in data.splitlines():
            # blank line: new object
            if not line:
                if endpoint_descriptor_list:
                    interface_descriptor_list.append({'endpoint_descriptor': endpoint_descriptor_list})

                if report_descriptors_list:
                    pass

                if output_line:
                    raw_output.append(output_line)

                output_line = {}
                device_descriptor_list = []
                configuration_descriptor_list = []
                interface_descriptor_list = []
                cdc_header_list = []
                cdc_call_management_list = []
                cdc_acm_list = []
                cdc_union_list = []
                endpoint_descriptor_list = []
                hid_device_descriptor_list = []
                report_descriptors_list = []
                hub_descriptor_list = []
                hub_port_status_list = []
                section = ''
                continue

            # sections
            if line.startswith('Bus '):
                if output_line:
                    raw_output.append(output_line)

                output_line = {}
                device_descriptor_list = []
                configuration_descriptor_list = []
                interface_descriptor_list = []
                cdc_header_list = []
                cdc_call_management_list = []
                cdc_acm_list = []
                cdc_union_list = []
                endpoint_descriptor_list = []
                hid_device_descriptor_list = []
                report_descriptors_list = []
                hub_descriptor_list = []
                hub_port_status_list = []
                section = 'bus'

                line_split = line.strip().split(maxsplit=6)
                output_line.update(
                    {
                        'bus': line_split[1],
                        'device': line_split[3][:-1],
                        'id': line_split[5],
                        'description': (line_split[6:7] or [None])[0]     # way to get a list item or None
                    }
                )
                continue

            if line.startswith('Device Descriptor:'):
                section = 'device_descriptor'
                device_descriptor_list = []
                configuration_descriptor_list = []
                interface_descriptor_list = []
                cdc_header_list = []
                cdc_call_management_list = []
                cdc_acm_list = []
                cdc_union_list = []
                endpoint_descriptor_list = []
                hid_device_descriptor_list = []
                report_descriptors_list = []
                hub_descriptor_list = []
                hub_port_status_list = []
                continue

            if line.startswith('  Configuration Descriptor:'):
                section = 'configuration_descriptor'
                configuration_descriptor_list = []
                interface_descriptor_list = []
                continue

            if line.startswith('    Interface Descriptor:'):
                section = 'interface_descriptor'

                if cdc_header_list:
                    interface_descriptor_list.append({'cdc_header': cdc_header_list})

                if cdc_call_management_list:
                    interface_descriptor_list.append({'cdc_call_management': cdc_call_management_list})

                if cdc_acm_list:
                    interface_descriptor_list.append({'cdc_acm': cdc_acm_list})

                if cdc_union_list:
                    interface_descriptor_list.append({'cdc_union': cdc_union_list})

                if endpoint_descriptor_list:
                    interface_descriptor_list.append({'endpoint_descriptor': endpoint_descriptor_list})

                if interface_descriptor_list:
                    if 'interface_descriptor' not in output_line['device_descriptor']['configuration_descriptor']:
                        output_line['device_descriptor']['configuration_descriptor']['interface_descriptor'] = []
                    output_line['device_descriptor']['configuration_descriptor']['interface_descriptor'].append(interface_descriptor_list)

                cdc_header_list = []
                cdc_call_management_list = []
                cdc_acm_list = []
                cdc_union_list = []
                endpoint_descriptor_list = []
                interface_descriptor_list = []
                continue

            if line.startswith('      CDC Header:'):
                section = 'cdc_header'
                cdc_header_list = []
                continue

            if line.startswith('      CDC Call Management:'):
                section = 'cdc_call_management'
                cdc_call_management_list = []
                continue

            if line.startswith('      CDC ACM:'):
                section = 'cdc_acm'
                cdc_acm_list = []
                continue

            if line.startswith('      CDC Union:'):
                section = 'cdc_union'
                cdc_union_list = []
                continue

            if line.startswith('      Endpoint Descriptor:'):
                section = 'endpoint_descriptor'
                if endpoint_descriptor_list:
                    interface_descriptor_list.append({'endpoint_descriptor': endpoint_descriptor_list})
                endpoint_descriptor_list = []
                continue

            if line.startswith('        HID Device Descriptor:'):
                section = 'hid_device_descriptor'
                hid_device_descriptor_list = []
                continue

            if line.startswith('         Report Descriptors:'):
                section = 'report_descriptors'
                report_descriptors_list = []
                continue

            if line.startswith('Hub Descriptor:'):
                section = 'hub_descriptor'
                hub_descriptor_list = []
                continue

            if line.startswith(' Hub Port Status:'):
                section = 'hub_port_status'
                hub_port_status_list = []
                continue

            if line.startswith('Device Status:'):
                section = 'device_status'
                line_split = line.strip().split(':', maxsplit=1)
                output_line.update(
                    {
                        'device_status':
                            {
                                'value': line_split[1].strip()
                            }
                    }
                )
                continue

            # create section lists and schema
            if section == 'device_descriptor' and line.startswith(' '):
                device_descriptor_list.append(_add_attributes(line))
                if 'device_descriptor' not in output_line:
                    output_line['device_descriptor'] = {}
                output_line['device_descriptor']['attributes'] = device_descriptor_list
                continue

            if section == 'configuration_descriptor' and line.startswith(' '):
                configuration_descriptor_list.append(_add_attributes(line))
                if 'configuration_descriptor' not in output_line['device_descriptor']:
                    output_line['device_descriptor']['configuration_descriptor'] = {}
                output_line['device_descriptor']['configuration_descriptor']['attributes'] = configuration_descriptor_list
                continue

            if section == 'interface_descriptor' and line.startswith(' '):
                interface_descriptor_list.append(_add_attributes(line))

                if cdc_header_list:
                    interface_descriptor_list.append({'cdc_header': cdc_header_list})

                if cdc_call_management_list:
                    interface_descriptor_list.append({'cdc_call_management': cdc_call_management_list})

                if cdc_acm_list:
                    interface_descriptor_list.append({'cdc_acm': cdc_acm_list})

                if cdc_union_list:
                    interface_descriptor_list.append({'cdc_union': cdc_union_list})

                if endpoint_descriptor_list:
                    interface_descriptor_list.append({'endpoint_descriptor': endpoint_descriptor_list})

                if interface_descriptor_list:
                    if 'interface_descriptor_list' not in output_line['device_descriptor']['configuration_descriptor']:
                        output_line['device_descriptor']['configuration_descriptor']['interface_descriptor'] = []
                    output_line['device_descriptor']['configuration_descriptor']['interface_descriptor'].append(interface_descriptor_list)

                    cdc_header_list = []
                    cdc_call_management_list = []
                    cdc_acm_list = []
                    cdc_union_list = []
                    endpoint_descriptor_list = []

                continue

            if section == 'cdc_header' and line.startswith(' '):
                cdc_header_list.append(_add_attributes(line))
                continue

            if section == 'cdc_call_management' and line.startswith(' '):
                cdc_call_management_list.append(_add_attributes(line))
                continue

            if section == 'cdc_acm' and line.startswith(' '):
                cdc_acm_list.append(_add_attributes(line))
                continue

            if section == 'cdc_union' and line.startswith(' '):
                cdc_union_list.append(_add_attributes(line))
                continue

            if section == 'endpoint_descriptor' and line.startswith(' '):
                if hid_device_descriptor_list:
                    endpoint_descriptor_list.append({'hid_device_descriptor': hid_device_descriptor_list})

                hid_device_descriptor_list = []
                endpoint_descriptor_list.append(_add_attributes(line))
                continue

            if section == 'hid_device_descriptor' and line.startswith(' '):
                if report_descriptors_list:
                    hid_device_descriptor_list.append({'report_descriptors': report_descriptors_list})

                report_descriptors_list = []
                hid_device_descriptor_list.append(_add_attributes(line))
                continue

            if section == 'report_descriptors' and line.startswith(' '):
                report_descriptors_list.append(_add_attributes(line))
                continue

            if section == 'hub_descriptor' and line.startswith(' '):
                hub_descriptor_list.append(_add_attributes(line))
                if 'hub_descriptor' not in output_line:
                    output_line['hub_descriptor'] = {}
                output_line['hub_descriptor']['attributes'] = hub_descriptor_list
                continue

            if section == 'hub_port_status' and line.startswith(' '):
                hub_port_status_list.append(_add_attributes(line))
                output_line['hub_descriptor']['hub_port_status'] = hub_port_status_list
                continue

    if output_line:
        raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
