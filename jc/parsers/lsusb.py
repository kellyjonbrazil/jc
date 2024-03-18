r"""jc - JSON Convert `lsusb` command output parser

Supports the `-v` option or no options.

Usage (cli):

    $ lsusb -v | jc --lsusb

or

    $ jc lsusb -v

Usage (module):

    import jc
    result = jc.parse('lsusb', lsusb_command_output)

Schema:

> Note: <item> object keynames are assigned directly from the lsusb
> output. If there are duplicate <item> names in a section, only the
> last one is converted.

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
                "cdc_mbim": {
                  "<item>": {
                    "value":                  string,
                    "description":            string,
                    "attributes": [
                                              string
                    ]
                  }
                },
                "cdc_mbim_extended": {
                  "<item>": {
                    "value":                  string,
                    "description":            string,
                    "attributes": [
                                              string
                    ]
                  }
                },
                "videocontrol_descriptors": [
                  {
                    "<item>": {
                      "value":                string,
                      "description":          string,
                      "attributes": [
                                              string
                      ]
                    }
                  }
                ],
                "videostreaming_descriptors": [
                  {
                    "<item>": {
                      "value":                string,
                      "description":          string,
                      "attributes": [
                                              string
                      ]
                    }
                  }
                ],
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
        "device_qualifier": {
          "<item>": {
            "value":                          string,
            "description":                    string
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
    version = '1.4'
    description = '`lsusb` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['lsusb']
    tags = ['command']


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


class _root_obj:
    def __init__(self, name):
        self.name = name
        self.list = []

    def _entries_for_this_bus_exist(self, bus_idx):
        """Returns true if there are object entries for the corresponding bus index"""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                return True

        return False

    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']


class _descriptor_obj:
    def __init__(self, name):
        self.name = name
        self.list = []

    def _entries_for_this_bus_and_interface_idx_exist(self, bus_idx, iface_idx):
        """Returns true if there are object entries for the corresponding bus index
        and interface index"""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx \
                and item[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                return True

        return False

    def _update_output(self, bus_idx, iface_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index and
        interface index. output_line is the i_desc_obj object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx \
                and item[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']


class _descriptor_list:
    def __init__(self, name):
        self.name = name
        self.list = []

    def _entries_for_this_bus_and_interface_idx_exist(self, bus_idx, iface_idx):
        """Returns true if there are object entries for the corresponding bus index
        and interface index"""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx \
                and item[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                return True

        return False

    def _get_objects_list(self, bus_idx, iface_idx):
        """Returns a list of descriptor object dictionaries for the corresponding
        bus index and interface index"""
        object_collection = []

        # find max number of items in this object that match the bus_idx and iface_idx
        num_of_items = -1
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx \
                and item[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                num_of_items = item[keyname]['_state'][f'{self.name}_idx']

        # create and return the collection of objects that match the bus_idx and iface_idx
        if num_of_items > -1:
            for obj_idx in range(num_of_items + 1):
                this_object = {}
                for item in self.list:
                    keyname = tuple(item.keys())[0]

                    if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx \
                        and item[keyname]['_state']['interface_descriptor_idx'] == iface_idx \
                        and item[keyname]['_state'][f'{self.name}_idx'] == obj_idx:

                        # is this a top level value or an attribute?
                        if item[keyname]['_state']['attribute_value']:
                            last_item = item[keyname]['_state']['last_item']
                            if 'attributes' not in this_object[last_item]:
                                this_object[last_item]['attributes'] = []

                            this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                            this_object[last_item]['attributes'].append(this_attribute)
                            continue

                        this_object.update(item)
                        del item[keyname]['_state']

                object_collection.append(this_object)

        return object_collection


class _LsUsb():
    def __init__(self):
        self.raw_output = []
        self.output_line = _NestedDict()

        self.section = ''
        self.old_section = ''

        # section_header is formatted with the correct spacing to be used with
        # jc.parsers.universal.sparse_table_parse(). Pad end of string to be at least len of 25
        # this value changes for different sections (e.g. videocontrol & videostreaming)
        self.normal_section_header = 'key                   val description'
        self.larger_section_header = 'key                               val description'

        self.bus_idx = -1
        self.interface_descriptor_idx = -1
        self.endpoint_descriptor_idx = -1
        self.videocontrol_interface_descriptor_idx = -1
        self.videostreaming_interface_descriptor_idx = -1
        self.last_item = ''
        self.last_indent = 0
        self.attribute_value = False

        self.bus_list = []
        self.device_descriptor = _root_obj('device_descriptor')
        self.configuration_descriptor = _root_obj('configuration_descriptor')
        self.interface_association = _root_obj('interface_association')
        self.interface_descriptor_list = []
        self.cdc_header = _descriptor_obj('cdc_header')
        self.cdc_call_management = _descriptor_obj('cdc_call_management')
        self.cdc_acm = _descriptor_obj('cdc_acm')
        self.cdc_union = _descriptor_obj('cdc_union')
        self.cdc_mbim = _descriptor_obj('cdc_mbim')
        self.cdc_mbim_extended = _descriptor_obj('cdc_mbim_extended')
        self.endpoint_descriptors = _descriptor_list('endpoint_descriptor')
        self.videocontrol_interface_descriptors = _descriptor_list('videocontrol_interface_descriptor')
        self.videostreaming_interface_descriptors = _descriptor_list('videostreaming_interface_descriptor')
        self.hid_device_descriptor = _descriptor_obj('hid_device_descriptor')
        # self.report_descriptors_list = []          # not implemented
        self.hub_descriptor = _root_obj('hub_descriptor')
        self.hub_port_status_list = []
        self.device_qualifier_list = []
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

        elif indent == self.last_indent and self.attribute_value \
            and self.old_section == self.section:

            self.attribute_value = True

        else:
            self.attribute_value = False

        section_header = self.normal_section_header

        if self.section == 'videocontrol_interface_descriptor' \
            or self.section == 'videostreaming_interface_descriptor' \
            or self.section == 'cdc_mbim_extended':

            section_header = self.larger_section_header

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
                    'endpoint_descriptor_idx': self.endpoint_descriptor_idx,
                    'videocontrol_interface_descriptor_idx': self.videocontrol_interface_descriptor_idx,
                    'videostreaming_interface_descriptor_idx': self.videostreaming_interface_descriptor_idx
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

        # bus information is on the same line so need to extract data
        # immediately and set indexes
        if line.startswith('Bus '):
            self.section = 'bus'
            self.bus_idx += 1
            self.interface_descriptor_idx = -1
            self.endpoint_descriptor_idx = -1
            self.videocontrol_interface_descriptor_idx = -1
            self.videostreaming_interface_descriptor_idx = -1
            self.attribute_value = False
            line_split = line.strip().split(maxsplit=6)
            self.bus_list.append(
                {
                    'bus': line_split[1],
                    'device': line_split[3][:-1],
                    'id': line_split[5],
                    # way to get a list item or None
                    'description': (line_split[6:7] or [None])[0],
                    '_state': {
                        'bus_idx': self.bus_idx
                    }
                }
            )
            return True

        # These sections are lists, so need to update indexes
        if line.startswith('    Interface Descriptor:'):
            self.section = 'interface_descriptor'
            self.interface_descriptor_idx += 1
            self.endpoint_descriptor_idx = -1
            self.videocontrol_interface_descriptor_idx = -1
            self.videostreaming_interface_descriptor_idx = -1
            self.attribute_value = False
            return True

        if line.startswith('      Endpoint Descriptor:'):
            self.section = 'endpoint_descriptor'
            self.endpoint_descriptor_idx += 1
            self.attribute_value = False
            return True

        if line.startswith('      VideoControl Interface Descriptor:'):
            self.section = 'videocontrol_interface_descriptor'
            self.videocontrol_interface_descriptor_idx += 1
            self.attribute_value = False
            return True

        if line.startswith('      VideoStreaming Interface Descriptor:'):
            self.section = 'videostreaming_interface_descriptor'
            self.videostreaming_interface_descriptor_idx += 1
            self.attribute_value = False
            return True

        # some device status information is displayed on the initial line so
        # need to extract immediately
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
            '      CDC MBIM:': 'cdc_mbim',
            '      CDC MBIM Extended:': 'cdc_mbim_extended',
            'Hub Descriptor:': 'hub_descriptor',
            ' Hub Port Status:': 'hub_port_status',
            'Device Qualifier (for other device speed):': 'device_qualifier',
            'Binary Object Store Descriptor:': None   # not implemented
        }

        for sec_string, section_val in string_section_map.items():
            if line.startswith(sec_string):
                self.section = section_val
                self.attribute_value = False
                return True

        return False

    def _populate_lists(self, line):
        section_list_map = {
            'device_descriptor': self.device_descriptor.list,
            'configuration_descriptor': self.configuration_descriptor.list,
            'interface_association': self.interface_association.list,
            'interface_descriptor': self.interface_descriptor_list,
            'cdc_header': self.cdc_header.list,
            'cdc_call_management': self.cdc_call_management.list,
            'cdc_acm': self.cdc_acm.list,
            'cdc_union': self.cdc_union.list,
            'cdc_mbim': self.cdc_mbim.list,
            'cdc_mbim_extended': self.cdc_mbim_extended.list,
            'hid_device_descriptor': self.hid_device_descriptor.list,
            # 'report_descriptors': self.report_descriptors_list,         # not implemented
            'videocontrol_interface_descriptor': self.videocontrol_interface_descriptors.list,
            'videostreaming_interface_descriptor': self.videostreaming_interface_descriptors.list,
            'endpoint_descriptor': self.endpoint_descriptors.list,
            'hub_descriptor': self.hub_descriptor.list,
            'device_qualifier': self.device_qualifier_list
        }

        for sec in section_list_map:
            if line.startswith(' ') and self.section == sec:
                section_list_map[self.section].append(self._add_attributes(line))
                return True

        # special handling of these sections
        if line.startswith(' ') and not line.startswith('     ') \
            and self.section == 'hub_port_status':

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
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['videocontrol_interface_descriptors'] = []
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['videocontrol_interface_descriptors'][0] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['videostreaming_interface_descriptors'] = []
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['videostreaming_interface_descriptors'][0] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_header'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_call_management'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_acm'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_union'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_mbim'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['cdc_mbim_extended'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['hid_device_descriptor'] = {}
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'] = []
        ['device_descriptor']['configuration_descriptor']['interface_descriptors'][0]['endpoint_descriptors'][0] = {}
        ['hub_descriptor'] = {}
        ['hub_descriptor']['hub_port_status'] = {}
        ['device_qualifier'] = {}
        ['device_status'] = {}
        """
        for idx, item in enumerate(self.bus_list):
            if self.output_line:
                self.raw_output.append(self.output_line)

            self.output_line = _NestedDict()

            del item['_state']
            self.output_line.update(item)

            # add initial root-level keys
            if self.device_descriptor._entries_for_this_bus_exist(idx):
                self.device_descriptor._update_output(idx, self.output_line)

            if self.configuration_descriptor._entries_for_this_bus_exist(idx):
                self.configuration_descriptor._update_output(
                    idx, self.output_line['device_descriptor']
                )

            if self.interface_association._entries_for_this_bus_exist(idx):
                self.interface_association._update_output(
                    idx, self.output_line['device_descriptor']['configuration_descriptor']
                )

            # add interface_descriptor key if it doesn't exist and there
            # are entries for this bus
            for iface_attrs in self.interface_descriptor_list:
                keyname = tuple(iface_attrs.keys())[0]

                if '_state' in iface_attrs[keyname] \
                    and iface_attrs[keyname]['_state']['bus_idx'] == idx:

                    self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptors'] = []

            # find max index for this bus idx, then iterate over that range
            i_desc_iters = -1
            for iface_attrs in self.interface_descriptor_list:
                keyname = tuple(iface_attrs.keys())[0]

                if '_state' in iface_attrs[keyname] \
                    and iface_attrs[keyname]['_state']['bus_idx'] == idx:

                    i_desc_iters = iface_attrs[keyname]['_state']['interface_descriptor_idx']

            # create the interface descriptor object
            if i_desc_iters > -1:
                for iface_idx in range(i_desc_iters + 1):
                    i_desc_obj = _NestedDict()

                    for iface_attrs in self.interface_descriptor_list:
                        keyname = tuple(iface_attrs.keys())[0]

                        if '_state' in iface_attrs[keyname] \
                            and iface_attrs[keyname]['_state']['bus_idx'] == idx \
                            and iface_attrs[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

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

                    # add the rest of the interface descriptor keys to the object
                    if self.cdc_header._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        self.cdc_header._update_output(idx, iface_idx, i_desc_obj)

                    if self.cdc_call_management._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        self.cdc_call_management._update_output(idx, iface_idx, i_desc_obj)

                    if self.cdc_acm._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        self.cdc_acm._update_output(idx, iface_idx, i_desc_obj)

                    if self.cdc_union._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        self.cdc_union._update_output(idx, iface_idx, i_desc_obj)

                    if self.cdc_mbim._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        self.cdc_mbim._update_output(idx, iface_idx, i_desc_obj)

                    if self.cdc_mbim_extended._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        self.cdc_mbim_extended._update_output(idx, iface_idx, i_desc_obj)

                    if self.hid_device_descriptor._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        self.hid_device_descriptor._update_output(idx, iface_idx, i_desc_obj)

                    # Not Implemented: Report Descriptors (need more samples)
                    # for rd in self.report_descriptors_list:
                    #     keyname = tuple(rd.keys())[0]
                    #     if '_state' in rd[keyname] and rd[keyname]['_state']['bus_idx'] == idx and rd[keyname]['_state']['interface_descriptor_idx'] == iface_idx:
                    #         i_desc_obj['hid_device_descriptor']['report_descriptors'].update(rd)
                    #         del i_desc_obj['hid_device_descriptor']['report_descriptors'][keyname]['_state']

                    if self.videocontrol_interface_descriptors._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        i_desc_obj['videocontrol_interface_descriptors'] = []
                        i_desc_obj['videocontrol_interface_descriptors'].extend(
                            self.videocontrol_interface_descriptors._get_objects_list(idx, iface_idx)
                        )

                    if self.videostreaming_interface_descriptors._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        i_desc_obj['videostreaming_interface_descriptors'] = []
                        i_desc_obj['videostreaming_interface_descriptors'].extend(
                            self.videostreaming_interface_descriptors._get_objects_list(idx, iface_idx)
                        )

                    if self.endpoint_descriptors._entries_for_this_bus_and_interface_idx_exist(idx, iface_idx):
                        i_desc_obj['endpoint_descriptors'] = []
                        i_desc_obj['endpoint_descriptors'].extend(
                            self.endpoint_descriptors._get_objects_list(idx, iface_idx)
                        )

                    # add the object to the list of interface descriptors
                    self.output_line['device_descriptor']['configuration_descriptor']['interface_descriptors'].append(i_desc_obj)

            # add final root-level keys
            if self.hub_descriptor._entries_for_this_bus_exist(idx):
                self.hub_descriptor._update_output(idx, self.output_line)

            for hps in self.hub_port_status_list:
                keyname = tuple(hps.keys())[0]

                if '_state' in hps[keyname] and hps[keyname]['_state']['bus_idx'] == idx:
                    self.output_line['hub_descriptor']['hub_port_status'].update(hps)
                    del self.output_line['hub_descriptor']['hub_port_status'][keyname]['_state']

            for dq in self.device_qualifier_list:
                keyname = tuple(dq.keys())[0]

                if '_state' in dq[keyname] and dq[keyname]['_state']['bus_idx'] == idx:
                    self.output_line['device_qualifier'].update(dq)
                    del self.output_line['device_qualifier'][keyname]['_state']

            for ds in self.device_status_list:

                if '_state' in ds and ds['_state']['bus_idx'] == idx:
                    self.output_line['device_status'].update(ds)
                    del self.output_line['device_status']['_state']


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

    lsusb = _LsUsb()

    if jc.utils.has_data(data):

        # fix known too-long field names
        data = data.replace('bmNetworkCapabilities', 'bmNetworkCapabilit   ')

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
