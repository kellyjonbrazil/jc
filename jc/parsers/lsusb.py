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
from rich import print


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


class _LsUsb():
    def __init__(self):
        self.raw_output = []
        self.output_line = {}
        
        self.section = ''
        self.bus_idx = -1
        self.interface_descriptor_idx = -1
        self.endpoint_descriptor_idx = -1

        self.bus_list = []
        self.device_descriptor_list = []
        self.configuration_descriptor_list = []
        self.interface_association_list = []
        self.interface_descriptor_list = []
        self.interface_descriptor_attribute_list = []
        self.cdc_header_list = []
        self.cdc_call_management_list = []
        self.cdc_acm_list = []
        self.cdc_union_list = []
        self.endpoint_descriptor_list = []
        self.hid_device_descriptor_list = []
        self.report_descriptors_list = []
        self.hub_descriptor_list = []
        self.hub_port_status_list = []
        self.device_status_list = []

    @staticmethod
    def _count_indent(line):
        indent = 0
        for char in line:
            if char == ' ':
                indent += 1
                continue
            else:
                break
        return indent

    def _add_attributes(self, line):
        indent = self._count_indent(line)
        # Section header is formatted with the correct spacing to be used with
        # jc.parsers.universal.sparse_table_parse(). Pad end of string to be at least len of 25
        section_header = 'key                   val description'

        temp_obj = [section_header, line.strip() + (' ' * 25)]
        temp_obj = sparse_table_parse(temp_obj)
        temp_obj = temp_obj[0]

        line_obj = {
            temp_obj['key']: {
                'value': temp_obj['val'],
                'description': temp_obj['description'],
                '_state': {
                    'indent': indent,
                    'bus_idx': self.bus_idx,
                    'interface_descriptor_idx': self.interface_descriptor_idx,
                    'endpoint_descriptor_idx': self.endpoint_descriptor_idx
                }
            }
        }

        return line_obj

    def _set_sections(self, line):
        # ignore blank lines
        if not line:
            self.section = ''
            return True

        if line.startswith('Bus '):
            self.section = 'bus'
            self.bus_idx += 1
            self.interface_descriptor_idx = -1
            self.endpoint_descriptor_idx = -1

            # bus informatin is on the same line so need to extract data immediately
            line_split = line.strip().split(maxsplit=6)
            self.bus_list.append(
                {
                    'bus': line_split[1],
                    'device': line_split[3][:-1],
                    'id': line_split[5],
                    'description': (line_split[6:7] or [None])[0],     # way to get a list item or None
                    '_state': {
                        'bus_idx': self.bus_idx
                    }
                }
            )
            return True

        if line.startswith('Device Descriptor:'):
            self.section = 'device_descriptor'
            return True

        if line.startswith('  Configuration Descriptor:'):
            self.section = 'configuration_descriptor'
            return True

        if line.startswith('    Interface Association:'):
            self.section = 'interface_association'
            return True

        if line.startswith('    Interface Descriptor:'):
            self.section = 'interface_descriptor'
            self.interface_descriptor_idx += 1
            self.endpoint_descriptor_idx = -1
            return True

        if line.startswith('      CDC Header:'):
            self.section = 'cdc_header'
            return True

        if line.startswith('      CDC Call Management:'):
            self.section = 'cdc_call_management'
            return True

        if line.startswith('      CDC ACM:'):
            self.section = 'cdc_acm'
            return True

        if line.startswith('      CDC Union:'):
            self.section = 'cdc_union'
            return True

        if line.startswith('      Endpoint Descriptor:'):
            self.section = 'endpoint_descriptor'
            self.endpoint_descriptor_idx += 1
            return True

        if line.startswith('        HID Device Descriptor:'):
            self.section = 'hid_device_descriptor'
            return True

        if line.startswith('         Report Descriptors:'):
            self.section = 'report_descriptors'
            return True

        if line.startswith('Hub Descriptor:'):
            self.section = 'hub_descriptor'
            return True

        if line.startswith(' Hub Port Status:'):
            self.section = 'hub_port_status'
            return True

        if line.startswith('Device Status:'):
            self.section = 'device_status'

            # some device status information is displayed on the initial line so need to extract immediately
            line_split = line.strip().split(':', maxsplit=1)
            self.device_status_list.append(
                {
                    'device_status':
                        {
                            'value': line_split[1].strip(),
                            '_state': {
                                'bus_idx': self.bus_idx
                            }
                        }
                }
            )
            return True

    def _populate_lists(self, line):
        if self.section == 'device_descriptor' and line.startswith(' '):
            self.device_descriptor_list.append(self._add_attributes(line))
            return True

        if self.section == 'configuration_descriptor' and line.startswith(' '):
            self.configuration_descriptor_list.append(self._add_attributes(line))
            return True

        if self.section == 'interface_association' and line.startswith(' '):
            self.interface_association_list.append(self._add_attributes(line))
            return True

        if self.section == 'interface_descriptor' and line.startswith(' '):
            self.interface_descriptor_list.append(self._add_attributes(line))
            return True

        if self.section == 'cdc_header' and line.startswith(' '):
            self.cdc_header_list.append(self._add_attributes(line))
            return True

        if self.section == 'cdc_call_management' and line.startswith(' '):
            self.cdc_call_management_list.append(self._add_attributes(line))
            return True

        if self.section == 'cdc_acm' and line.startswith(' '):
            self.cdc_acm_list.append(self._add_attributes(line))
            return True

        if self.section == 'cdc_union' and line.startswith(' '):
            self.cdc_union_list.append(self._add_attributes(line))
            return True

        if self.section == 'hid_device_descriptor' and line.startswith(' '):
            self.report_descriptors_list.append(self._add_attributes(line))
            return True

        if self.section == 'report_descriptors' and line.startswith(' '):
            self.report_descriptors_list.append(self._add_attributes(line))
            return True

        if self.section == 'endpoint_descriptor' and line.startswith(' '):
            self.endpoint_descriptor_list.append(self._add_attributes(line))
            return True

        if self.section == 'hub_descriptor' and line.startswith(' '):
            self.hub_descriptor_list.append(self._add_attributes(line))
            return True

        if self.section == 'hub_port_status' and line.startswith(' '):
            self.hub_port_status_list.append(self._add_attributes(line))
            return True

        if self.section == 'device_status' and line.startswith(' '):
            self.device_status_list.append(self._add_attributes(line))
            return True

    def _populate_schema(self):
        """
        Schema:
        = {}
        ['device_descriptor'] = {}
        ['device_descriptor']['configuration_descriptor'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_association'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'] = []
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['attributes'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_header'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_call_management'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_adcm'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_union'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['hid_device_descriptor'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['hid_device_descriptor']['report_descriptors'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'] = []
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'][0]['attributes'] = {}
        ['hub_descriptor'] = {}
        ['hub_descriptor']['hub_port_status'] = {}
        ['device_status'] = {}
        """
        for idx, item in enumerate(self.bus_list):
            if self.output_line:
                self.raw_output.append(self.output_line)

            self.output_line = {}

            del item['_state']
            self.output_line.update(item)
            
            for dd in self.device_descriptor_list:
                keyname = list(dd.keys())[0]
                if '_state' in dd[keyname] and dd[keyname]['_state']['bus_idx'] == idx:
                    if 'device_descriptor' not in self.output_line:
                        self.output_line['device_descriptor'] = {}
                    self.output_line['device_descriptor'].update(dd)
                    del self.output_line['device_descriptor'][keyname]['_state']

            for cd in self.configuration_descriptor_list:
                keyname = list(cd.keys())[0]
                if '_state' in cd[keyname] and cd[keyname]['_state']['bus_idx'] == idx:
                    if 'configuration_descriptor' not in self.output_line['device_descriptor']:
                        self.output_line['device_descriptor']['configuration_descriptor'] = {}
                    self.output_line['device_descriptor']['configuration_descriptor'].update(cd)
                    del self.output_line['device_descriptor']['configuration_descriptor'][keyname]['_state']

            for ia in self.interface_association_list:
                keyname = list(ia.keys())[0]
                if '_state' in ia[keyname] and ia[keyname]['_state']['bus_idx'] == idx:
                    if 'interface_association' not in self.output_line['device_descriptor']['configuration_descriptor']:
                        self.output_line['device_descriptor']['configuration_descriptor']['interface_association'] = {}
                    self.output_line['device_descriptor']['configuration_descriptor']['interface_association'].update(ia)
                    del self.output_line['device_descriptor']['configuration_descriptor']['interface_association'][keyname]['_state']
            
            # add interface_descriptor key if it doesn't exist and there are entries for this bus
            if self.interface_descriptor_list:
                for iface_attrs in self.interface_descriptor_list:
                    keyname = list(iface_attrs.keys())[0]
                    if '_state' in iface_attrs[keyname] and iface_attrs[keyname]['_state']['bus_idx'] == idx:
                        if 'interface_descriptors' not in self.output_line['device_descriptor']['configuration_descriptor']:
                            self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptors'] = []

            # find max index for this bus idx, then iterate over that range
            i_desc_iters = -1
            for iface_attrs in self.interface_descriptor_list:
                keyname = list(iface_attrs.keys())[0]
                if '_state' in iface_attrs[keyname] and iface_attrs[keyname]['_state']['bus_idx'] == idx:
                    i_desc_iters = iface_attrs[keyname]['_state']['interface_descriptor_idx']

            # create the interface descriptor object
            if i_desc_iters > -1:
                for iface_idx in range(i_desc_iters + 1):
                    i_desc_obj = {}
                    for iface_attrs in self.interface_descriptor_list:
                        keyname = list(iface_attrs.keys())[0]
                        if '_state' in iface_attrs[keyname] and iface_attrs[keyname]['_state']['bus_idx'] == idx and iface_attrs[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            del iface_attrs[keyname]['_state']
                            i_desc_obj.update(iface_attrs)
                    
                    # add the object to the list of interface descriptors
                    self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptors'].append(i_desc_obj)

                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'] = []
                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_header'] = {}
                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_call_management'] = {}
                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_adcm'] = {}
                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_union'] = {}
                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['hid_device_descriptor'] = {}
                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['hid_device_descriptor']['report_descriptors'] = {}
                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'] = []
                # ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'][0]['attributes'] = {}

                for endpoint_descriptor_idx in self.endpoint_descriptor_list:
                    pass


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

    if jc.utils.has_data(data):
        s = _LsUsb()

        for line in data.splitlines():
            # sections
            if s._set_sections(line):
                continue
            
            # create section lists and schema
            if s._populate_lists(line):
                continue

#     print(f'''
# # {s.section=}
# # {s.bus_list=}
# # {s.device_descriptor_list=}
# # {s.configuration_descriptor_list=}
# # {s.interface_association_list=}
# # {s.interface_descriptor_list=}
# # {s.cdc_header_list=}
# # {s.cdc_call_management_list=}
# # {s.cdc_acm_list=}
# # {s.cdc_union_list=}
# # {s.endpoint_descriptor_list=}
# # {s.hid_device_descriptor_list=}
# # {s.report_descriptors_list=}
# # {s.hub_descriptor_list=}
# # {s.hub_port_status_list=}
# # {s.device_status_list=}
# ''')

    # populate the schema
    s._populate_schema()

    # output the raw object
    if s.output_line:
        s.raw_output.append(s.output_line)

    return s.raw_output if raw else _process(s.raw_output)
