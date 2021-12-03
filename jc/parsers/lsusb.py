"""jc - JSON CLI output utility `lsusb` command output parser

Supports the `-v` option or no options.

Usage (cli):

    $ lsusb -v | jc --lsusb

    or

    $ jc lsusb -v

Usage (module):

    import jc.parsers.lsusb
    result = jc.parsers.lsusb.parse(lsusb_command_output)

Schema:

    Note: <item> object keynames are assigned directly from the lsusb output.
          If there are duplicate <item> names in a section, only the last one is converted.

    [
      {
        "bus":                                string,
        "device":                             string,
        "id":                                 string,
        "description":                        string,
        "device_descriptor": {
          "<item>": {
            "value":                          string,
            "description":                    string,
            "attributes": [
                                              string
            ]
          },
          "configuration_descriptor": {
            "<item>": {
              "value":                        string,
              "description":                  string,
              "attributes": [
                                              string
              ]
            },
            "interface_association": {
              "<item>": {
                "value":                      string,
                "description":                string,
                "attributes": [
                                              string
                ]
              }
            },
            "interface_descriptors": [
              {
                "<item>": {
                  "value":                    string,
                  "description":              string,
                  "attributes": [
                                              string
                  ]
                },
                "cdc_header": {
                  "<item>": {
                    "value":                  string,
                    "description":            string,
                    "attributes": [
                                              string
                    ]
                  }
                },
                "cdc_call_management": {
                  "<item>": {
                    "value":                  string,
                    "description":            string,
                    "attributes": [
                                              string
                    ]
                  }
                },
                "cdc_acm": {
                  "<item>": {
                    "value":                  string,
                    "description":            string,
                    "attributes": [
                                              string
                    ]
                  }
                },
                "cdc_union": {
                  "<item>": {
                    "value":                  string,
                    "description":            string,
                    "attributes": [
                                              string
                    ]
                  }
                },
                "endpoint_descriptors": [
                  {
                    "<item>": {
                      "value":                string,
                      "description":          string,
                      "attributes": [
                                              string
                      ]
                    }
                  }
                ]
              }
            ]
          }
        },
        "hub_descriptor": {
          "<item>": {
            "value":                          string,
            "description":                    string,
            "attributes": [
                                              string,
            ]
          },
          "hub_port_status": {
            "<item>": {
              "value":                        string,
              "attributes": [
                                              string
              ]
            }
          }
        },
        "device_status": {
          "value":                            string,
          "description":                      string
        }
      }
    ]

Examples:

    $ lsusb -v | jc --lsusb -p
    [
      {
        "bus": "002",
        "device": "001",
        "id": "1d6b:0001",
        "description": "Linux Foundation 1.1 root hub",
        "device_descriptor": {
          "bLength": {
            "value": "18"
          },
          "bDescriptorType": {
            "value": "1"
          },
          "bcdUSB": {
            "value": "1.10"
          },
          ...
          "bNumConfigurations": {
            "value": "1"
          },
          "configuration_descriptor": {
            "bLength": {
              "value": "9"
            },
            ...
            "iConfiguration": {
              "value": "0"
            },
            "bmAttributes": {
              "value": "0xe0",
              "attributes": [
                "Self Powered",
                "Remote Wakeup"
              ]
            },
            "MaxPower": {
              "description": "0mA"
            },
            "interface_descriptors": [
              {
                "bLength": {
                  "value": "9"
                },
                ...
                "bInterfaceProtocol": {
                  "value": "0",
                  "description": "Full speed (or root) hub"
                },
                "iInterface": {
                  "value": "0"
                },
                "endpoint_descriptors": [
                  {
                    "bLength": {
                      "value": "7"
                    },
                    ...
                    "bmAttributes": {
                      "value": "3",
                      "attributes": [
                        "Transfer Type  Interrupt",
                        "Synch Type  None",
                        "Usage Type  Data"
                      ]
                    },
                    "wMaxPacketSize": {
                      "value": "0x0002",
                      "description": "1x 2 bytes"
                    },
                    "bInterval": {
                      "value": "255"
                    }
                  }
                ]
              }
            ]
          }
        },
        "hub_descriptor": {
          "bLength": {
            "value": "9"
          },
          ...
          "wHubCharacteristic": {
            "value": "0x000a",
            "attributes": [
              "No power switching (usb 1.0)",
              "Per-port overcurrent protection"
            ]
          },
          ...
          "hub_port_status": {
            "Port 1": {
              "value": "0000.0103",
              "attributes": [
                "power",
                "enable",
                "connect"
              ]
            },
            "Port 2": {
              "value": "0000.0103",
              "attributes": [
                "power",
                "enable",
                "connect"
              ]
            }
          }
        },
        "device_status": {
          "value": "0x0001",
          "description": "Self Powered"
        }
      }
    ]
"""
import jc.utils
from jc.parsers.universal import sparse_table_parse
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`lsusb` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
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
    # no further processing
    return proc_data


