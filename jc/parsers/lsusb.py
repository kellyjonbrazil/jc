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
        section_list_map = {
            'device_descriptor': self.device_descriptor_list,
            'configuration_descriptor': self.configuration_descriptor_list,
            'interface_association': self.interface_association_list,
            'interface_descriptor': self.interface_descriptor_list,
            'cdc_header': self.cdc_header_list,
            'cdc_call_management': self.cdc_call_management_list,
            'cdc_acm': self.cdc_acm_list,
            'cdc_union': self.cdc_union_list,
            'hid_device_descriptor': self.hid_device_descriptor_list,
            'report_descriptors': self.report_descriptors_list,
            'endpoint_descriptor': self.endpoint_descriptor_list,
            'hub_descriptor': self.hub_descriptor_list,
            'hub_port_status': self.hub_port_status_list,
            'device_status': self.device_status_list
        }

        for sec in section_list_map.keys():
            if line.startswith(' ') and self.section == sec:
                section_list_map[self.section].append(self._add_attributes(line))
                return True

    def _populate_schema(self):
        """
        Schema:
        = {}
        ['device_descriptor'] = {}
        ['device_descriptor']['configuration_descriptor'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_association'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'] = []
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_header'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_call_management'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_acm'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_union'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['hid_device_descriptor'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['hid_device_descriptor']['report_descriptors'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'] = []
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'][0] = {}
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
                keyname = tuple(dd.keys())[0]
                if '_state' in dd[keyname] and dd[keyname]['_state']['bus_idx'] == idx:
                    if 'device_descriptor' not in self.output_line:
                        self.output_line['device_descriptor'] = {}
                    self.output_line['device_descriptor'].update(dd)
                    del self.output_line['device_descriptor'][keyname]['_state']

            for cd in self.configuration_descriptor_list:
                keyname = tuple(cd.keys())[0]
                if '_state' in cd[keyname] and cd[keyname]['_state']['bus_idx'] == idx:
                    if 'configuration_descriptor' not in self.output_line['device_descriptor']:
                        self.output_line['device_descriptor']['configuration_descriptor'] = {}
                    self.output_line['device_descriptor']['configuration_descriptor'].update(cd)
                    del self.output_line['device_descriptor']['configuration_descriptor'][keyname]['_state']

            for ia in self.interface_association_list:
                keyname = tuple(ia.keys())[0]
                if '_state' in ia[keyname] and ia[keyname]['_state']['bus_idx'] == idx:
                    if 'interface_association' not in self.output_line['device_descriptor']['configuration_descriptor']:
                        self.output_line['device_descriptor']['configuration_descriptor']['interface_association'] = {}
                    self.output_line['device_descriptor']['configuration_descriptor']['interface_association'].update(ia)
                    del self.output_line['device_descriptor']['configuration_descriptor']['interface_association'][keyname]['_state']
            
            # add interface_descriptor key if it doesn't exist and there are entries for this bus
            for iface_attrs in self.interface_descriptor_list:
                keyname = tuple(iface_attrs.keys())[0]
                if '_state' in iface_attrs[keyname] and iface_attrs[keyname]['_state']['bus_idx'] == idx:
                    if 'interface_descriptors' not in self.output_line['device_descriptor']['configuration_descriptor']:
                        self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptors'] = []

            # find max index for this bus idx, then iterate over that range
            i_desc_iters = -1
            for iface_attrs in self.interface_descriptor_list:
                keyname = tuple(iface_attrs.keys())[0]
                if '_state' in iface_attrs[keyname] and iface_attrs[keyname]['_state']['bus_idx'] == idx:
                    i_desc_iters = iface_attrs[keyname]['_state']['interface_descriptor_idx']

            # create the interface descriptor object
            if i_desc_iters > -1:
                for iface_idx in range(i_desc_iters + 1):
                    i_desc_obj = {}
                    for iface_attrs in self.interface_descriptor_list:
                        keyname = tuple(iface_attrs.keys())[0]
                        if '_state' in iface_attrs[keyname] and iface_attrs[keyname]['_state']['bus_idx'] == idx and iface_attrs[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            del iface_attrs[keyname]['_state']
                            i_desc_obj.update(iface_attrs)

                    # add other nodes to the object (cdc_header, endpoint descriptors, etc.)
                    for ch in self.cdc_header_list:
                        keyname = tuple(ch.keys())[0]
                        if '_state' in ch[keyname] and ch[keyname]['_state']['bus_idx'] == idx and ch[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            if 'cdc_header' not in i_desc_obj:
                                i_desc_obj['cdc_header'] = {}
                            i_desc_obj['cdc_header'].update(ch)
                            del i_desc_obj['cdc_header'][keyname]['_state']

                    for ccm in self.cdc_call_management_list:
                        keyname = tuple(ccm.keys())[0]
                        if '_state' in ccm[keyname] and ccm[keyname]['_state']['bus_idx'] == idx and ccm[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            if 'cdc_call_management' not in i_desc_obj:
                                i_desc_obj['cdc_call_management'] = {}
                            i_desc_obj['cdc_call_management'].update(ccm)
                            del i_desc_obj['cdc_call_management'][keyname]['_state']

                    for ca in self.cdc_acm_list:
                        keyname = tuple(ca.keys())[0]
                        if '_state' in ca[keyname] and ca[keyname]['_state']['bus_idx'] == idx and ca[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            if 'cdc_acm' not in i_desc_obj:
                                i_desc_obj['cdc_acm'] = {}
                            i_desc_obj['cdc_acm'].update(ca)
                            del i_desc_obj['cdc_acm'][keyname]['_state']

                    for cu in self.cdc_union_list:
                        keyname = tuple(cu.keys())[0]
                        if '_state' in cu[keyname] and cu[keyname]['_state']['bus_idx'] == idx and cu[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            if 'cdc_union' not in i_desc_obj:
                                i_desc_obj['cdc_union'] = {}
                            i_desc_obj['cdc_union'].update(cu)
                            del i_desc_obj['cdc_union'][keyname]['_state']

                    for hd in self.hid_device_descriptor_list:
                        keyname = tuple(hd.keys())[0]
                        if '_state' in hd[keyname] and hd[keyname]['_state']['bus_idx'] == idx and hd[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            if 'hid_device_descriptor' not in i_desc_obj:
                                i_desc_obj['hid_device_descriptor'] = {}
                            i_desc_obj['hid_device_descriptor'].update(hd)
                            del i_desc_obj['hid_device_descriptor'][keyname]['_state']

                        for rd in self.report_descriptors_list:
                            keyname = tuple(rd.keys())[0]
                            if '_state' in rd[keyname] and rd[keyname]['_state']['bus_idx'] == idx and rd[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                                if 'report_descriptors' not in i_desc_obj['hid_device_descriptor']:
                                    i_desc_obj['hid_device_descriptor']['report_descriptors'] = {}
                                i_desc_obj['hid_device_descriptor']['report_descriptors'].update(rd)
                                del i_desc_obj['hid_device_descriptor']['report_descriptors'][keyname]['_state']

                    # add endpoint_descriptor key if it doesn't exist and there are entries for this interface_descriptor
                    for endpoint_attrs in self.endpoint_descriptor_list:
                        keyname = tuple(endpoint_attrs.keys())[0]
                        if '_state' in endpoint_attrs[keyname] and endpoint_attrs[keyname]['_state']['bus_idx'] == idx and endpoint_attrs[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            if 'endpoint_descriptors' not in i_desc_obj:
                                i_desc_obj['endpoint_descriptors'] = []

                    # find max index for this endpoint_descriptor idx, then iterate over that range
                    e_desc_iters = -1
                    for endpoint_attrs in self.endpoint_descriptor_list:
                        keyname = tuple(endpoint_attrs.keys())[0]
                        if '_state' in endpoint_attrs[keyname] and endpoint_attrs[keyname]['_state']['bus_idx'] == idx and endpoint_attrs[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                            e_desc_iters = endpoint_attrs[keyname]['_state']['endpoint_descriptor_idx']

                    # create the endpoint descriptor object
                    if e_desc_iters > -1:
                        for endpoint_idx in range(e_desc_iters + 1):
                            e_desc_obj = {}
                            for endpoint_attrs in self.endpoint_descriptor_list:
                                keyname = tuple(endpoint_attrs.keys())[0]
                                if '_state' in endpoint_attrs[keyname] and endpoint_attrs[keyname]['_state']['bus_idx'] == idx and endpoint_attrs[keyname]['_state']['interface_descriptor_idx'] == iface_idx and endpoint_attrs[keyname]['_state']['endpoint_descriptor_idx'] == endpoint_idx:
                                    del endpoint_attrs[keyname]['_state']
                                    e_desc_obj.update(endpoint_attrs)
                            
                            i_desc_obj['endpoint_descriptors'].append(e_desc_obj)
                    
                    # add the object to the list of interface descriptors
                    self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptors'].append(i_desc_obj)
            
            # ['hub_descriptor'] = {}
            # ['hub_descriptor']['hub_port_status'] = {}
            # ['device_status'] = {}
            
            for hd in self.hub_descriptor_list:
                keyname = tuple(hd.keys())[0]
                if '_state' in hd[keyname] and hd[keyname]['_state']['bus_idx'] == idx:
                    if 'hub_descriptor' not in self.output_line:
                        self.output_line['hub_descriptor'] = {}
                    self.output_line['hub_descriptor'].update(hd)
                    del self.output_line['hub_descriptor'][keyname]['_state']


                    


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
# {s.section=}
# {s.bus_list=}
# {s.device_descriptor_list=}
# {s.configuration_descriptor_list=}
# {s.interface_association_list=}
# {s.interface_descriptor_list=}
# {s.cdc_header_list=}
# {s.cdc_call_management_list=}
# {s.cdc_acm_list=}
# {s.cdc_union_list=}
# {s.endpoint_descriptor_list=}
# {s.hid_device_descriptor_list=}
# {s.report_descriptors_list=}
# {s.hub_descriptor_list=}
# {s.hub_port_status_list=}
# {s.device_status_list=}
# ''')

    # populate the schema
    s._populate_schema()

    # output the raw object
    if s.output_line:
        s.raw_output.append(s.output_line)

    return s.raw_output if raw else _process(s.raw_output)
