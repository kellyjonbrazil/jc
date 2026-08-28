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
                "videocontrol_interface_descriptors": [
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
                "videostreaming_interface_descriptors": [
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
                "audiocontrol_interface_descriptors": [
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
                "audiostreaming_interface_descriptors": [
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
                "midistreaming_interface_descriptors": [
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
                    },
                    "audiostreaming_endpoint_descriptor": {
                      "<item>": {
                        "value":              string,
                        "description":        string,
                        "attributes": [
                                              string
                        ]
                      }
                    },
                    "midistreaming_endpoint_descriptor": {
                      "<item>": {
                        "value":              string,
                        "description":        string,
                        "attributes": [
                                              string
                        ]
                      }
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
    version = '2.1'
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


# Each non-root section's parent section and where its data attaches:
# (parent_section, key_in_parent, is_list). `parent_section` of None
# means the section attaches directly to the current bus/device object.
# `is_list` sections (e.g. multiple Endpoint Descriptors) get a new
# dict appended to a list on every occurrence; others merge into a
# single dict (last value wins for a duplicate key, as noted in the
# schema above). `key_in_parent` of None marks a section that isn't
# implemented: its lines are still tracked (so indentation stays
# correct for whatever follows) but discarded.
_SECTION_TREE = {
    'device_descriptor':                   (None, 'device_descriptor', False),
    'configuration_descriptor':            ('device_descriptor', 'configuration_descriptor', False),
    'interface_association':               ('configuration_descriptor', 'interface_association', False),
    'interface_descriptor':                ('configuration_descriptor', 'interface_descriptors', True),
    'cdc_header':                          ('interface_descriptor', 'cdc_header', False),
    'cdc_call_management':                 ('interface_descriptor', 'cdc_call_management', False),
    'cdc_acm':                             ('interface_descriptor', 'cdc_acm', False),
    'cdc_union':                           ('interface_descriptor', 'cdc_union', False),
    'cdc_mbim':                            ('interface_descriptor', 'cdc_mbim', False),
    'cdc_mbim_extended':                   ('interface_descriptor', 'cdc_mbim_extended', False),
    'hid_device_descriptor':               ('interface_descriptor', 'hid_device_descriptor', False),
    'report_descriptors':                  ('hid_device_descriptor', None, False),  # not implemented
    'endpoint_descriptor':                 ('interface_descriptor', 'endpoint_descriptors', True),
    'videocontrol_interface_descriptor':   ('interface_descriptor', 'videocontrol_interface_descriptors', True),
    'videostreaming_interface_descriptor': ('interface_descriptor', 'videostreaming_interface_descriptors', True),
    'audiocontrol_interface_descriptor':   ('interface_descriptor', 'audiocontrol_interface_descriptors', True),
    'audiostreaming_interface_descriptor': ('interface_descriptor', 'audiostreaming_interface_descriptors', True),
    'audiostreaming_endpoint_descriptor':  ('endpoint_descriptor', 'audiostreaming_endpoint_descriptor', False),
    'midistreaming_interface_descriptor':  ('interface_descriptor', 'midistreaming_interface_descriptors', True),
    'midistreaming_endpoint_descriptor':   ('endpoint_descriptor', 'midistreaming_endpoint_descriptor', False),
    'hub_descriptor':                      (None, 'hub_descriptor', False),
    'hub_port_status':                     ('hub_descriptor', 'hub_port_status', False),
    'device_qualifier':                    (None, 'device_qualifier', False),
    'device_status':                       (None, 'device_status', False),
    'binary_object_store':                 (None, None, False),  # not implemented
}

# section headers, matched with str.startswith(), mapped to their
# _SECTION_TREE name. 'Bus ' and 'Device Status:' are handled
# separately since their line also carries data.
_SECTION_HEADERS = (
    ('    Interface Descriptor:', 'interface_descriptor'),
    ('      Endpoint Descriptor:', 'endpoint_descriptor'),
    ('      VideoControl Interface Descriptor:', 'videocontrol_interface_descriptor'),
    ('      VideoStreaming Interface Descriptor:', 'videostreaming_interface_descriptor'),
    ('      AudioControl Interface Descriptor:', 'audiocontrol_interface_descriptor'),
    ('      AudioStreaming Interface Descriptor:', 'audiostreaming_interface_descriptor'),
    ('        AudioStreaming Endpoint Descriptor:', 'audiostreaming_endpoint_descriptor'),
    ('      MIDIStreaming Interface Descriptor:', 'midistreaming_interface_descriptor'),
    ('        MIDIStreaming Endpoint Descriptor:', 'midistreaming_endpoint_descriptor'),
    ('Device Descriptor:', 'device_descriptor'),
    ('  Configuration Descriptor:', 'configuration_descriptor'),
    ('    Interface Association:', 'interface_association'),
    ('      CDC Header:', 'cdc_header'),
    ('      CDC Call Management:', 'cdc_call_management'),
    ('      CDC ACM:', 'cdc_acm'),
    ('      CDC Union:', 'cdc_union'),
    ('        HID Device Descriptor:', 'hid_device_descriptor'),
    ('         Report Descriptors:', 'report_descriptors'),
    ('      CDC MBIM:', 'cdc_mbim'),
    ('      CDC MBIM Extended:', 'cdc_mbim_extended'),
    ('Hub Descriptor:', 'hub_descriptor'),
    (' Hub Port Status:', 'hub_port_status'),
    ('Device Qualifier (for other device speed):', 'device_qualifier'),
    ('Binary Object Store Descriptor:', 'binary_object_store'),
)

# sections whose key/val/description columns are wider than normal
_LARGER_HEADER_SECTIONS = {
    'videocontrol_interface_descriptor',
    'videostreaming_interface_descriptor',
    'cdc_mbim_extended',
}


class _LsUsb:
    def __init__(self):
        self.raw_output = []
        self.root = None
        self.stack = []      # list of (section_name, container) from root to current
        self.section = None  # current section name; None means no active/recognized section

        # section_header is formatted with the correct spacing to be used with
        # jc.parsers.universal.sparse_table_parse(). Pad end of string to be
        # at least len of 25. This value changes for different sections (e.g.
        # videocontrol & videostreaming)
        self.normal_section_header = 'key                   val description'
        self.larger_section_header = 'key                               val description'

        self.last_item = ''
        self.last_indent = 0
        self.attribute_value = False
        self.fresh_section = False

    @staticmethod
    def _count_indent(line):
        indent = 0
        for char in line:
            if char != ' ':
                break
            indent += 1
        return indent

    def _enter_section(self, section_name):
        """
        Move to the container for `section_name`, creating/attaching it
        under its parent as needed, and reset attribute-line tracking
        for the new section. Returns the new current container.
        """
        parent_name, key, is_list = _SECTION_TREE[section_name]

        while self.stack and self.stack[-1][0] != parent_name:
            self.stack.pop()

        parent_container = self.stack[-1][1] if self.stack else self.root

        if key is None:
            container = {}  # not implemented; content is parsed then discarded
        elif is_list:
            container = {}
            parent_container.setdefault(key, []).append(container)
        else:
            container = parent_container.setdefault(key, {})

        self.stack.append((section_name, container))
        self.section = section_name
        self.attribute_value = False
        self.fresh_section = True

        return container

    def _start_new_bus(self, line):
        if self.root is not None:
            self.raw_output.append(self.root)

        # Bus 002 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
        line_split = line.strip().split(maxsplit=6)
        self.root = {
            'bus': line_split[1],
            'device': line_split[3][:-1],
            'id': line_split[5],
            # way to get a list item or None
            'description': (line_split[6:7] or [None])[0],
        }
        self.stack = [(None, self.root)]
        self.section = 'bus'
        self.attribute_value = False
        self.fresh_section = True

    def _start_device_status(self, line):
        # Device Status:     0x0001
        container = self._enter_section('device_status')
        _, value = line.strip().split(':', maxsplit=1)
        container['value'] = value.strip()

    def _handle_section_header(self, line):
        """
        If `line` starts a new section, transition to it and return
        True. Otherwise return False.
        """
        if not line:
            self.section = None
            self.attribute_value = False
            return True

        if line.startswith('Bus '):
            self._start_new_bus(line)
            return True

        if line.startswith('Device Status:'):
            self._start_device_status(line)
            return True

        for prefix, section_name in _SECTION_HEADERS:
            if line.startswith(prefix):
                self._enter_section(section_name)
                return True

        return False

    def _add_hub_port_status_line(self, line):
        # Port 1: 0000.0103 power enable connect
        first_split = line.split(': ', maxsplit=1)
        port_field = first_split[0].strip()
        second_split = first_split[1].split(maxsplit=1)
        port_val = second_split[0]
        attributes = second_split[1].split()

        self.stack[-1][1][port_field] = {
            'value': port_val,
            'attributes': attributes,
        }

    def _add_content_line(self, line):
        indent = self._count_indent(line)

        # determine whether this is a top-level value item or a
        # lower-level attribute of the last-seen item. The first line
        # of a freshly-entered section is never an attribute, even if
        # its indentation happens to look like a continuation.
        if self.fresh_section:
            self.attribute_value = False
        elif indent > self.last_indent:
            self.attribute_value = True
        elif indent == self.last_indent and self.attribute_value:
            self.attribute_value = True
        else:
            self.attribute_value = False

        self.fresh_section = False

        section_header = self.normal_section_header
        if self.section in _LARGER_HEADER_SECTIONS:
            section_header = self.larger_section_header

        parsed = sparse_table_parse([section_header, line.strip() + (' ' * 25)])[0]

        container = self.stack[-1][1]

        if self.attribute_value:
            target = container.setdefault(self.last_item, {})
            this_attribute = f'{parsed["key"]} {parsed["val"] or ""} {parsed["description"] or ""}'.strip()
            target.setdefault('attributes', []).append(this_attribute)
        else:
            entry = {}
            if parsed['val'] is not None:
                entry['value'] = parsed['val']
            if parsed['description'] is not None:
                entry['description'] = parsed['description']
            container[parsed['key']] = entry
            self.last_item = parsed['key']

        self.last_indent = indent

    def _handle_content_line(self, line):
        if self.section is None or not line.startswith(' '):
            return

        if self.section == 'device_status':
            self.stack[-1][1]['description'] = line.strip()
            return

        if self.section == 'hub_port_status':
            # deeper-indented sub-lines (e.g. "Ext Status:") are not implemented
            if not line.startswith('     '):
                self._add_hub_port_status_line(line)
            return

        self._add_content_line(line)


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

            if lsusb._handle_section_header(line):
                continue

            lsusb._handle_content_line(line)

    if lsusb.root is not None:
        lsusb.raw_output.append(lsusb.root)

    return lsusb.raw_output if raw else _process(lsusb.raw_output)
