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


class _LsUsb():
    def __init__(self):
        self.raw_output = []
        self.output_line = {}
        self.section = ''
        self.old_section = ''
        self.section_depth = 0
        self.old_section_depth = 0
        self.device_descriptor_list = []
        self.configuration_descriptor_list = []
        self.interface_association_list = []
        self.interface_descriptor_list = []
        self.cdc_header_list = []
        self.cdc_call_management_list = []
        self.cdc_acm_list = []
        self.cdc_union_list = []
        self.endpoint_descriptor_list = []
        self.hid_device_descriptor_list = []
        self.report_descriptors_list = []
        self.hub_descriptor_list = []
        self.hub_port_status_list = []

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

        line_obj = [section_header, line.strip() + (' ' * 25)]
        line_obj = sparse_table_parse(line_obj)
        # line_obj[0].update({'indent': indent, 'depth': self.section_depth})

        return line_obj[0]

    def _new_section(self, new_section):
        self.old_section = self.section
        self.section = new_section

    def _new_depth(self, new_depth):
        self.old_section_depth = self.section_depth
        self.section_depth = new_depth

    def _populate_schema(self, final=False):
        """
        Append list entries and reset lists on section change
        Depth assignments:
        
        Bus                                 0
          Device Descriptor:                2
           <attrs>                          3
            Configuration Descriptor:       4
             <attrs>                        5
              Interface Association:        6
               <attrs>                      7
              Interface Descriptor:         6
               <attrs>                      7
                CDC Header:                 8
                 <attrs>                    9
                CDC Call Management:        8
                 <attrs>                    9
                CDC ACM:                    8
                 <attrs>                    9
                CDC Union:                  8
                 <attrs>                    9
                  HID Device Descriptor:    10
                   <attrs>                  11
                    Report Descriptors:     12
                     <attrs>                13
                Endpoint Descriptor:        8
                 <attrs>                    9
          Hub Descriptor:                   2
           <attrs>                          3
            Hub Port Status:                4
             <attrs>                        5
          Device Status:                    2
           <attrs>                          3
        """
        if (self.section != self.old_section and self.section_depth < self.old_section_depth) or final:
            # in decending depth order

            if self.report_descriptors_list:
                self.report_descriptors_list.append({'report_descriptor': self.report_descriptors_list})
                self.report_descriptors_list = []
                if not final:
                    return

            if self.hid_device_descriptor_list:
                self.endpoint_descriptor_list.append({'hid_device_descriptor': self.hid_device_descriptor_list})
                self.hid_device_descriptor_list = []
                if not final:
                    return

            if self.cdc_header_list:
                self.interface_descriptor_list.append({'cdc_header': self.cdc_header_list})
                self.cdc_header_list = []

            if self.cdc_call_management_list:
                self.interface_descriptor_list.append({'cdc_call_management': self.cdc_call_management_list})
                self.cdc_call_management_list = []

            if self.cdc_acm_list:
                self.interface_descriptor_list.append({'cdc_acm': self.cdc_acm_list})
                self.cdc_acm_list = []

            if self.cdc_union_list:
                self.interface_descriptor_list.append({'cdc_union': self.cdc_union_list})
                self.cdc_union_list = []

            if self.endpoint_descriptor_list:
                self.interface_descriptor_list.append({'endpoint_descriptor': self.endpoint_descriptor_list})
                self.endpoint_descriptor_list = []
                if not final:
                    return

            if self.interface_association_list:
                self.output_line['device_descriptor']['configuration_descriptor']['interface_association']['attributes'].append(self.interface_association_list)
                self.interface_association_list = []

            if self.interface_descriptor_list:
                if 'interface_descriptor_list' not in self.output_line['device_descriptor']['configuration_descriptor']:
                    self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptor'] = []
                self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptor'].append(self.interface_descriptor_list)
                if not final:
                    return

            if self.configuration_descriptor_list:
                self.output_line['device_descriptor']['configuration_descriptor']['attributes'].append(self.configuration_descriptor_list)
                self.configuration_descriptor_list = []
            
            if self.hub_port_status_list:
                if 'hub_descriptor' not in self.output_line:
                    self.output_line['hub_descriptor'] = {}
                    self.output_line['hub_descriptor']['hub_port_status'] = []
                self.output_line['hub_descriptor']['hub_port_status'].append(self.hub_port_status_list)
                self.hub_port_status_list = []
                if not final:
                    return

            if self.device_descriptor_list:
                self.output_line['device_descriptor']['attributes'].append(self.device_descriptor_list)
                self.device_descriptor_list = []
    
            if self.hub_descriptor_list:
                if 'hub_descriptor' not in self.output_line:
                    self.output_line['hub_descriptor'] = {}
                if 'attributes' not in self.output_line['hub_descriptor']:
                    self.output_line['hub_descriptor']['attributes'] = []
                self.output_line['hub_descriptor']['attributes'].append(self.hub_descriptor_list)
                self.hub_descriptor_list = []
                if not final:
                    return

    def _set_sections(self, line):
        if line.startswith('Bus '):
            self._new_section('bus')
            self._new_depth(0)

            if self.output_line:
                self.raw_output.append(self.output_line)

            self.output_line = {}

            line_split = line.strip().split(maxsplit=6)
            self.output_line.update(
                {
                    'bus': line_split[1],
                    'device': line_split[3][:-1],
                    'id': line_split[5],
                    'description': (line_split[6:7] or [None])[0]     # way to get a list item or None
                }
            )
            return True

        if line.startswith('Device Descriptor:'):
            self._new_section('device_descriptor')
            self._new_depth(2)
            return True

        if line.startswith('  Configuration Descriptor:'):
            self._new_section('configuration_descriptor')
            self._new_depth(4)
            return True

        if line.startswith('    Interface Association:'):
            self._new_section('interface_association')
            self._new_depth(6)
            return True

        if line.startswith('    Interface Descriptor:'):
            self._new_section('interface_descriptor')
            self._new_depth(6)
            return True

        if line.startswith('      CDC Header:'):
            self._new_section('cdc_header')
            self._new_depth(8)
            return True

        if line.startswith('      CDC Call Management:'):
            self._new_section('cdc_call_management')
            self._new_depth(8)
            return True

        if line.startswith('      CDC ACM:'):
            self._new_section('cdc_acm')
            self._new_depth(8)
            return True

        if line.startswith('      CDC Union:'):
            self._new_section('cdc_union')
            self._new_depth(8)
            return True

        if line.startswith('      Endpoint Descriptor:'):
            self._new_section('endpoint_descriptor')
            self._new_depth(8)
            return True

        if line.startswith('        HID Device Descriptor:'):
            self._new_section('hid_device_descriptor')
            self._new_depth(10)
            return True

        if line.startswith('         Report Descriptors:'):
            self._new_section('report_descriptors')
            self._new_depth(12)
            return True

        if line.startswith('Hub Descriptor:'):
            self._new_section('hub_descriptor')
            self._new_depth(2)
            return True

        if line.startswith(' Hub Port Status:'):
            self._new_section('hub_port_status')
            self._new_depth(4)
            return True

        if line.startswith('Device Status:'):
            self._new_section('device_status')
            self._new_depth(2)

            line_split = line.strip().split(':', maxsplit=1)
            self.output_line.update(
                {
                    'device_status':
                        {
                            'value': line_split[1].strip()
                        }
                }
            )
            return True

    def _populate_lists(self, line):
        if self.section == 'device_descriptor' and line.startswith(' '):
            self._new_depth(3)
            self.device_descriptor_list.append(self._add_attributes(line))
            if 'device_descriptor' not in self.output_line:
                self.output_line['device_descriptor'] = {}
                self.output_line['device_descriptor']['attributes'] = []
            return True

        if self.section == 'configuration_descriptor' and line.startswith(' '):
            self._new_depth(5)
            self.configuration_descriptor_list.append(self._add_attributes(line))
            if 'configuration_descriptor' not in self.output_line['device_descriptor']:
                self.output_line['device_descriptor']['configuration_descriptor'] = {}
                self.output_line['device_descriptor']['configuration_descriptor']['attributes'] = []
            return True

        if self.section == 'interface_association' and line.startswith(' '):
            self._new_depth(7)
            self.interface_association_list.append(self._add_attributes(line))
            if 'interface_association' not in self.output_line['device_descriptor']['configuration_descriptor']:
                self.output_line['device_descriptor']['configuration_descriptor']['interface_association'] = {}
                self.output_line['device_descriptor']['configuration_descriptor']['interface_association']['attributes'] = []
            return True

        if self.section == 'interface_descriptor' and line.startswith(' '):
            self._new_depth(7)
            self.interface_descriptor_list.append(self._add_attributes(line))
            return True

        if self.section == 'cdc_header' and line.startswith(' '):
            self._new_depth(9)
            self.cdc_header_list.append(self._add_attributes(line))
            return True

        if self.section == 'cdc_call_management' and line.startswith(' '):
            self._new_depth(9)
            self.cdc_call_management_list.append(self._add_attributes(line))
            return True

        if self.section == 'cdc_acm' and line.startswith(' '):
            self._new_depth(9)
            self.cdc_acm_list.append(self._add_attributes(line))
            return True

        if self.section == 'cdc_union' and line.startswith(' '):
            self._new_depth(9)
            self.cdc_union_list.append(self._add_attributes(line))
            return True

        if self.section == 'hid_device_descriptor' and line.startswith(' '):
            self._new_depth(11)            
            self.report_descriptors_list.append(self._add_attributes(line))
            return True

        if self.section == 'report_descriptors' and line.startswith(' '):
            self._new_depth(13)
            self.report_descriptors_list.append(self._add_attributes(line))
            return True

        if self.section == 'endpoint_descriptor' and line.startswith(' '):
            self._new_depth(9)
            self.endpoint_descriptor_list.append(self._add_attributes(line))
            return True

        if self.section == 'hub_descriptor' and line.startswith(' '):
            self._new_depth(3)
            self.hub_descriptor_list.append(self._add_attributes(line))
            return True

        if self.section == 'hub_port_status' and line.startswith(' '):
            self._new_depth(5)
            self.hub_port_status_list.append(self._add_attributes(line))
            return True


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
            print(f'section: {s.section}, depth: {s.section_depth}')
            # populate schema when backing out of nodes
            s._populate_schema()
            
            # ignore blank lines
            if not line:
                s._new_section('')
                s._new_depth(0)
                continue

            # sections
            if s._set_sections(line):
                continue
            
            # create section lists and schema
            if s._populate_lists(line):
                continue
            
    # get final list entries
    s._new_depth(-1)
    s._populate_schema(final=True)

    # output the raw object
    if s.output_line:
        s.raw_output.append(s.output_line)

    return s.raw_output if raw else _process(s.raw_output)
