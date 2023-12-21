[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.lsusb"></a>

# jc.parsers.lsusb

jc - JSON Convert `lsusb` command output parser

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

<a id="jc.parsers.lsusb.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/lsusb.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/lsusb.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