class _NestedDict(dict):
    # for ease of creating/updating nested dictionary structures
    # https://stackoverflow.com/questions/5369723/multi-level-defaultdict-with-variable-depth
    # https://ohuiginn.net/mt/2010/07/nested_dictionaries_in_python.html
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return self.setdefault(key, _NestedDict())


class _LsUsb():
    def __init__(self):
        self.raw_output = []
        self.output_line = _NestedDict()

        self.section = ''
        self.old_section = ''
        self.bus_idx = -1
        self.interface_descriptor_idx = -1
        self.endpoint_descriptor_idx = -1
        self.last_item = ''
        self.last_indent = 0
        self.attribute_value = False

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
            break
        return indent

    def _add_attributes(self, line):
        indent = self._count_indent(line)

        # determine whether this is a top-level value item or lower-level attribute
        if indent > self.last_indent and self.old_section == self.section:
            self.attribute_value = True
        elif indent == self.last_indent and self.attribute_value and self.old_section == self.section:
            self.attribute_value = True
        else:
            self.attribute_value = False

        # section_header is formatted with the correct spacing to be used with
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
                    'attribute_value': self.attribute_value,
                    'last_item': self.last_item,
                    'bus_idx': self.bus_idx,
                    'interface_descriptor_idx': self.interface_descriptor_idx,
                    'endpoint_descriptor_idx': self.endpoint_descriptor_idx
                }
            }
        }

        if line_obj[temp_obj['key']]['value'] is None:
            del line_obj[temp_obj['key']]['value']

        if line_obj[temp_obj['key']]['description'] is None:
            del line_obj[temp_obj['key']]['description']

        self.old_section = self.section
        self.last_indent = indent

        if not self.attribute_value:
            self.last_item = temp_obj['key']

        return line_obj

    def _add_hub_port_status_attributes(self, line):
        # Port 1: 0000.0103 power enable connect
        first_split = line.split(': ', maxsplit=1)
        port_field = first_split[0].strip()
        second_split = first_split[1].split(maxsplit=1)
        port_val = second_split[0]
        attributes = second_split[1].split()

        return {
            port_field: {
                'value': port_val,
                'attributes': attributes,
                '_state': {
                    'bus_idx': self.bus_idx
                }
            }
        }

    def _add_device_status_attributes(self, line):
        return {
            'description': line.strip(),
            '_state': {
                'bus_idx': self.bus_idx
            }
        }

    def _set_sections(self, line):
        # ignore blank lines
        if not line:
            self.section = ''
            self.attribute_value = False
            return True

        # bus information is on the same line so need to extract data immediately and set indexes
        if line.startswith('Bus '):
            self.section = 'bus'
            self.bus_idx += 1
            self.interface_descriptor_idx = -1
            self.endpoint_descriptor_idx = -1
            self.attribute_value = False
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

        # This section is a list, so need to update indexes
        if line.startswith('    Interface Descriptor:'):
            self.section = 'interface_descriptor'
            self.interface_descriptor_idx += 1
            self.endpoint_descriptor_idx = -1
            self.attribute_value = False
            return True

        # This section is a list, so need to update the index
        if line.startswith('      Endpoint Descriptor:'):
            self.section = 'endpoint_descriptor'
            self.endpoint_descriptor_idx += 1
            self.attribute_value = False
            return True

        # some device status information is displayed on the initial line so need to extract immediately
        if line.startswith('Device Status:'):
            self.section = 'device_status'
            self.attribute_value = False
            line_split = line.strip().split(':', maxsplit=1)
            self.device_status_list.append(
                {
                    'value': line_split[1].strip(),
                    '_state': {
                        'bus_idx': self.bus_idx
                    }
                }
            )
            return True

        # set the rest of the sections
        string_section_map = {
            'Device Descriptor:': 'device_descriptor',
            '  Configuration Descriptor:': 'configuration_descriptor',
            '    Interface Association:': 'interface_association',
            '      CDC Header:': 'cdc_header',
            '      CDC Call Management:': 'cdc_call_management',
            '      CDC ACM:': 'cdc_acm',
            '      CDC Union:': 'cdc_union',
            '        HID Device Descriptor:': 'hid_device_descriptor',
            '         Report Descriptors:': 'report_descriptors',
            'Hub Descriptor:': 'hub_descriptor',
            ' Hub Port Status:': 'hub_port_status'
        }

        for sec_string, section_val in string_section_map.items():
            if line.startswith(sec_string):
                self.section = section_val
                self.attribute_value = False
                return True

        return False

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
            'hub_descriptor': self.hub_descriptor_list
        }

        for sec in section_list_map:
            if line.startswith(' ') and self.section == sec:
                section_list_map[self.section].append(self._add_attributes(line))
                return True

        # special handling of these sections
        if line.startswith(' ') and self.section == 'hub_port_status':
            self.hub_port_status_list.append(self._add_hub_port_status_attributes(line))
            return True

        if line.startswith(' ') and self.section == 'device_status':
            self.device_status_list.append(self._add_device_status_attributes(line))
            return True

        return False

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
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'] = []
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'][0] = {}
        ['hub_descriptor'] = {}
        ['hub_descriptor']['hub_port_status'] = {}
        ['device_status'] = {}
        """
        for idx, item in enumerate(self.bus_list):
            if self.output_line:
                self.raw_output.append(self.output_line)

            self.output_line = _NestedDict()

            del item['_state']
            self.output_line.update(item)

            for dd in self.device_descriptor_list:
                keyname = tuple(dd.keys())[0]
                if '_state' in dd[keyname] and dd[keyname]['_state']['bus_idx'] == idx:

                    # is this a top level value or an attribute?
                    if dd[keyname]['_state']['attribute_value']:
                        last_item = dd[keyname]['_state']['last_item']
                        if 'attributes' not in self.output_line['device_descriptor'][last_item]:
                            self.output_line['device_descriptor'][last_item]['attributes'] = []

                        this_attribute = f'{keyname} {dd[keyname].get("value", "")} {dd[keyname].get("description", "")}'.strip()
                        self.output_line['device_descriptor'][last_item]['attributes'].append(this_attribute)
                        continue

                    self.output_line['device_descriptor'].update(dd)
                    del self.output_line['device_descriptor'][keyname]['_state']

            for cd in self.configuration_descriptor_list:
                keyname = tuple(cd.keys())[0]
                if '_state' in cd[keyname] and cd[keyname]['_state']['bus_idx'] == idx:

                    # is this a top level value or an attribute?
                    if cd[keyname]['_state']['attribute_value']:
                        last_item = cd[keyname]['_state']['last_item']
                        if 'attributes' not in self.output_line['device_descriptor']['configuration_descriptor'][last_item]:
                            self.output_line['device_descriptor']['configuration_descriptor'][last_item]['attributes'] = []

                        this_attribute = f'{keyname} {cd[keyname].get("value", "")} {cd[keyname].get("description", "")}'.strip()
                        self.output_line['device_descriptor']['configuration_descriptor'][last_item]['attributes'].append(this_attribute)
                        continue

                    self.output_line['device_descriptor']['configuration_descriptor'].update(cd)
                    del self.output_line['device_descriptor']['configuration_descriptor'][keyname]['_state']

            for ia in self.interface_association_list:
                keyname = tuple(ia.keys())[0]
                if '_state' in ia[keyname] and ia[keyname]['_state']['bus_idx'] == idx:

                    # is this a top level value or an attribute?
                    if ia[keyname]['_state']['attribute_value']:
                        last_item = ia[keyname]['_state']['last_item']
                        if 'attributes' not in self.output_line['device_descriptor']['configuration_descriptor']['interface_association'][last_item]:
                            self.output_line['device_descriptor']['configuration_descriptor']['interface_association'][last_item]['attributes'] = []

                        this_attribute = f'{keyname} {ia[keyname].get("value", "")} {ia[keyname].get("description", "")}'.strip()
                        self.output_line['device_descriptor']['configuration_descriptor']['interface_association'][last_item]['attributes'].append(this_attribute)
                        continue

                    self.output_line['device_descriptor']['configuration_descriptor']['interface_association'].update(ia)
                    del self.output_line['device_descriptor']['configuration_descriptor']['interface_association'][keyname]['_state']

            # add interface_descriptor key if it doesn't exist and there are entries for this bus
            for iface_attrs in self.interface_descriptor_list:
                keyname = tuple(iface_attrs.keys())[0]
                if '_state' in iface_attrs[keyname] and iface_attrs[keyname]['_state']['bus_idx'] == idx:
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
                    i_desc_obj = _NestedDict()
                    for iface_attrs in self.interface_descriptor_list:
                        keyname = tuple(iface_attrs.keys())[0]
                        if '_state' in iface_attrs[keyname] and iface_attrs[keyname]['_state']['bus_idx'] == idx and iface_attrs[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                            # is this a top level value or an attribute?
                            if iface_attrs[keyname]['_state']['attribute_value']:
                                last_item = iface_attrs[keyname]['_state']['last_item']
                                if 'attributes' not in i_desc_obj[last_item]:
                                    i_desc_obj[last_item]['attributes'] = []

                                this_attribute = f'{keyname} {iface_attrs[keyname].get("value", "")} {iface_attrs[keyname].get("description", "")}'.strip()
                                i_desc_obj[last_item]['attributes'].append(this_attribute)
                                continue

                            del iface_attrs[keyname]['_state']
                            i_desc_obj.update(iface_attrs)

                    # add other nodes to the object (cdc_header, endpoint descriptors, etc.)
                    for ch in self.cdc_header_list:
                        keyname = tuple(ch.keys())[0]
                        if '_state' in ch[keyname] and ch[keyname]['_state']['bus_idx'] == idx and ch[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                            # is this a top level value or an attribute?
                            if ch[keyname]['_state']['attribute_value']:
                                last_item = ch[keyname]['_state']['last_item']
                                if 'attributes' not in i_desc_obj['cdc_header'][last_item]:
                                    i_desc_obj['cdc_header'][last_item]['attributes'] = []

                                this_attribute = f'{keyname} {ch[keyname].get("value", "")} {ch[keyname].get("description", "")}'.strip()
                                i_desc_obj['cdc_header'][last_item]['attributes'].append(this_attribute)
                                continue

                            i_desc_obj['cdc_header'].update(ch)
                            del i_desc_obj['cdc_header'][keyname]['_state']

                    for ccm in self.cdc_call_management_list:
                        keyname = tuple(ccm.keys())[0]
                        if '_state' in ccm[keyname] and ccm[keyname]['_state']['bus_idx'] == idx and ccm[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                            # is this a top level value or an attribute?
                            if ccm[keyname]['_state']['attribute_value']:
                                last_item = ccm[keyname]['_state']['last_item']
                                if 'attributes' not in i_desc_obj['cdc_call_management'][last_item]:
                                    i_desc_obj['cdc_call_management'][last_item]['attributes'] = []

                                this_attribute = f'{keyname} {ccm[keyname].get("value", "")} {ccm[keyname].get("description", "")}'.strip()
                                i_desc_obj['cdc_call_management'][last_item]['attributes'].append(this_attribute)
                                continue

                            i_desc_obj['cdc_call_management'].update(ccm)
                            del i_desc_obj['cdc_call_management'][keyname]['_state']

                    for ca in self.cdc_acm_list:
                        keyname = tuple(ca.keys())[0]
                        if '_state' in ca[keyname] and ca[keyname]['_state']['bus_idx'] == idx and ca[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                            # is this a top level value or an attribute?
                            if ca[keyname]['_state']['attribute_value']:
                                last_item = ca[keyname]['_state']['last_item']
                                if 'attributes' not in i_desc_obj['cdc_acm'][last_item]:
                                    i_desc_obj['cdc_acm'][last_item]['attributes'] = []

                                this_attribute = f'{keyname} {ca[keyname].get("value", "")} {ca[keyname].get("description", "")}'.strip()
                                i_desc_obj['cdc_acm'][last_item]['attributes'].append(this_attribute)
                                continue

                            i_desc_obj['cdc_acm'].update(ca)
                            del i_desc_obj['cdc_acm'][keyname]['_state']

                    for cu in self.cdc_union_list:
                        keyname = tuple(cu.keys())[0]
                        if '_state' in cu[keyname] and cu[keyname]['_state']['bus_idx'] == idx and cu[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                            # is this a top level value or an attribute?
                            if cu[keyname]['_state']['attribute_value']:
                                last_item = cu[keyname]['_state']['last_item']
                                if 'attributes' not in i_desc_obj['cdc_union'][last_item]:
                                    i_desc_obj['cdc_union'][last_item]['attributes'] = []

                                this_attribute = f'{keyname} {cu[keyname].get("value", "")} {cu[keyname].get("description", "")}'.strip()
                                i_desc_obj['cdc_union'][last_item]['attributes'].append(this_attribute)
                                continue

                            i_desc_obj['cdc_union'].update(cu)
                            del i_desc_obj['cdc_union'][keyname]['_state']

                    for hidd in self.hid_device_descriptor_list:
                        keyname = tuple(hidd.keys())[0]
                        if '_state' in hidd[keyname] and hidd[keyname]['_state']['bus_idx'] == idx and hidd[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                            # is this a top level value or an attribute?
                            if hidd[keyname]['_state']['attribute_value']:
                                last_item = hidd[keyname]['_state']['last_item']
                                if 'attributes' not in i_desc_obj['hid_device_descriptor'][last_item]:
                                    i_desc_obj['hid_device_descriptor'][last_item]['attributes'] = []

                                this_attribute = f'{keyname} {hidd[keyname].get("value", "")} {hidd[keyname].get("description", "")}'.strip()
                                i_desc_obj['hid_device_descriptor'][last_item]['attributes'].append(this_attribute)
                                continue

                            i_desc_obj['hid_device_descriptor'].update(hidd)
                            del i_desc_obj['hid_device_descriptor'][keyname]['_state']

                        # Not Implemented: Report Descriptors (need more samples)
                        # for rd in self.report_descriptors_list:
                        #     keyname = tuple(rd.keys())[0]
                        #     if '_state' in rd[keyname] and rd[keyname]['_state']['bus_idx'] == idx and rd[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                        #         i_desc_obj['hid_device_descriptor']['report_descriptors'].update(rd)
                        #         del i_desc_obj['hid_device_descriptor']['report_descriptors'][keyname]['_state']

                    # add endpoint_descriptor key if it doesn't exist and there are entries for this interface_descriptor
                    for endpoint_attrs in self.endpoint_descriptor_list:
                        keyname = tuple(endpoint_attrs.keys())[0]
                        if '_state' in endpoint_attrs[keyname] and endpoint_attrs[keyname]['_state']['bus_idx'] == idx and endpoint_attrs[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
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

                                    # is this a top level value or an attribute?
                                    if endpoint_attrs[keyname]['_state']['attribute_value']:
                                        last_item = endpoint_attrs[keyname]['_state']['last_item']
                                        if 'attributes' not in e_desc_obj[last_item]:
                                            e_desc_obj[last_item]['attributes'] = []

                                        this_attribute = f'{keyname} {endpoint_attrs[keyname].get("value", "")} {endpoint_attrs[keyname].get("description", "")}'.strip()
                                        e_desc_obj[last_item]['attributes'].append(this_attribute)
                                        continue

                                    e_desc_obj.update(endpoint_attrs)
                                    del endpoint_attrs[keyname]['_state']

                            i_desc_obj['endpoint_descriptors'].append(e_desc_obj)

                    # add the object to the list of interface descriptors
                    self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptors'].append(i_desc_obj)

            for hd in self.hub_descriptor_list:
                keyname = tuple(hd.keys())[0]
                if '_state' in hd[keyname] and hd[keyname]['_state']['bus_idx'] == idx:

                    # is this a top level value or an attribute?
                    if hd[keyname]['_state']['attribute_value']:
                        last_item = hd[keyname]['_state']['last_item']
                        if 'attributes' not in self.output_line['hub_descriptor'][last_item]:
                            self.output_line['hub_descriptor'][last_item]['attributes'] = []

                        this_attribute = f'{keyname} {hd[keyname].get("value", "")} {hd[keyname].get("description", "")}'.strip()
                        self.output_line['hub_descriptor'][last_item]['attributes'].append(this_attribute)
                        continue

                    self.output_line['hub_descriptor'].update(hd)
                    del self.output_line['hub_descriptor'][keyname]['_state']

            for hps in self.hub_port_status_list:
                keyname = tuple(hps.keys())[0]
                if '_state' in hps[keyname] and hps[keyname]['_state']['bus_idx'] == idx:
                    self.output_line['hub_descriptor']['hub_port_status'].update(hps)
                    del self.output_line['hub_descriptor']['hub_port_status'][keyname]['_state']

            for ds in self.device_status_list:
                if '_state' in ds and ds['_state']['bus_idx'] == idx:
                    self.output_line['device_status'].update(ds)
                    del self.output_line['device_status']['_state']


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
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    lsusb = _LsUsb()

    if jc.utils.has_data(data):
        for line in data.splitlines():
            # only -v option or no options are supported
            if line.startswith('/'):
                raise ParseError('Only `lsusb` or `lsusb -v` are supported.')

            # sections
            if lsusb._set_sections(line):
                continue

            # create section lists and schema
            if lsusb._populate_lists(line):
                continue

    # populate the schema
    lsusb._populate_schema()

    # add any final output object if it exists and return the raw_output list
    if lsusb.output_line:
        lsusb.raw_output.append(lsusb.output_line)

    return lsusb.raw_output if raw else _process(lsusb.raw_output)
